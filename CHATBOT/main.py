from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
import threading
from transformers import AutoTokenizer, AutoModelForCausalLM
from uuid import uuid4
import torch
from engineio.async_drivers import gevent
from user_information import*
from multiprocessing import Process, Manager, Queue
import time 
from pyngrok import ngrok
from spacy_function import NER  # 匯入 Place_Answer_InLabel
import socket

app = Flask(__name__)
socketio = SocketIO( app, async_mode='gevent', cors_allowed_origins="*" )


user_rooms = {}  # 紀錄user登陸網站的編碼


def send_messages_from_queue(message_queu, socketio):   #存queue中抓第一個訊息傳送到window上
    while True:
        if not message_queue.empty():
            message, room_id = message_queue.get()
            socketio.emit('message', message, room=room_id)   # 傳訊息到 server          
        time.sleep(0.1) 




@socketio.on('selected_restaurant')
def handle_selected_restaurant( data ):
    user_sid = request.sid
    room_id = user_rooms.get(user_sid)

    selected_restaurant = data.get("selected_restaurant")
    print(f"User in room {room_id} selected restaurant: {selected_restaurant}")
    
    # 檢查是否包含 selected_restaurant 並提取店名
    if data and "selected_restaurant" in data:
        selected_restaurant_full = data.get("selected_restaurant")
        print(f"Full message from Android: {selected_restaurant_full}")
        
        # 去掉 "選擇的餐廳是：" 並保留後面的店名
        selected_restaurant = selected_restaurant_full.replace("選擇的餐廳是：", "").strip()
        print(f"Parsed restaurant name: {selected_restaurant}")

    global shared_usechatbot
    shared_usechatbot[room_id] = [True, selected_restaurant, True, True]
    
    # 傳送確認消息回給 Android 客戶端
    socketio.emit("message", f"已確認選擇的店家：{selected_restaurant}", room=room_id)


user_data = {}  # 用於存儲每個房間的使用者資訊

@socketio.on('user_info')
def handle_user_info(data):
    user_sid = request.sid
    room_id = user_rooms.get(user_sid)
    username = data.get('username', '')
    gender = data.get('gender', '')
    
    # 儲存資料到 user_data 中
    user_data[room_id] = {"username": username, "gender": gender}
    print(f"Received user info for room {room_id}: Name={username}, Gender={gender}")
    print(f"Current user_data: {user_data}")
    
    


