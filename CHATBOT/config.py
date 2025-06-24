# config.py
# 集中管理所有模型、權重、資料、embedding、資料夾等路徑與常數

# NLU/分類模型
NLU_TOKENIZER = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
NLU_FUNCTION_MODEL = "./new_result/checkpoint-3000"  # 更新為實際使用的路徑
NLU_COLLECT_MODEL = "./Is_Collect_or_Function/checkpoint-3000"


# NER/Spacy模型
SPACY_TIME_MODEL = "./output/model_time4"
SPACY_STORE_MODEL = "./output/model_store5"
SPACY_FOOD_MODEL = "./output/model_food5"
SPACY_ALL_MODEL = "./output1/model-best"
SPACY_DIA_RESERVE = "./output2_dia_reserve/model-best"
SPACY_DIA_RECOMMAND = "./output2_dia_recommand/model-best"
SPACY_DIA_MAP = "./output2_dia_map/model-best"

# NLG/聊天模型
NLG_MODEL_PATH = "./NLG_TAIDE/model/TAIDE_DP_3(詢問+訂位功能)"
NLG_ADAPTER_PATH = "./NLG_TAIDE/checkpoint/TAIDE_DP_4(詢問+訂位功能)_checkpoint/checkpoint-9300"

# Embedding
EMBEDDING_MODEL = "lier007/xiaobu-embedding-v2"
TEXT2VEC_MODEL = "./shibing624_text2vec-base-chinese"

# 資料檔案
DATA_JSON = "./data.json"
STOREINFO_JSON = "./storeinfo_review.json"
TAG_EMBEDDINGS_JSON = "./tag_embeddings.json"
UPDATED_STOREINFO_JSON = "./updated_storeinfo_tablesm.json"


# 環境變數檔案
ENV_API_KEY_FILE = "env_api_key.env" 