import json
import numpy as np
import pymysql
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from math import radians, cos, sin, asin, sqrt
from flask import Flask, request, jsonify
import logging
from sqlalchemy import create_engine
from datetime import timedelta

app = Flask(__name__)

# 設定日誌級別
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 计算两个经纬度点之间的距离
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat1 - lat2
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r


# 修改 get_data_from_mysql 函数，将所有数据的时间字段转换为字符串
def get_data_from_mysql(host, user, password, database, port):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )

    # 主查询
    query = "SELECT * FROM storeinfo_table"
    data = pd.read_sql_query(query, connection)

    # 清理数据
    data = data[data['tag'].notnull()]
    data['tag'] = data['tag'].apply(lambda x: x.strip().split(','))

    # 逐行添加 store_hours 和 url
    data_list = []
    for _, row in data.iterrows():
        store_id = row['store_id']
        store_hours = get_store_hours(store_id, connection)
        url = get_store_url(store_id, connection)
        row_data = row.to_dict()
        row_data['store_hours'] = store_hours
        row_data['url'] = url
        data_list.append(row_data)

    # 关闭连接
    connection.close()

    return data_list

# 修改 get_store_hours 函数，将时间字段转换为字符串
def get_store_hours(store_id, connection):
    query = "SELECT day_of_week, open_time_1, close_time_1, open_time_2, close_time_2 FROM openhours WHERE store_id = %s"
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(query, (store_id,))
        hours = cursor.fetchall()
        # 将时间字段转换为字符串
        for row in hours:
            row["open_time_1"] = str(row["open_time_1"]) if row["open_time_1"] else ""
            row["close_time_1"] = str(row["close_time_1"]) if row["close_time_1"] else ""
            row["open_time_2"] = str(row["open_time_2"]) if row["open_time_2"] else ""
            row["close_time_2"] = str(row["close_time_2"]) if row["close_time_2"] else ""
        return hours

def get_store_url(store_id, connection):
    query = "SELECT url FROM store_urls WHERE store_id = %s"
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(query, (store_id,))
        result = cursor.fetchone()
        return result["url"] if result else ""

    
def get_user_preferences(client_id, host, user, password, database, port):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    query = f"""
    SELECT initselect FROM preferences_table WHERE client_id = '{client_id}'
    """
    data = pd.read_sql_query(query, engine)
    preferences = data['initselect'].tolist()
    return preferences

# 从文件中读取JSON数据
def read_data_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# 基于用户偏好的标签推荐餐厅
def recommend_restaurants_based_on_preferences(data, user_tags_list):
    tags = [' '.join(item["tag"]) for item in data]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(tags)

    # 計算稀疏度
    total_elements = tfidf_matrix.shape[0] * tfidf_matrix.shape[1]
    nonzero_elements = tfidf_matrix.nnz
    sparsity = 1 - (nonzero_elements / total_elements)
    print("矩陣的稀疏度:", sparsity)
    
    user_tags = ' '.join(user_tags_list)
    user_tfidf = vectorizer.transform([user_tags])
    cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    for idx, item in enumerate(data):
        item['similarity'] = cosine_similarities[idx]
    return data


# 过滤掉不在指定距离内的餐厅
def filter_restaurants_by_distance(data, user_lat, user_lon, max_distance):
    filtered_restaurants = []
    for item in data:
        restaurant_lat = item["latitude"]
        restaurant_lon = item["longitude"]
        distance = haversine(user_lon, user_lat, restaurant_lon, restaurant_lat)
        if distance <= max_distance:
            item['distance'] = distance  # 临时添加距离信息，用于后续排序
            filtered_restaurants.append(item)
    return filtered_restaurants


def sort_restaurants(data):
    # Sort by similarity, then by distance, then by popularity
    return sorted(data, key=lambda x: (
    -x.get('similarity', 0), x.get('distance', float('inf')), -x.get('review_count', 0), -x.get('average_rating', 0)))

user_mode = "基本"
def sort_by_reviews_and_ratings(data):
    return sorted(data, key=lambda x: (-x.get('review_count', 0), -x.get('average_rating', 0)))


