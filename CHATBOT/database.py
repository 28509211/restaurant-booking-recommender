# import mysql.connector
# from mysql.connector import Error
import json
import os
from config import DATA_JSON, STOREINFO_JSON

def read_dict_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_dict_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class DataBase :

    def __init__( self ):

        # self.connection = mysql.connector.connect(
        #         host='0.tcp.jp.ngrok.io',
        #         port=13672,  # NGROK 提供的端口
        #         user='tim',
        #         password='11027102',
        #         database='clientdatabase'
        # )

        # self.cursor = self.connection.cursor()
        # self.word_table = self.See_Data_In_Table( 'food_data' )

        #======================================================================================
        self.word_table = read_dict_from_file( DATA_JSON )
        self.store_table = read_dict_from_file( STOREINFO_JSON )
        


    def See_Table( self ) :  #看有甚麼table
        query =  'SHOW TABLES' 
        self.cursor.execute( query )
        table = self.cursor.fetchall()

        for i in table :
            print( i )


    def See_Data_In_Table( self, table_name ) :
  
        query = f'SELECT * FROM {table_name}'
        self.cursor.execute(query)

        # 获取列名
        column_names = [desc[0] for desc in self.cursor.description]
        print("Column names:", column_names)

        # 获取查询结果
        rows = self.cursor.fetchall()

        # 创建一个字典以存储每列的数据
        column_data = {column: [] for column in column_names}

        # 遍历每一行，提取每列的数据
        for row in rows:
            for column_name, value in zip(column_names, row):
                if value != '' :
                    column_data[column_name].append(value)

        return column_data

    def Get_WordTable( self ) :  # 字典

        return self.word_table

    def Get_Store_ReviewTable( self ) :  # 字典

        return self.store_table

    def FindReview_Store_Table( self, store_name ) :  #找店家的評論
        review_folder = "review"

        for stores in self.store_table :
            if stores[ 'store_name' ] == store_name :
                file_name = f"{stores[ 'store_name' ]}_review.txt"
                file_path = os.path.join(review_folder, file_name)

                if not os.path.isfile(file_path):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(stores['reviews'])

                    return f"./review/{stores[ 'store_name' ]}_review.txt"
                else :
                    return f"./review/{stores[ 'store_name' ]}_review.txt"


    def FindAddress_Store_Table( self, store_name ) :  #找店家的地址
        for stores in self.store_table :
            if stores[ 'store_name' ] == store_name :       
                return stores['location']
        
        return ""

       

global_db = DataBase()


