import openpyxl
from compare_text import*
# from all_user import*
import spacy
from compare_text import*
from database import*
from spacy_ruler import*
from config import SPACY_TIME_MODEL, SPACY_STORE_MODEL, SPACY_FOOD_MODEL, SPACY_DIA_RESERVE, SPACY_DIA_RECOMMAND, SPACY_DIA_MAP

class NER():

    def __init__( self ) :  # cp 是 compare_Similar class
        self.user_ner = { "PLACE":"中壢區",  "TIME2":"", "TIME":"", "DATE":"", "STORE":"一品魚麵", "FOOD":[], "ADJ":[], "ADDRESS":"桃園市中壢區中山東路四段33號", "QUESTION":"", "PEOPLE":"", "ASK_STORE":""  }
        self.time_model = spacy.load(SPACY_TIME_MODEL) #TIME, TIME2, DATE
        self.store_model = spacy.load(SPACY_STORE_MODEL) #STORE
        self.food_model = spacy.load(SPACY_FOOD_MODEL) #FOOD, ADJ, PLACE
        # self.all_model = spacy.load("CHATBOT/output1/model-best")
        # self.all_model = Add_Ruler(self.all_model)
        print( "NER_Normal_Store_Ruler Loading... ")
        self.store_model = Add_Ruler( self.store_model, [ 'STORE' ] )

        print( "NER_Normal_Food_Ruler Loading... ")
        self.food_model = Add_Ruler( self.food_model, [ 'FOOD', 'ADJ' ] )


        self.dailogue_reserve = spacy.load( SPACY_DIA_RESERVE )
        print( "NER_Dialogue_Reserve_Ruler Loading... ")
        self.dailogue_reserve = Add_Ruler( self.dailogue_reserve, [ 'STORE', 'TIME', 'TIME2', "DATE", 'PEOPLE' ] )


        self.dailogue_recommand = spacy.load( SPACY_DIA_RECOMMAND )
        print( "NER_Dialogue_Recommand_Ruler Loading... ")
        self.dailogue_recommand = Add_Ruler( self.dailogue_recommand, [ 'FOOD', 'ADJ' ] )

        
        self.dailogue_map = spacy.load( SPACY_DIA_MAP )
        print( "NER_Dialogue_Map_Ruler Loading... ")
        self.dailogue_map = Add_Ruler( self.dailogue_map, [ 'STORE' ] )



    def Dialogue_NER_Predict( self, inputs, history, nlu_result ) : #一輪機器和使用者的對話去判別NER
        if len( history ) >= 3 :
            sentence = f"<BOT>{ history[-2] }<USER>{ history[-1] }\r"
            print( "spacy_function( Dialogue_NER_Predict ) : " + sentence )

            if nlu_result == "導航":
                model = self.dailogue_map
                self.Dialogue_Ner( sentence, model )
            elif nlu_result == "訂位":
                model = self.dailogue_reserve
                self.Dialogue_Ner( sentence, model )
            elif  nlu_result == "推薦":
                model = self.dailogue_recommand
                self.Dialogue_Ner( sentence, model )
            elif nlu_result == "詢問":
                self.Ask_Ner( inputs )
            else:
                pass
                
            
        else: 
            # self.AllFunction_Ner_1( inputs )  # 全部label的模型  choose 1

            #choose 2 根據NLU 去使用適合的NER model 
            if nlu_result == "導航":
                self.Nativgate_Ner( inputs )
            elif nlu_result == "訂位":
                self.Recommand_Ner( inputs )
            elif  nlu_result == "推薦":
                self.Recommand_Ner( inputs )
            elif nlu_result == "詢問":
                self.Ask_Ner( inputs )

    def Place_Pre_InLabel( self, information_dict ) : #把偵測到的標籤放到user的ner欄位

        for label in information_dict :
            
            if label in  self.user_ner :
                    
                text = information_dict[ label ]

                self.user_ner[ label ] = text
        


    def Place_Answer_InLabel(self, information_dict):
        for label in information_dict:
            value = information_dict.get(label)
        
            # 若 `value` 為空，跳過該標籤
            if not value:
                print(f"Place_Answer_InLabel Skipping label {label} as it has no value.")
                continue
        
            print("Place_Answer_InLabel 預測到的: Label:", label, "Value:", value)
            
            if label == "STORE":
                maybe_store_list = global_cp.Search_Similar_And_Let_User_Choose(value, label)
                # 如果有結果，列出所有可能的店家名稱
                if maybe_store_list:
                    text = '、'.join(maybe_store_list)  # 列出所有店家名稱
                    self.user_ner[label] = text
                else:
                    text = ""
                    self.user_ner[label] = text

            elif label == "QUESTION" :
                text = value
                self.user_ner[label] = text
            elif label == "FOOD" or label == "ADJ" :

                temp_text = []

                for pre in self.user_ner[ label ] :
                    text = global_cp.Search_Similar( pre, label)
                    if text not in temp_text and text != "" :
                        temp_text.append( text ) 

                self.user_ner[label] = temp_text
                
            else:
                text = global_cp.Search_Similar(value, label)
                self.user_ner[label] = text


            if text == "":
                print( "Place_Answer_InLabel 找不到相似的" )





    def Predict_Ner( self, inputs, ner_model=None ): #選用ner_model預測獲得預測的結果

        ner_doc = ner_model( inputs )
        pre_ner = { 'FOOD':[], 'ADJ':[] }

        for X in ner_doc.ents :
            if X.label_ == "FOOD" or X.label_ == "ADJ" :
                pre_ner[ X.label_ ].append( X.text )
            else :
                pre_ner[ X.label_ ] = X.text

        return pre_ner

    def Dialogue_Ner( self, inputs, model ) :
        pre_ner = self.Predict_Ner( inputs, model )
        self.Place_Pre_InLabel( pre_ner )
        self.Place_Answer_InLabel( pre_ner )

    def Nativgate_Ner( self, inputs ) :  # 導航需要的ner偵測

        pre_ner = self.Predict_Ner( inputs, self.store_model )
        self.Place_Pre_InLabel( pre_ner )
        self.Place_Answer_InLabel( pre_ner )


    def Recommand_Ner( self, inputs ) :  # 推薦需要的ner偵測

        pre_ner = self.Predict_Ner( inputs, self.food_model )

        self.Place_Pre_InLabel( pre_ner )
        self.Place_Answer_InLabel( pre_ner )

    def Reserve_Ner( self, inputs ) : # 訂位需要的ner偵測

        pre_ner = self.Predict_Ner( inputs, self.store_model )
        pre_ner.update( self.Predict_Ner( inputs, self.store_time ) )

        self.Place_Pre_InLabel( pre_ner )
        self.Place_Answer_InLabel( pre_ner )

    def Ask_Ner( self, inputs ) : # 詢問需要的ner偵測

        pre_ner = self.Predict_Ner( inputs, self.store_model )

        self.Place_Pre_InLabel( pre_ner )
        self.Place_Answer_InLabel( pre_ner )

    def AllFunction_Ner( self, inputs ) : # 所有的ner偵測
        pre_ner = self.Predict_Ner( inputs, self.time_model )
        pre_ner.update( self.Predict_Ner( inputs, self.store_model ) )
        pre_ner.update( self.Predict_Ner( inputs, self.food_model ) )

        self.Place_Pre_InLabel( pre_ner )
        self.Place_Answer_InLabel( pre_ner )

    def Get_User_NER( self ) :
        return self.user_ner

    def Replace_label( self, data, label ):
        if label == "FOOD" or label == "ADJ":
            self.user_ner[label] = [data] 
        else :
            if label == "STORE" :
                self.user_ner["STORE"] = data 
                self.user_ner["ASK_STORE"] = data 
            else :
                self.user_ner[label] = data 


    def Get_User_NER_Label( self, label ) :
        return self.user_ner[ label ]

    def Get_User_Ner_Food_Adj_MergeToList( self ) :
        
        recommand_key = []

        food = self.Get_User_NER_Label( "FOOD" )
        adj = self.Get_User_NER_Label( "ADJ" )

        if not isinstance( food, list ) : 
            if food != "":
                recommand_key.append( food )
        else :
            for i in food :
                recommand_key.append( i )

        if not isinstance( adj, list ) :
            if adj != "":
                recommand_key.append( adj )
        else :
            for i in adj :
                recommand_key.append( i )

        return recommand_key       


    def AllFunction_Ner_1( self, inputs ) : # 所有的ner偵測

        pre_ner = self.Predict_Ner( inputs, self.all_model )

        self.Place_Pre_InLabel( pre_ner )
        self.Place_Answer_InLabel( pre_ner ) 

    def Clear_Ner( self, function_label ) :
        if function_label == "reserve" :
            self.user_ner[ 'PEOPLE' ] = ""
            self.user_ner[ 'TIME' ] = ""
            self.user_ner[ 'TIME2' ] = ""
            self.user_ner[ 'DATE' ] = ""
            self.user_ner[ 'STORE' ] = ""
        elif function_label == "recommand" :
            self.user_ner[ 'FOOD' ] = []
            self.user_ner[ 'ADJ' ] = []
        elif function_label == "map" :
            self.user_ner[ 'ADDRESS' ] = ""
        elif function_label == "ask" :
            self.user_ner[ 'ASK_STORE' ] = ""
# db = DataBase( )

# # print("ddddddddddddddd")

# cp = Comapare_Similiar( db.Get_WordTable( ) )

# # cp.Search_Similar( "燒臘", 'store' )

# a = NER( )

# test = "我想要在3.10睡覺"

# a.AllFunction_Ner( test )

# print( str( a.user_ner ) )

