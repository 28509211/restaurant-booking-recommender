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
from database import*
from config import NER_NLU_TEST_REVIEW

class User:
    def __init__( self ):

        # model 
        self.ner = None
        self.classification = None
        self.chatbot = None
        self.database = Database()
        self.dp = DP()

        self.__Load_NER()
        self.__Load_NLU()

        self.__Load_Function_And_NLG()

        self.task_stack = [] # 使用者的NLU stack


        #USER INPUT
        self.history_input = []
        self.history_output = []
        self.history = []  # 使用者對話紀錄
        self.input = ""  # 使用者目前對話

                
    def __Load_NER( self ) :
        self.ner = NER()

    def __Load_NLU( self ) :
        self.classification = NLU()

    def __Load_Function_And_NLG( self ) :
        self.chatbot_function = Use_Function( )

    def Use_NER( self, message, nlu_result, debug=False ) :
        self.ner.Dialogue_NER_Predict( message, self.history_input, nlu_result )
        ner_result = self.ner.Get_User_NER()
        if debug:
            print( "NER result: ", ner_result )
        return ner_result

    def Change_NER( self, data, label ):
        self.ner.Replace_label( data, label ) 
    

    def Use_Dp( self, nlu_result ) :
        dp_result = self.dp.Dialogue_Management( self.history_input, nlu_result )
        return dp_result

    

    def Use_NLU( self, message, debug=False ) :
        nlu_result = self.classification.Predict_Function( message )
        if debug:
            print( "NLU result: ", nlu_result )
        return nlu_result


    def Use_NLG_Chat( self, message, dp_mode=False ) :
      answer = self.chatbot_function.Chat( message, dp_mode )
      return answer

    def Use_NLG_Ask( self, message, store_data ) :
      store_data = "CHATBOT/NER_NLU/test_review.txt"
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

        # print( history_input )

        return history_input

    def Clear_History( self ) :
        self.history_input = []
        self.history = []
        
    def Use_NLG_Reserve(self, user_information ):
        answer = self.chatbot_function.Use_Reserve( user_information )
        return answer

    def Use_Recommand(self):
        answer = self.dp.Recommand_Function( self.ner.Get_User_NER_Label( "FOOD" ), self.ner.Get_User_NER_Label( "ADJ" ) )
        return answer
        
    def Use_Map(self):
        answer = self.dp.Map_Function( self.ner.Get_User_NER_Label( "STORE" ), self.ner.Get_User_NER_Label( "ADDRESS" ) )
        return answer

    
    def Use_Ask_Question(self, question, database ):
        store_data = NER_NLU_TEST_REVIEW
        answer = self.chatbot_function.Ask_Question( question, store_data )
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

    def Use_Get_Ner_Label_Data( self, label ) :
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


# user = User()
# user.Use_NER("你好")