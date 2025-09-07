# app.py (RECOMMENDATION SYSTEM MAIN FILE)
import os
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

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat1 - lat2
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def load_db_config():
    # 由 docker-compose 傳入
    return {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT'))
    }

def get_data_from_mysql(host, user, password, database, port):
    connection = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    query = "SELECT * FROM storeinfo_table"
    data = pd.read_sql_query(query, connection)

    data = data[data['tag'].notnull()]
    data['tag'] = data['tag'].apply(lambda x: x.strip().split(','))

    data_list = []
    for _, row in data.iterrows():
        store_id = row['store_id']
        store_hours = get_store_hours(store_id, connection)
        url = get_store_url(store_id, connection)
        row_data = row.to_dict()
        row_data['store_hours'] = store_hours
        row_data['url'] = url
        data_list.append(row_data)

    connection.close()
    return data_list

def get_store_hours(store_id, connection):
    query = "SELECT day_of_week, open_time_1, close_time_1, open_time_2, close_time_2 FROM openhours WHERE store_id = %s"
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(query, (store_id,))
        hours = cursor.fetchall()
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
    query = f"SELECT initselect FROM preferences_table WHERE client_id = '{client_id}'"
    data = pd.read_sql_query(query, engine)
    preferences = data['initselect'].tolist()
    return preferences

def recommend_restaurants_based_on_preferences(data, user_tags_list):
    tags = [' '.join(item["tag"]) for item in data]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(tags)
    user_tags = ' '.join(user_tags_list)
    user_tfidf = vectorizer.transform([user_tags])
    cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    for idx, item in enumerate(data):
        item['similarity'] = float(cosine_similarities[idx])  # 確保可 JSON 序列化
    return data

def filter_restaurants_by_distance(data, user_lat, user_lon, max_distance):
    out = []
    for item in data:
        distance = haversine(user_lon, user_lat, item["longitude"], item["latitude"])
        if distance <= max_distance:
            item['distance'] = float(distance)
            out.append(item)
    return out

def sort_restaurants(data):
    return sorted(
        data,
        key=lambda x: (-x.get('similarity', 0.0),
                       x.get('distance', float('inf')),
                      -x.get('review_count', 0),
                      -x.get('average_rating', 0.0))
    )

def recommandation_with_tags(user_tags_list, db_config, mode, user_lat=None, user_lon=None, max_distance=None):
    data = get_data_from_mysql(db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])
    returnlist = []

    if mode == "基本":
        recommendations = recommend_restaurants_based_on_preferences(data, user_tags_list)
        recommendations = sort_restaurants(recommendations)
        for item in recommendations[:5]:
            returnlist.append({
                "store_id": item["store_id"],
                "store_name": item["store_name"],
                "category": item["category"],
                "address": item["address"],
                "service": item["service"],
                "ratings": item.get("ratings"),
                "store_hours": item.get("store_hours", []),
                "url": item.get("url", "")
            })

    elif mode == "距離過濾2":
        if user_lat is None or user_lon is None or max_distance is None:
            return [{"error": "user_lat/user_lon/max_distance required"}]
        filtered = filter_restaurants_by_distance(data, user_lat, user_lon, max_distance)
        recommendations = sort_restaurants(filtered)
        for item in recommendations[:10]:
            returnlist.append({
                "store_id": item["store_id"],
                "store_name": item["store_name"],
                "category": item["category"],
                "address": item["address"],
                "service": item["service"],
                "ratings": item.get("ratings"),
                "store_hours": item.get("store_hours", []),
                "url": item.get("url", "")
            })
    else:
        returnlist.append({"error": "Invalid input. Give up."})

    return returnlist

@app.route('/healthz')
def healthz():
    return jsonify({"ok": True})

@app.route('/recommend2', methods=['POST'])
def recommend():
    request_data = request.get_json(force=True, silent=True) or {}
    client_id = request_data.get('client_id')
    if not client_id:
        return jsonify({"error": "client_id required"}), 400

    db_config = load_db_config()

    user_lat = 25.0330
    user_lon = 121.5654
    max_distance = 15

    user_tags_list = get_user_preferences(client_id, db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])
    app.logger.info("使用者選擇的標籤: %s", user_tags_list)

    rec_basic = recommandation_with_tags(user_tags_list, db_config, "基本")
    rec_dist  = recommandation_with_tags(user_tags_list, db_config, "距離過濾2", user_lat, user_lon, max_distance)

    return jsonify({
        "recommendations_basic": rec_basic,
        "recommendations_distance": rec_dist
    })

if __name__ == '__main__':
    FLASK_HOST = os.getenv('FLASK_HOST')
    FLASK_PORT = int(os.getenv('FLASK_PORT'))
    app.run(host=FLASK_HOST, port=FLASK_PORT)
