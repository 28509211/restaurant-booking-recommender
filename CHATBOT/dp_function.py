
class Dp: 

    def __init__( self ) :


        # chatbot詢問該ner的次數(該ner為空的次數)

        self.ask_address_times = 0
        self.ask_store_times = 0
        self.ask_place_times = 0
        self.ask_food_times = 0
        self.ask_people_times = 0
        self.ask_date_times = 0
        self.ask_time_times = 0

    
    def Choose_Map_Dp(self, ner_result, ner_finded_times, ner_not_finded):
      if ner_result.get('ADDRESS', '') == '':
        if ner_finded_times.get('ADDRESS', 0) > 0:
            dp_sentence = f"導航服務，找不到 {ner_not_finded.get('ADDRESS', ['未知地址'])[0]} 此地址"
            self.ask_address_times = 0
        elif self.ask_address_times == 0:
            dp_sentence = '導航服務，詢問使用者要去的地方'
            self.ask_address_times += 1
        else:
            dp_sentence = '導航服務，再次詢問使用者要去的地方'
            self.ask_address_times += 1
        return dp_sentence

    
      dp_sentence = "導航服務，準備執行"
      self.ask_address_times = 0
      return dp_sentence



    def Choose_Ask_Dp( self, ner_result, ner_finded_times, ner_not_finded ) :

        dp_sentence = ""

        if ner_result[ 'ASK_STORE' ] == '' :       
            if ner_finded_times['STORE'] > 0 :
                dp_sentence = f"詢問店家服務，找不到  { ner_not_finded[ 'STORE' ][0] }  此類似名稱的店家"
                self.ask_store_times = 0
            elif self.ask_store_times == 0 :
                dp_sentence = '詢問店家服務，詢問使用者店家名稱資訊'
                self.ask_store_times = self.ask_store_times = 0+ 1 
            elif self.ask_store_times > 0 :
                dp_sentence = '詢問店家服務，再次詢問使用者店家名稱資訊'
                self.ask_store_times = self.ask_store_times + 1 
                

            return dp_sentence

        else:
            dp_sentence = "詢問店家服務，準備執行"
            self.ask_store_times = 0
            
        return dp_sentence


    def Choose_Recommand_Dp( self, ner_result, ner_finded_times, ner_not_finded ) :

        dp_sentence = ""

        if ner_result[ 'FOOD' ] == [] and ner_result[ 'ADJ' ] == [] and self.ask_food_times == 0 : 
            dp_sentence = "推薦服務，詢問使用者是否可以提供食物類型或是形容詞"   
            self.ask_food_times = self.ask_food_times + 1  
        else :  
            dp_sentence = "推薦服務，準備執行"
            self.ask_food_times = 0

        return dp_sentence

    def Choose_Reserve_Dp( self, ner_result, ner_finded_times, ner_not_finded ) :

        dp_sentence = ""

        if ner_result[ 'STORE' ] == '' :       
            if ner_finded_times['STORE'] > 0 :
                dp_sentence = f"訂位服務，找不到  { ner_not_finded[ 'STORE' ][0] }  此類似名稱的店家"
                self.ask_store_times = 0
            elif self.ask_store_times == 0 :
                dp_sentence = '訂位服務，詢問使用者店家名稱資訊'
                self.ask_store_times = self.ask_store_times = 0 + 1 
            elif self.ask_store_times > 0 :
                dp_sentence = '訂位服務，再次詢問使用者店家名稱資訊'
                self.ask_store_times = self.ask_store_times + 1 
                

            return dp_sentence

        # elif ner_result[ 'PLACE' ] == '' :
        #         # 模型的結果給dp_sentence
        #     if ner_finded_times['PLACE'] > 0 :
        #         dp_sentence = f"訂位服務，找不到 { ner_not_finded[ 'PLACE' ][0] }  此地區"
        #         self.ask_place_times = 0
        #     elif self.ask_place_times == 0 :
        #         dp_sentence = '訂位服務，詢問使用者地區資訊'
        #         self.ask_place_times = self.ask_place_times + 1 
        #     elif self.ask_place_times > 0 :
        #         dp_sentence = '訂位服務，再次詢問使用者地區資訊'
        #         self.ask_place_times = self.ask_place_times + 1 

        #     return dp_sentence

        elif ner_result[ 'PEOPLE' ] == '' :
                # 模型的結果給dp_sentence
            if ner_finded_times['PEOPLE'] > 0 :
                dp_sentence = f"訂位服務，{ ner_not_finded[ 'PEOPLE' ][0] }  人數不符合標準"
                self.ask_people_times = 0
            elif self.ask_people_times == 0 :
                dp_sentence = '訂位服務，詢問使用者人數資訊'
                self.ask_people_times = self.ask_people_times + 1 
            elif self.ask_people_times > 0 :
                dp_sentence = '訂位服務，再次詢問使用者日期資訊'
                self.ask_people_times = self.ask_people_times + 1 

            return dp_sentence


        elif ner_result[ 'DATE' ] == '' :
                # 模型的結果給dp_sentence
            if ner_finded_times['DATE'] > 0 :
                dp_sentence = f"訂位服務，{ ner_not_finded[ 'DATE' ][0] }  日期不符合標準"
                self.ask_date_times = 0
            elif self.ask_date_times == 0 :
                dp_sentence = '訂位服務，詢問使用者日期資訊'
                self.ask_date_times = self.ask_date_times + 1 
            elif self.ask_date_times > 0 :
                dp_sentence = '訂位服務，再次詢問使用者日期資訊'
                self.ask_date_times = self.ask_date_times + 1 

            return dp_sentence

        elif ner_result[ 'TIME' ] == '' :
                # 模型的結果給dp_sentence
            if ner_finded_times['TIME'] > 0 :
                dp_sentence = f"訂位服務，{ ner_not_finded[ 'TIME' ][0] }  時間不符合標準"
                self.ask_time_times = 0
            elif self.ask_time_times == 0 :
                dp_sentence = '訂位服務，詢問使用者時間資訊'
                self.ask_time_times = self.ask_time_times + 1 
            elif self.ask_time_times > 0 :
                dp_sentence = '訂位服務，再次詢問使用者時間資訊'
                self.ask_time_times = self.ask_time_times + 1 

            return dp_sentence
        
        dp_sentence = "訂位服務，準備執行"
        self.ask_store_times = 0
        self.ask_people_times = 0
        self.ask_time_times = 0
        self.ask_date_times = 0

        return dp_sentence


    def Clear_Ask_Times( self, nlu_type ) : #清除 chatbot詢問該ner的次數(該ner為空的次數)
        if nlu_type == '導航' :
            self.ask_address_times = 0
        elif nlu_type == '詢問':
            self.ask_store_times = 0
        elif nlu_type == '推薦' :
            self.ask_food_times = 0
        elif nlu_type == '訂位' :   
            self.ask_store_times = 0
            self.ask_people_times = 0
            self.ask_time_times = 0
            self.ask_date_times = 0

    def Clear_Record_Ask_Times_and_Finded_Times_and_Not_Finded( self, global_cp, nlu_type ) : # 清除 在ner_table找到的次數 和 在ner table中找不到的ner詞
        if nlu_type == "導航" :
            global_cp.Clear_Ner_Finded_Times( 'ADDRESS' )
            global_cp.Clear_Ner_Not_Finded( 'ADDRESS' )
            self.Clear_Ask_Times( '導航' )
        elif nlu_type == "詢問" :

            global_cp.Clear_Ner_Finded_Times( 'STORE' )
            global_cp.Clear_Ner_Not_Finded( 'STORE' )

            self.Clear_Ask_Times( '詢問' )
        elif nlu_type == "推薦" :
            global_cp.Clear_Ner_Finded_Times( 'FOOD' )
            global_cp.Clear_Ner_Not_Finded( 'FOOD' )

            global_cp.Clear_Ner_Finded_Times( 'ADJ' )
            global_cp.Clear_Ner_Not_Finded( 'ADJ' )

            self.Clear_Ask_Times( '推薦' )
        elif nlu_type == "訂位" :

            global_cp.Clear_Ner_Finded_Times( 'STORE' )
            global_cp.Clear_Ner_Not_Finded( 'STORE' )

            global_cp.Clear_Ner_Finded_Times( 'TIME' )
            global_cp.Clear_Ner_Not_Finded( 'TIME' )

            global_cp.Clear_Ner_Finded_Times( 'TIME2' )
            global_cp.Clear_Ner_Not_Finded( 'TIME2' )

            global_cp.Clear_Ner_Finded_Times( 'DATE' )
            global_cp.Clear_Ner_Not_Finded( 'DATE' )

            global_cp.Clear_Ner_Finded_Times( 'PEOPLE' )
            global_cp.Clear_Ner_Not_Finded( 'PEOPLE' )

     
            self.Clear_Ask_Times( '訂位' )


    def Choose_Dp( self, nlu_type, ner_result, ner_finded_times, ner_not_finded ) :
        dp_sentence = ""
        print( "DP中的ner: ", end="")
        print( ner_result )
        if nlu_type == "導航" :
            dp_sentence = self.Choose_Map_Dp( ner_result, ner_finded_times, ner_not_finded ) 
        elif nlu_type == "詢問" :
            dp_sentence = self.Choose_Ask_Dp( ner_result, ner_finded_times, ner_not_finded ) 
        elif nlu_type == "推薦" :
            dp_sentence = self.Choose_Recommand_Dp( ner_result, ner_finded_times, ner_not_finded ) 
        elif nlu_type == "訂位" :
            dp_sentence = self.Choose_Reserve_Dp( ner_result, ner_finded_times, ner_not_finded ) 
        else :
            dp_sentence = ""

        return dp_sentence


