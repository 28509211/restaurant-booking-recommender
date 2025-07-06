from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from llamafactory.chat import ChatModel
from llamafactory.extras.misc import torch_gc
import time
import requests
from dotenv import load_dotenv
from config import NLG_MODEL_PATH, NLG_ADAPTER_PATH, EMBEDDING_MODEL
from dotenv import load_dotenv
import os

load_dotenv()


class NLG : 

    def __init__( self ) :
  
        args = dict(
            model_name_or_path=NLG_MODEL_PATH,
            adapter_name_or_path=NLG_ADAPTER_PATH,
            template="llama3",                     # same to the one in training
            finetuning_type="lora",                  # same to the one in training
            quantization_bit=4,                    # load 4-bit quantized model
        )

        self.chat_model = ChatModel(args)

        self.embeddings = self.__Load_Embedding()
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=30,
        )




    def __Set_DateTable( self, datatable ):  # 設定資料庫資料(店家的所有評論data)

        loader = TextLoader( datatable, encoding='utf-8' )
        pages = loader.load()

             
        docs = self.text_splitter.split_documents( pages ) #切

        db = FAISS.from_documents( docs, self.embeddings ) #把文檔轉向量

        return db


    def __Load_Embedding( self ) :


        modelPath = EMBEDDING_MODEL


        embeddings = HuggingFaceEmbeddings(
            model_name = modelPath,
        )

        return embeddings


    def __Set_Templete( self, soure_knowledge, query ) :


        argument_prompt = f"""你現在是一位專業的餐助理，請根據以下資訊回答問題：
                            1. 若資訊中包含與問題相關的答案，請直接回答，避免多餘的標點符號。
                            2. 若資訊不足以回答，請描述評論中提到的其他特色，但回答不能超過50字。
                            3. 請保持回答簡短且不包含無意義的重複內容。
                            
        context:    
        { soure_knowledge }

        query:
        { query }\n
        """

        return argument_prompt

    def __Clean_Answer(self, answer):
        import re

        # 移除連續的重複標點符號
        answer = re.sub(r"[，。！？]{2,}", "，", answer)

        # 如果回答過於空洞或只有符號，提供預設回答
        if len(answer) < 5 or all(char in "，。！？" for char in answer):
            return "抱歉，目前無法根據評論提供回答，但可以參考我們的熱門推薦。"

        return answer


    def Ask_Question(self, question, database):  # 詢問
        messages = []

        # 設定該家評論的資料庫
        db = self.__Set_DateTable(database)

        query = question
        result = db.similarity_search(query, k=5)

        # 組合找到的評論並清理內容
        soure_knowledge = ""
        for doc in result:
            clean_content = doc.page_content.replace("，", "，").strip()  # 清理多餘標點符號與空格
            soure_knowledge += clean_content + "\n"

        # 如果無法找到相關評論，給出預設上下文
        if not soure_knowledge.strip():
            soure_knowledge = "目前沒有找到相關評論內容。"

        # 使用模板生成 prompt
        argument_prompt = self.__Set_Templete(soure_knowledge, question)

        # 添加到對話消息列表
        messages.append({"role": "user", "content": argument_prompt})

        # NLG 輸出
        try:
            answer = self.chat_model.chat(messages)
            answer_text = answer[0].response_text.strip()
        except Exception as e:
            # 處理可能的錯誤
            print(f"生成回答時出錯: {e}")
            return "抱歉，目前無法提供回答。"

        # 清理生成的回答
        clean_answer = self.__Clean_Answer(answer_text)

        # 返回清理後的回答
        return clean_answer


    def Chat( self, user_inputs, dp_mode = False ):
        
        messages = []

        messages.append({"role": "user", "content": user_inputs})

        if dp_mode  :
            system_prompt = "根據以下這段話描述出引導式的回答給使用者"
            answer = self.chat_model.chat( messages, system= system_prompt ) 
        else:
            system_prompt = """ 你是一位客服人員，可以提供使用者以下這些功能:
                                1.聊天:與使用者進行進行日常對話和互動，限於簡單問答與閒聊。
                                2.訂位:根據使用者提供的信息（餐廳名稱、日期、時間、用餐人數等），幫助撥打電話進行訂位，並確認成功與否。若缺少必要信息，會引導使用者補充完整。
                                3.推薦:根據使用者描述的需求（如地點、菜系、價位等），從可用的餐廳名單中篩選並推薦最適合的選擇。若有多個選項，會提供簡短的描述供選擇。
                                4.詢問評論：當使用者對餐廳或菜品有具體疑問時，從餐廳評論中查找相關意見並回覆。僅限於餐廳的公共評論數據，無法提供專業評分。
                                5.導航:根據使用者提供的店家地址，提供導航指引，幫助其到達目的地。
                                系統只提供以上五項功能，除此之外不提供其他操作。如果使用者的需求超出以上四項功能範圍，系統會禮貌地提醒「此功能不在服務範圍內」，並引導他們重新描述問題或選擇適合的功能。
                                如果使用者表示「好無聊」或「不知道要做什麼」，系統會友善地回覆並簡單介紹可用的功能，鼓勵他們進行互動。"""

            answer = self.chat_model.chat( messages, system= system_prompt ) 
        answer = answer[0].response_text
        
        print( answer )

        return answer

    def Reserve( self, clerk_inputs ):  
        
        messages = []

        system_prompt = "你是一位客服人員，負責處理顧客的訂位請求。"


        messages.append({"role": "user", "content": clerk_inputs})

        answer = self.chat_model.chat( messages, system= system_prompt ) 
        answer = answer[0].response_text

        print( answer )

        return answer

    def Use_Reserve( self, user_information ) :
 

        # 載入 .env 檔案中的環境變數
        load_dotenv()

        # 從環境變數中取得值
        api_key = os.getenv("BLAND_AI_API_KEY")

        # Headers
        headers = {
        'Authorization': api_key
        }

        # Data
        data = {
        "phone_number": "+886963877304",
        "from": "+14152264530",
        "task": f"在這個情境中，您將扮演顧客，撥打電話到餐廳進行訂位。根據使用者提供的訂位資訊，您與餐廳店員進行對話。在對話過程中，您需要確認以下資訊：\n\n訂位日期：{user_information['date']}\n訂位時間：{user_information['time']}\n姓名：使用者{user_information['username']}{user_information['gender']}\n人數：使用者提供的人數（例如 {user_information['people']}）\n當您與餐廳店員進行對話時：\n\n如果有空位：顧客確認訂位並感謝店員。\n如果沒有空位：顧客禮貌地表示感謝並理解，然後結束對話。\n缺少資訊：若顧客未提供完整資訊，店員會詢問必要的資料，顧客需要提供完整訂位細節。\n如果對方提出其他時間：如果店員告知某個時間沒有空位，顧客可以表示再考慮並告知會再撥電話確認。\n情境範例：\n\n訂位情境 - 有空位：\n\n顧客: 您好，我想在訂位，5位，姓林。\n店員: 您好，林先生/小姐，11月11日下午三點還有空位。請問您要預訂嗎？\n顧客: 是的，請幫我預訂，謝謝！\n店員: 好的，您的訂位已經完成，謝謝您！\n訂位情境 - 沒有空位：\n\n顧客: 您好，我想在11月11日下午三點訂位，5位，姓林。\n店員: 很抱歉，11月11日下午三點我們的座位已經滿了，您想要選擇其他時間嗎？\n顧客: 謝謝您的回覆，沒問題，祝您生意興隆！\n缺少資訊情境：\n\n顧客: 您好，我想訂位。\n店員: 您好，請問訂位的日期、時間以及人數是？\n顧客: 喔，對不起，我要訂11月11日下午三點，5位，姓林。\n店員: 好的，請稍等，我幫您查詢空位。\n提出其他時間情境：\n\n顧客: 您好，我想在11月11日下午三點訂位，5位，姓林。\n店員: 很抱歉，11月11日下午三點我們的座位已經滿了，您想要選擇其他時間嗎？\n顧客: 可以請問其他時間的空位情況嗎？\n店員: 我們有11月11日晚上7點的空位。\n顧客: 謝謝，我再考慮一下，可能會稍後再來電確認。\n語言要求：以上所有對話均需以中文(CHINESE)進行。",
        "model": "base",
        "language": "zh-TW",
        "voice": "nat",
        "voice_settings": {},
        "local_dialing": False,
        "max_duration": 12,
        "answered_by_enabled": True,
        "wait_for_greeting": True,
        "record": True,
        "amd": False,
        "interruption_threshold": 100,
        "transfer_list": {},
        "pronunciation_guide": [],
        "background_track": "none",
        "request_data": {},
        "tools": [],
        "dynamic_data": [],
        "analysis_schema": {},
        "calendly": {}
        }

        # API request 
        requests.post('https://us.api.bland.ai/v1/calls', json=data, headers=headers)