def Chatbot( room_id, shared_usechatbot, message_queue ) :
    user = User()  # 嘗試初始化 User

    print( "USER DATA !!!!!", user_data )
    DO_FUNCTION = False
    ASK_QUESTION = False

    nlu_last = "聊天"
    nlu_result = "聊天"

    socketio.emit('message', "準備完畢......", room=room_id)   # 傳訊息到 server      
    print( "--------------------------------------Model ok------------------------------------")

    while shared_usechatbot[room_id][2]:
        if shared_usechatbot[room_id][0] :  # 接收到使用者訊息
            

            message = shared_usechatbot[room_id][1]   # user talk
            shared_usechatbot[room_id] = [False, "", True, shared_usechatbot[room_id][3]]

            if ASK_QUESTION :
                if message == "0" :
                    ASK_QUESTION = False 
                    user.Clear_Ner( "ask" )
                    message_queue.put(["結束詢問模式", room_id])   # chatbot talk( 把nlg透露在網站上 )
                    shared_usechatbot[room_id] = [False, "", True, False]
                else :
                    review_path = global_cp.Find_Store_Review( user.User_Get_Ner_Label_Data( "ASK_STORE" ) )  #找到store的評論並寫入test_review.txt
                    question = message
                    answer = user.Use_Ask_Question( question, review_path)
                    message_queue.put([answer, room_id])   # chatbot talk( 把nlg透露在網站上 )
                    shared_usechatbot[room_id] = [ False, "", True, False]
            else :

                if shared_usechatbot[room_id][3] == True:
                    user.Replace_Ner( message, "STORE")
                    address = global_cp.Find_Store_Address( user.User_Get_Ner_Label_Data( "STORE" )  )
                    user.Replace_Ner( address, "ADDRESS" )
                else:
                    
                    # ==========Multi Label NLU Predict==========
                    nlu_last = nlu_result #更新 nlu_last
                    nlu_result = user.Use_NLU( message, debug=False )  # nlu 判別
                    nlu_message = "NLU PREDICT: " + str( nlu_result )
                    print( nlu_message )


                    if nlu_last != nlu_result :       # 若前一次使用的功能和現在使用的不一樣(意圖轉換) 清除紀錄(為了選擇較正確的dp)
                        global_dp.Clear_Record_Ask_Times_and_Finded_Times_and_Not_Finded( global_cp,  nlu_last )
                        user.Clear_History()  # 清除對話紀錄資訊
                        user.Set_Input( message ) #把這次偵測到的新功能的句子重新新增到history 


                    # ==========NER Predict==========
                    ner_result = user.Use_NER( message, nlu_result, debug= False ) # ner判別, user talk 已記錄在對話歷史中
                    ner_message = "NER PREDICT: " + str( ner_result )
                    print( ner_message )

                
                    
                    print( "history: ", end="" )
                    print( user.Get_History_Input() )


                    store_value = ner_result.get("STORE", "")
                    if store_value:
                        maybe_store_list = store_value.split("、")  # 分割多個店名
                        print("找到的店名列表:", maybe_store_list)
                        
                        if len(maybe_store_list) > 1:  # 如果有多個店名
                            # 發送多店名列表給 Android 端進行選擇
                            socketio.emit('restaurant_list', {"restaurants": maybe_store_list}, room=room_id)
                            print("Multiple restaurants sent to user for selection:", maybe_store_list)
                        else:
                            # 單一店名情況，直接處理
                            selected_store = maybe_store_list[0]
                            print(f"Single store found and selected: {selected_store}")
                            # 你可以直接設置選定的店家到 ner_result
                            user.Replace_Ner(selected_store, "STORE")
                            address = global_cp.Find_Store_Address( user.User_Get_Ner_Label_Data( "STORE" )  )
                            user.Replace_Ner( address, "ADDRESS" )

                        
                
                    
                    # ==========DP Choose==========            
                    dp_sentence = user.Use_Dp( nlu_result ) # dp 判別


                    if "準備執行" in dp_sentence :
                        user.Clear_History()  # 清除對話紀錄資訊
                        global_dp.Clear_Record_Ask_Times_and_Finded_Times_and_Not_Finded( global_cp,  nlu_last )
                        DO_FUNCTION = True   # 已收集完該功能的 NER準備要執行該功能
                    
                    if nlu_result == "聊天" :
                        answer =  user.Use_NLG_Chat( message )
                    else :
                        print( "dp -> dialogue: " + dp_sentence )
                        answer =  user.Use_NLG_Chat( dp_sentence, dp_mode=True )

                    message_queue.put([answer, room_id])   # chatbot talk( 把nlg透露在網站上 )
                    shared_usechatbot[room_id] = [False, "", True, False]
                    
                    
                    if DO_FUNCTION :
                        if nlu_result == "推薦" :
                            store_rec_list = user.Use_Recommand( user.User_Get_Ner_Food_Adj_MergeList() )
                            if len(store_rec_list) > 1:  # 如果有多個店名
                            # 發送多店名列表給 Android 端進行選擇
                                socketio.emit('restaurant_list', {"restaurants": store_rec_list}, room=room_id)
                                print("Multiple restaurants sent to user for selection:", store_rec_list)
                                
                            user.Clear_Ner( "recommand" )
                        elif nlu_result == "導航":
                            user.Use_Map( address, room_id, message_queue, socketio )
                            user.Clear_Ner( "map" )
                        elif nlu_result == "訂位":
                            print( "USER DATA !!!!!", user_data )
                            # 從 user_data 中提取對應房間的使用者資料
                            user_info = user_data.get(room_id, {"username": "未知", "gender": "未知" })
                            username = user_info.get("username", "未知")
                            gender = user_info.get("gender", "未知")
                            print( "IN CHATBOT FUNCTION名稱和性別: ", username, gender)
                            # 更新 user_reserve_information
                            user_reserve_information = {
                                "username": username,
                                "date": user.User_Get_Ner_Label_Data( 'DATE' ),
                                "time": user.User_Get_Ner_Label_Data( 'TIME2' ) + user.User_Get_Ner_Label_Data( 'TIME' ),
                                "people": user.User_Get_Ner_Label_Data( 'PEOPLE' ),
                                "gender": gender
                            }
                            user.Use_NLG_Reserve( user_reserve_information )
                            user.Clear_Ner( "reserve" )

                        elif nlu_result == "詢問":
                            ASK_QUESTION = True
                            answer =  user.Use_NLG_Chat( "詢問店家服務，詢問使用者要詢問的問題", dp_mode=True )
                            message_queue.put([f"你好像有問題想詢問 開啟詢問模式\n{answer}", room_id])   # chatbot talk( 把nlg透露在網站上 )
                            shared_usechatbot[room_id] = [False, "", True, False]
                            
                        DO_FUNCTION = False
                        user.Delete_Executed_Task()   # 刪除在stack中已執行完畢的任務    
                    else:
                        user.Set_Input( answer, BOT=True ) # chatbot talk( 紀錄 )


                       












