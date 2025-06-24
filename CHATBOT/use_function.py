from chat_function import*
from sentence_transformers import SentenceTransformer, models, util
import torch
import json
from flask_socketio import SocketIO
import numpy as np
from config import TEXT2VEC_MODEL, TAG_EMBEDDINGS_JSON, UPDATED_STOREINFO_JSON

class Use_Function( NLG ):

    def __init__( self ):
        super().__init__()

    def Recommand(self, input_tags):
    # 加載模型
        print( "(Recommand_Function) input tag:", input_tags )
        local_model_path = TEXT2VEC_MODEL
        word_embedding_model = models.Transformer(local_model_path)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), 'max')
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        model = model.to('cuda')  # 確保模型在 GPU 上

        # 加載餐廳標籤向量
        with open( TAG_EMBEDDINGS_JSON, 'r', encoding='utf-8') as f:
            tag_embeddings = json.load(f)

        # 加載餐廳 ID 和名稱的映射
        with open( UPDATED_STOREINFO_JSON, 'r', encoding='utf-8') as f:
            store_info = json.load(f)
        store_id_to_name = {str(item['store_id']): item['store_name'] for item in store_info}

        # 計算用戶輸入標籤的整體向量（這裡採用平均方式）
        input_embeddings = [
            model.encode(tag, convert_to_tensor=True, device='cuda') for tag in input_tags
        ]  # 確保輸入張量在 GPU 上
        user_vector = torch.mean(torch.stack(input_embeddings), dim=0)  # 用戶標籤整體向量

        recommendations = []
        for store_id, info in tag_embeddings.items():
            # 將餐廳標籤整合為一個整體向量
            store_embeddings = [
                torch.tensor(tag, dtype=user_vector.dtype, device=user_vector.device) for tag in info['embeddings'].values()
            ]  # 確保餐廳標籤在相同設備上
            store_vector = torch.mean(torch.stack(store_embeddings), dim=0)  # 餐廳標籤整體向量

            # 計算用戶向量與餐廳向量的相似度
            similarity = util.pytorch_cos_sim(user_vector, store_vector).item()
            store_name = store_id_to_name.get(store_id, "未知餐廳")
            recommendations.append((store_name, similarity))

        # 按相似度排序，取前10個推薦
        top_k = sorted(recommendations, key=lambda x: x[1], reverse=True)[:10]

        store_rec_list = []
        # 回傳僅包含餐廳名稱的列表
        for i in top_k:
            store_rec_list.append(i[0])

        
        return store_rec_list


    def Map(self, address, room_id, message_queue, socketio):
        if address:
            # 發送導航指令到 Android 端
            socketio.emit('navigate_to_address', {'address': address}, room=room_id)
            print(f"導航地址已發送：{address}")
        else:
            # 如果沒有找到地址，提示用戶
            message_queue.put(["未找到導航地址，請重新描述。", room_id])
            print("導航失敗：未找到有效地址")


    def Reserve( self ):
        super().Use_Reserve( ) 

    def Ask( self, question, database ):
        answer = super().Ask_Question( question, database ) 
        return answer 


    def Chat( self, user_inputs, dp_mode=False ):
        answer = super().Chat( user_inputs, dp_mode ) 
        return answer 