global_dp = Dp()

    





# <導航>
# 導航服務，詢問使用者要去的地方
# 導航服務，再次詢問使用者要去的地方
# 導航服務，找不到 [ 'ADDRESS' ]  此地址
# 導航服務，準備執行
# <G>

# <詢問>
# 詢問店家服務，詢問使用者地區資訊
# 詢問店家服務，再次詢問使用者地區資訊
# 詢問店家服務，找不到 [ 'PLACE' ] 此地區
# 詢問店家服務，詢問使用者店家名稱資訊
# 詢問店家服務，再次詢問使用者店家名稱資訊
# 詢問店家服務，找不到 [ 'STORE' ]  此類似名稱的店家
# 詢問店家服務，準備執行
# <G>

# <訂位>
# 訂位服務，詢問使用者地區資訊
# 訂位服務，再次詢問使用者地區資訊
# 訂位服務，找不到 [ 'PLACE' ] 此地區"
# 訂位服務，詢問使用者店家名稱資訊
# 訂位服務，再次詢問使用者店家名稱資訊
# 訂位服務，找不到 [ 'STORE' ] 此類似名稱的店家
# 訂位服務，詢問使用者人數資訊
# 訂位服務，再次詢問使用者人數資訊
# 訂位服務，[ 'People' ]  人數不符合標準
# 訂位服務，詢問使用者日期資訊
# 訂位服務，再次詢問使用者日期資訊
# 訂位服務，[ 'DATE' ] 日期不符合標準
# 訂位服務，詢問使用者時間資訊
# 訂位服務，詢問使用者時間資訊
# 訂位服務，[ 'TIME' ] 時間不符合標準
# 訂位服務，準備執行
# <G>


# <推薦>
# 推薦服務，詢問使用者是否可以提供食物類型或是形容詞
# 推薦服務，準備執行
# <G>

