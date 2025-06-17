import numpy as np
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer
from Levenshtein import distance as levenshtein_distance
import traceback

from database import*


class Comapare_Similiar:

    def __init__( self, table ):
        self.table = table 
        self.ner_finded_times = { "ADDRESS":0, "TIME":0, "TIME2":0, "FOOD":0, "DATE":0, "ADJ":0, "STORE":0, "PEOPLE":0, "PLACE":0 }
        self.ner_not_finded = { "ADDRESS":[],  "TIME":[], "TIME2":[], "FOOD":[], "DATE":[], "ADJ":[], "STORE":[], "PEOPLE":[], "PLACE":[] }
        

    def jaccard_similarity( self, str1, str2 ):
        # 将字符串转换为字符集
        set1 = set(str1)
        set2 = set(str2)
        
        # 计算 Jaccard 相似度
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0

    def combined_similarity( self, str1, str2, alpha=0.5 ):
        jaccard_sim = self.jaccard_similarity(str1, str2)
        levenshtein_dist = levenshtein_distance(str1, str2)
        
        # 归一化 Levenshtein 距离
        max_len = max(len(str1), len(str2))
        levenshtein_sim = 1 - (levenshtein_dist / max_len) if max_len > 0 else 0
        
        # 结合两种相似度
        return alpha * jaccard_sim + (1 - alpha) * levenshtein_sim

    def Search_Similar( self, value, ner_type ) :


        # 檢查 ner_type 是否存在於 self.table 中
        if ner_type not in self.table:
            print(f"(Search_Similar Warning): '{ner_type}' not found in table. Returning default value.")
            return ""  # 或返回一個適當的預設值

        
        most_similar = None
        highest_score = -1

        for target_value in self.table[ ner_type ]:
            score = self.combined_similarity( value, target_value )
            self.Add_Ner_Finded_Times( ner_type )   # 紀錄 ner 的搜尋次數

            # print(f"Similarity between '{value}' and '{target_value}': {score:.4f}")
            
            if score > highest_score:
                highest_score = score
                most_similar = target_value

    

        print(f"(Search_Similar) The most similar value to '{value}' is: '{most_similar}' with a score of {highest_score:.4f}")

        if highest_score > 0.3:
            return most_similar
        else :
            self.Add_Ner_Not_Finded( ner_type, value )
            return ""

    
    def Search_Similar_And_Let_User_Choose( self, value, ner_type ) :

        if not value:
            print("(Search_Similar_And_Let_User_Choose) Warning: 'value' is empty.")
            return ""
        maybe_ner = []
        most_similar = None
        temp_score = 0.3

        for target_value in self.table[ ner_type ]:
            score = self.combined_similarity( value, target_value )
            self.Add_Ner_Finded_Times( ner_type )   # 紀錄 ner 的搜尋次數

            # print(f"Similarity between '{value}' and '{target_value}': {score:.4f}")
            
            if score > temp_score:
                maybe_ner.append( target_value )

        return maybe_ner

    def Add_Ner_Not_Finded( self, ner_type, value ) :
        self.ner_not_finded[ ner_type ].append( value )

    def Clear_Ner_Not_Finded( self, ner_type ) :
        self.ner_not_finded[ ner_type ] = []

    def Get_Ner_Not_Finded( self ) :
        return self.ner_not_finded

    def Add_Ner_Finded_Times( self, ner_type ) :
        self.ner_finded_times[ ner_type ] = self.ner_finded_times[ ner_type ] + 1


    def Clear_Ner_Finded_Times( self, ner_type ) :
         self.ner_finded_times[ ner_type ] = 0 

    def Get_Ner_Finded_Times( self ) :
        return self.ner_finded_times


    def Find_Store_Review( self, store_name ) :
        return global_db.FindReview_Store_Table( store_name )

    def Find_Store_Address( self, store_name ) :
        return global_db.FindAddress_Store_Table( store_name )

# db = DataBase( )

# cp = Comapare_Similiar( db.Get_WordTable( ) )

# cp.Search_Similar( "燒臘", 'store' )

global_cp = Comapare_Similiar( global_db.Get_WordTable( )  )