@app.route('/')
def index():
    return render_template('index.html')






@socketio.on('connect') 
def handle_connect():
    new_user = request.sid
    room_id = str(uuid4())
    user_rooms[new_user] = room_id
    join_room(room_id)
    print(f"New room created: {room_id}")
    print(user_rooms)

    global shared_usechatbot
    # 確保在初始化時只創建一個 User 實例
    if room_id not in shared_usechatbot:
        shared_usechatbot[room_id] = [False, "", True, False]  # 初始化 User 實例

    # 啟動 Chatbot
    a = threading.Thread(target=Chatbot, args=(room_id, shared_usechatbot, message_queue ))
    a.start()


@socketio.on( 'disconnect' ) 
def handle_disconnect():
    global shared_usechatbot

    user_name = request.sid
    if user_name in user_rooms:
        room_id = user_rooms[ user_name ]
        print("==========================DISCONNECT==================================")

        shared_usechatbot[room_id] = [False, "", False, False]


        shared_usechatbot.pop(room_id)
        leave_room( room_id ) 
        del user_rooms[ user_name ]  


@socketio.on( 'message' )
def handle_message( message ):
    user_name = request.sid  
    room_id = user_rooms.get( user_name )
    print( f"Message received from room {room_id}: {message}" )

    global shared_usechatbot
    
    # 檢查是否包含 "選擇的餐廳是：" 前綴
    if "選擇的餐廳是：" in message:
        # 去掉前綴並保留店名部分
        selected_restaurant = message.replace("選擇的餐廳是：", "").strip()
        print(f"Parsed restaurant name: {selected_restaurant}")

        # 更新選擇的店家到 ner_result
        shared_usechatbot[room_id] = [True, selected_restaurant, True, True]

        # 傳送確認消息回給 Android 客戶端
        # socketio.emit("message", f"已確認選擇的店家：{selected_restaurant}", room=room_id)
    else:
        # 處理一般訊息
        shared_usechatbot[room_id] = [True, message, True, False]
        
        # 日誌輸出確認 shared_usechatbot 是否正確寫入
        print(f"Updated shared_usechatbot[{room_id}] to: {shared_usechatbot[room_id]}")
        

    

def get_local_ips(port=5000):
    urls = [f"http://127.0.0.1:{port}"]
    return urls


def run_server():
    print("----------------RUN SERVER-----------------")
    urls = get_local_ips(port=5000)
    print("✅ 你可以用以下網址訪問伺服器：")
    for url in urls:
        print("👉", url)
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    print("Current async mode:", socketio.async_mode)
    manager = Manager()
    message_queue = Queue()  # 每個process傳送的訊息會到這裡，然後server會從最前面的開始把資料傳到網站上
    shared_usechatbot = manager.dict()
    
    send_thread = threading.Thread(target=send_messages_from_queue, args=(message_queue, socketio))
    send_thread.start()

    run_server()