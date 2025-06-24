from transformers import AutoTokenizer, AutoModelForSequenceClassification ,DistilBertForTokenClassification, DistilBertForSequenceClassification
import torch 
from multi_function_tools import *
from config import NLU_FUNCTION_MODEL, NLU_COLLECT_MODEL

class NLU: 

    def __init__( self ) :
        self.__user_history_input = ""
        self.__user_input = ""
        self.__encoding_input = None
        self.user_task_stack = []
        self.model_tokenizer = None
        self.model_chat = None 
        self.model_collect = None 
        self.model_function = None
        self.ask_question = None
        self.predict_task = []
        self.__Load_Model()
        self.mulitlabel_table = Create_MultiLabel_Dictionary()

    def __Load_Model( self ) :
        self.model_tokenizer = AutoTokenizer.from_pretrained( "lxyuan/distilbert-base-multilingual-cased-sentiments-student" )
        # self.model_collect = AutoModelForSequenceClassification.from_pretrained( "CHATBOT/model_collect/checkpoint-2000" )
        # self.model_chat  = AutoModelForSequenceClassification.from_pretrained( "CHATBOT/model_chat/checkpoint-2000" )
        self.model_function  = AutoModelForSequenceClassification.from_pretrained( NLU_FUNCTION_MODEL )
        # self.model_ask_question = AutoModelForSequenceClassification.from_pretrained( "CHATBOT/Is_it_ask_restaurant_question/checkpoint-2000" )
        self.model_collect_one_round = AutoModelForSequenceClassification.from_pretrained( NLU_COLLECT_MODEL )
    def Predict_Chat( self ) :

        model = self.model_chat
        self.__encoding_input.to( model.device )
        outputs = model( **self.__encoding_input )

        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid( outputs.logits[0].cpu() )

        if probs > 0.6 :  # 判定為聊天
            return 1
        else:
            return 0

    def Predict_Ask_Question( self, message ) :

        self.Set_Input( message ) # encoding

        model = self.model_ask_question
        self.__encoding_input.to( model.device )
        outputs = model( **self.__encoding_input )

        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid( outputs.logits[0].cpu() )

        if probs > 0.6 :  # 判定為此詢問為詢問的問題
            return 1
        else:
            return 0
           
    
    def Predict_Collect( self ) :

        model = self.model_collect
        self.__encoding_input.to( model.device )
        outputs = model( **self.__encoding_input )

        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid( outputs.logits[0].cpu() )


        if probs > 0.6 : # 判定為收集資訊
            return 1
        else:
            return 0

    def Predict_Function( self ) :

        pre = [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0]

        classes =  ['聊天', '導航', '推薦', '訂位', '詢問', 1, 2, 3, 4, 5]



        model = self.model_function
        self.__encoding_input.to( model.device )
        outputs = model( **self.__encoding_input )

        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid( outputs.logits[0].cpu() )


        print("Predict_Function Probs: ", end='')
        print( probs )

        positions = ( probs > 0.7 ).nonzero( as_tuple=True )[0].tolist()

        for i in positions:
            pre[i] = 1

        # print( pre )

        if tuple( pre ) in self.mulitlabel_table :
            pre_label = list( self.mulitlabel_table[ tuple( pre ) ] )
        else:
            pre_label = []


        

        return pre_label  # list( 類別 )


    def Predict1( self, user_inputs, history_inputs ) : # 先判段是否聊天  是:判斷是否收集資訊 否:判斷是否有功能  

        self.Set_History_Input( history_inputs ) 
        predict = self.Predict_Chat()
        if predict == 1 : 
            predict = self.Predict_Collect()
            if predict == 1 :
                self.predict_task = ['收集資訊']
            else :
                self.predict_task = ['聊天']
        else :
            self.Set_Input( user_inputs ) 
            predict = self.Predict_Function()
            if len( predict ) == 0 :
                self.predict_task = ['聊天(假)']
            else :
                self.predict_task = predict

        self.Stack_Add()



    def Predict2( self, user_inputs, history_inputs ) : # 先判段是否有功能   否:判斷是否聊天  是:判斷是否收集資訊


        self.Set_Input( user_inputs ) 
        predict = self.Predict_Function()
        if len( predict ) == 0 :
            self.Set_History_Input( history_inputs ) 
            predict = self.Predict_Chat()
            if predict == 1 : 
                predict = self.Predict_Collect()
                if predict == 1 :
                    self.predict_task = ['收集資訊']
                else :
                    self.predict_task = ['聊天']
            else:
                self.predict_task = ['聊天(假)']
        else :
            self.predict_task = predict

        self.Stack_Add()

    def Predict3( self, user_inputs, history_inputs ) : # 先判段是否有功能   如果是詢問則判斷是不是詢問問題  沒有功能的情況判斷是否收集資訊


        self.Set_Input( user_inputs ) 
        predict = self.Predict_Function()
        
        print( "功能" )
        print( predict )


        if len( predict ) == 0 :
            self.Set_History_Input( history_inputs ) 
            predict = self.Predict_Collect()

            print( "詢問" )
            print( predict )
            if predict == 1 : 
                self.predict_task = ['收集資訊']
            else :
                self.predict_task = ['聊天']
        else :
            self.predict_task = predict
            
        self.Stack_Add()

    def Predict4( self, user_inputs, history_inputs ) : # 先判段是否有功能   如果是詢問則判斷是不是詢問問題  沒有功能的情況判斷是否收集資訊

        one_round_input = history_inputs

        print( "(Predict4) one_round_input: " + one_round_input )

        self.Set_Input( one_round_input ) 
        predict = self.Predict_Collect_One_Round()

        if predict == 1 : 
            self.predict_task = ['收集資訊']
        else :
            self.Set_Input( user_inputs ) 
            print( "(Predict4) user_inputs:" + user_inputs )
            predict = self.Predict_Function()
            self.predict_task = predict

        
        print( "(Predict4) Result: " )
        print( self.predict_task )

        self.Stack_Add()

    def Predict_Collect_One_Round( self ) :  # 判斷 收集 or 功能
 
 
        model = self.model_collect_one_round
        self.__encoding_input.to( model.device )
        outputs = model( **self.__encoding_input )
 
        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid( outputs.logits[0].cpu() )
 
        print( "Collect_One_Round:" )
        print( probs )
 
 
        if probs > 0.501 : # 判定為收集資訊
            return 1
        else:
            return 0
 


    def Stack_Add( self ) :
        for task in self.predict_task :
            if task in self.user_task_stack:
                self.user_task_stack.remove( task )
                
            self.user_task_stack.append( task )

    def Get_Now_Do_Task( self ) :
        return self.user_task_stack[ -1 ]

    def Stack_Delete( self ) :
        if len( self.user_task_stack ) != 0  :
            self.user_task_stack.pop()

    def Get_Stack_Predict( self ) :    # stack中的任務有甚麼?
        return self.user_task_stack

    def Print_Stack_Predict( self ) :    # stack中的任務有甚麼?
        history_task = self.user_task_stack
        print("正式的NLU(Print_Stack_Predict) History_Stack_Task: " + str( history_task ) )

    def Get_Now_Predict( self ) :   # input句子的任務是??
        return self.predict_task

    def Get_ActuallyExecute_Predict( self ) :  #應該要執行的任務
        
        return self.__Tidy_User_History_Task()
            
    def __Tidy_User_History_Task( self ) :
        print( "__Tidy_User_History_Task1: ")
        print( self.user_task_stack )
        if len( self.user_task_stack ) != 0 :
            now_execute_task = self.user_task_stack[-1]
            if now_execute_task == "聊天" :
                self.Stack_Delete()
                return now_execute_task
            elif now_execute_task == "收集資訊":  # 收集資料的後面絕對不會是聊天和收集資料這兩項功能，所以只有空和function的可能
                print( "__Tidy_User_History_Task2: ")
                print( self.user_task_stack )
                self.Stack_Delete()
                print( "__Tidy_User_History_Task3: ")
                print( self.user_task_stack )
                if len( self.user_task_stack ) != 0 :
                    now_execute_task = self.user_task_stack[-1]  
                else:
                    now_execute_task = "聊天" 
                return now_execute_task 
                
            return now_execute_task
        else :
            return ['聊天']
        
    def Set_Input( self, inputs ) :  #把輸入的句子轉成(編碼)讓模型可以理解的樣子
        self.__user_input = inputs
        self.__encoding_input = self.model_tokenizer( inputs, return_tensors='pt')

    def Set_History_Input( self, inputs ) :  #把歷史輸入的句子轉成(編碼)讓模型可以理解的樣子
        self.__user_history_input = inputs
        self.__encoding_input = self.model_tokenizer( inputs, return_tensors='pt')


# a = NLU()

# a.Predict3( "這家餐廳有可以拍照的地方嗎", "這家餐廳有可以拍照的地方嗎" )
# print( a.predict_task )