# def recommandation_with_tags(user_tags_list, db_config, mode=user_mode, user_lat=None, user_lon=None, max_distance=None):
#     data = get_data_from_mysql(db_config['host'], db_config['user'], db_config['password'],
#                                db_config['database'], db_config['port'])
#     if mode == "基本":
#         recommendations = recommend_restaurants_based_on_preferences(data, user_tags_list)
#         recommendations = sort_restaurants(recommendations)
#         return [item["store_id"] for item in recommendations[:5]]
#     elif mode == "距離過濾2":
#         if user_lat is None or user_lon is None or max_distance is None:
#             raise ValueError("user_lat, user_lon and max_distance are required for distance filtering")
#         filtered_restaurants = filter_restaurants_by_distance(data, user_lat, user_lon, max_distance)
#         recommendations = sort_by_reviews_and_ratings(filtered_restaurants)
#         return [item["store_id"] for item in recommendations[:10]]
#     else:
#         return ["Invalid input."]


def recommandation_with_tags(user_tags_list, db_config, mode, user_lat=None, user_lon=None, max_distance=None):
    data = get_data_from_mysql(db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])
    returnlist = []
    
    if mode == "基本":
        recommendations = recommend_restaurants_based_on_preferences(data, user_tags_list)
        recommendations = sort_restaurants(recommendations)
        
        # 顯示所有推薦的 store_id
        store_ids = [item["store_id"] for item in recommendations[:5]]
        print("基本模式推薦的店家 IDs:", store_ids)
        
        for item in recommendations[:5]:
            returnlist.append({
                "store_id": item["store_id"],
                "store_name": item["store_name"],
                "category": item["category"],
                "address": item["address"],
                "service": item["service"],
                "ratings": item["ratings"],
                "store_hours": item.get("store_hours", []),
                "url": item.get("url", "")
            })

    elif mode == "距離過濾2":
        if user_lat is None or user_lon is None or max_distance is None:
            raise ValueError("user_lat, user_lon and max_distance are required for distance filtering")
        
        filtered_restaurants = filter_restaurants_by_distance(data, user_lat, user_lon, max_distance)
        recommendations = sort_restaurants(filtered_restaurants)
        
        # 顯示所有推薦的 store_id
        store_ids = [item["store_id"] for item in recommendations[:10]]
        print("距離過濾2模式推薦的店家 IDs:", store_ids)
        
        for item in recommendations[:10]:
            returnlist.append({
                "store_id": item["store_id"],
                "store_name": item["store_name"],
                "category": item["category"],
                "address": item["address"],
                "service": item["service"],
                "ratings": item["ratings"],
                "store_hours": item.get("store_hours", []),
                "url": item.get("url", "")
            })

    else:
        returnlist.append({"error": "Invalid input. Give up."})

    return returnlist

# 建立推薦API
@app.route('/recommend2', methods=['POST'])
def recommend():
    request_data = request.get_json()
    client_id = request_data.get('client_id')
    
    # 預設的地理位置和篩選距離
    user_lat = 25.0330
    user_lon = 121.5654
    max_distance = 15
    
    # 獲取使用者偏好標籤
    user_tags_list = get_user_preferences(client_id, db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])
    
    logger.info("使用者選擇的標籤: %s", user_tags_list)
    
    # 執行基本模式並在 Python 端顯示結果
    recommendations_basic = recommandation_with_tags(user_tags_list, db_config, "基本")
    basic_ids = [item["store_id"] for item in recommendations_basic]
    print("基本模式推薦的店家 IDs:", basic_ids)
    
    # 執行距離過濾2模式並在 Python 端顯示結果
    recommendations_distance = recommandation_with_tags(user_tags_list, db_config, "距離過濾2", user_lat, user_lon, max_distance)
    distance_ids = [item["store_id"] for item in recommendations_distance]
    print("距離過濾2模式推薦的店家 IDs:", distance_ids)
    
    # API 只返回距離過濾2模式的推薦結果
    # API 返回基本模式和距離過濾2模式的推薦結果
    return jsonify({
        "recommendations_basic": recommendations_basic,
        "recommendations_distance": recommendations_distance
    })



if __name__ == '__main__':
    db_config = {
        'host': 'X',
        'user': 'X',
        'password': 'X',
        'database': 'X',
        'port': X
    }
    app.run(host='0.0.0.0', port=5001)
