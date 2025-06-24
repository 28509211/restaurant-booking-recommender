# import spacy 
from transformers import AutoTokenizer, AutoModelForSequenceClassification ,DistilBertForTokenClassification, DistilBertForSequenceClassification
import torch 
from classification_function import*
from spacy_function import*
from chat_function import*
from langchain_community.document_loaders import TextLoader
from dp_function import*
from test_ner_function import*
from test_nlu_function import*
from use_function import*

class User:
    def __init__( self ):

        # model 
        self.ner = None
        self.classification = None
        self.chatbot = None

        self.__Load_NER()
        self.__Load_NLU()

        self.__Load_Function_And_NLG()

        self.task_stack = [] # 使用者的NLU stack


        #USER INPUT
        self.history_input = ""
        self.history = []  # 使用者對話紀錄
        self.input = ""  # 使用者目前對話

                
    def __Load_NER( self ) :
        self.ner = NER()

    def __Load_NLU( self ) :
        self.classification = NLU()

    def __Load_Function_And_NLG( self ) :
        self.chatbot_function = Use_Function( )

    def Use_NER( self, inputs, nlu_result, debug=False ) :
        if debug == False:

            self.ner.Dialogue_NER_Predict( inputs, self.history, nlu_result )

            return self.ner.user_ner
        else:
            not_end = True 
            test_ner = {}
            while not_end :
                test_ner.update( test_add_ner() )
                not_end = input( "要結束嗎? (0, 1):" )
                if not_end == "1" :
                    not_end = False 
                else :
                    not_end = True

            self.ner.Place_Pre_InLabel( test_ner )
            self.ner.Place_Answer_InLabel( test_ner )

            # self.Set_Input( inputs )
            return self.ner.user_ner

    def Change_NER( self, data, label ):
        self.ner.Replace_label( data, label ) 
    

    def Use_Dp( self, nlu_type ):
        ner_result = self.ner.user_ner
        ner_finded_times = global_cp.Get_Ner_Finded_Times()
        ner_not_finded = global_cp.Get_Ner_Not_Finded()

        dp_sentence = global_dp.Choose_Dp( nlu_type, ner_result, ner_finded_times, ner_not_finded )

        return dp_sentence

    

    def Use_NLU( self, message, debug=False ) :
        if debug == False:

            self.Set_Input( message ) #設定input 和加入history

            self.history_input = self.Tidy_History( self.history )
            self.classification.Predict4( message, self.history_input )  #會自動把該輪預測出的 意圖 加入到stack  
            now_task = self.classification.Get_ActuallyExecute_Predict()

            self.classification.Print_Stack_Predict()  #印 stack 的 功能
            return now_task
        else:  # test模式
            self.Set_Input( message ) #設定input 和加入history
            test_predict = test_nlu()
            return test_predict


    def Use_NLG_Chat( self, message, dp_mode=False ) :
      answer = self.chatbot_function.Chat( message, dp_mode )
      return answer

    def Use_NLG_Ask( self, message, store_data ) :
      loader = TextLoader( store_data )
      database = loader.load()
      answer = self.chatbot_function.Ask( message, database )
      return answer


    def Set_Input( self, inputs, BOT=False ) :
        if BOT :
            self.history.append( inputs )
        else :
            self.input = inputs 
            self.history.append( inputs )


    def Get_Input( self ) :
        return self.input

    def Get_History_Input( self ) :
        return self.history

    def Tidy_History( self, history_list ) :
        history_input = ""
        if len( history_list ) > 1 :
            history_input =  history_list[-2] + "<SEP>" + history_list[-1]
        else :
            if len( history_list ) == 1 :
                history_input = history_list[0]
            else :
                history_input = ""


        return history_input

    def Clear_History( self ) :
        self.history_input = ""
        self.history = []
        
    def Use_NLG_Reserve(self, user_reserve_information ):
        self.chatbot_function.Use_Reserve( user_reserve_information )

    def Use_Recommand(self, input_tags):
        return self.chatbot_function.Recommand( input_tags )
        
    def Use_Map(self, address, room_id, message_queue, socketio):
        self.chatbot_function.Map( address, room_id, message_queue, socketio )

    
    def Use_Ask_Question(self, question, database ):
        answer = self.chatbot_function.Ask_Question( question, database )
        return answer 

    def Predict_Is_Question( self, message ) :
        ask_question_pre = self.classification.Predict_Ask_Question( message )
        if ask_question_pre == 1 : 
            return True
        else :
            return False

    def Delete_Executed_Task( self ) :
        self.classification.Stack_Delete()
        print("=======================================")
        print( "結束功能執行後的NLU: ")
        print( self.classification.Print_Stack_Predict() )
        print("=======================================")

    def User_Get_Ner_Label_Data( self, label ) :
        return self.ner.Get_User_NER_Label( label )

    
    def User_Get_Ner_Food_Adj_MergeList( self ) :
        return self.ner.Get_User_Ner_Food_Adj_MergeToList( )

    def Set_Ner_Label( self, label, ner_message ) :
        self.ner.Replace_label( ner_message, label  )

    def Replace_Ner( self, data, label ) :
        self.ner.Replace_label( data, label )

    def Clear_Ner( self, function_label ) :
        self.ner.Clear_Ner( function_label )
        print("=======================================")
        print( "結束功能執行後的NER: ")
        print( self.ner.Get_User_NER() ) 
        print("=======================================")

