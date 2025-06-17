<<<<<<< HEAD
# Restaurant Booking Recommender System
# 智能餐廳訂位推薦系統

一個完整的智能餐廳訂位推薦系統，整合了聊天機器人、數據收集、機器學習訓練和數據處理等多個模組，提供從數據收集到智能推薦的全流程解決方案。

## 🌟 專案特色

- **🤖 智能聊天機器人**: 基於深度學習的對話系統，支援餐廳推薦、訂位、評論查詢
- **🗺️ 自動化數據收集**: 從Google Maps自動收集餐廳資訊、圖片、評論
- **🧠 機器學習模型**: 多標籤分類、二分類、LLaMA-3微調等多種模型
- **📊 數據處理管道**: 完整的數據清洗、格式轉換、訓練數據生成流程
- **🔧 模組化設計**: 各功能模組獨立，易於維護和擴展

## 📁 專案結構

```
restaurant-booking-recommender/
├── CHATBOT/                    # 智能聊天機器人核心模組
│   ├── main.py                # Flask + SocketIO 主伺服器
│   ├── chat_function.py       # 對話生成與API串接
│   ├── classification_function.py  # NLU意圖分類
│   ├── spacy_function.py      # NER命名實體辨識
│   ├── dp_function.py         # 對話流程管理
│   ├── database.py            # 餐廳資料存取
│   ├── config.py              # 集中配置管理
│   ├── script.py              # 一鍵啟動腳本
│   └── requirements.txt       # 依賴套件
│
├── Search_data/               # 數據收集模組
│   └── Google_Map/           # Google Maps數據收集
│       ├── search_coordinate/     # 座標生成與比對
│       ├── search_store_Data/     # 店家基本資料爬蟲
│       ├── search_store_Picture/  # 店家圖片爬蟲
│       ├── search_store_Review/   # 店家評論爬蟲
│       └── search_store_with_google/  # Google API搜尋
│
├── Train/                     # 機器學習模型訓練
│   ├── NLU_BERT_MULTILABEL.ipynb      # 多標籤分類模型
│   ├── NLU_FOR_Binary.ipynb           # 二分類模型
│   └── Finetune_Llama3_with_LLaMA_Factory_ipynb  # LLaMA-3微調
│
└── Data/                      # 數據處理與管理
    ├── data_raw/              # 原始數據檔案
    ├── data_processed/        # 處理後JSON數據
    ├── scripts/               # 數據處理腳本
```

## 🚀 快速開始

### 1. 環境需求
- Python 3.8+
- 8GB+ RAM (推薦16GB)
- GPU支援 (用於模型訓練)

### 2. 安裝依賴
```bash
# 克隆專案
git clone <repository-url>
cd restaurant-booking-recommender

# 安裝聊天機器人依賴
cd CHATBOT
pip install -r requirements.txt

# 安裝數據收集依賴
cd ../Search_data/Google_Map
pip install -r requirements.txt

# 安裝數據處理依賴
cd ../../Data/scripts
pip install pandas numpy requests beautifulsoup4
```

### 3. 模型權重下載
請至 [Google Drive模型權重下載](https://drive.google.com/drive/folders/1xt2j6hwjhCDhpAqlXl1bVf1dRDx-EIxc?usp=sharing) 下載所有模型資料夾，並放置於對應目錄。

**必要模型目錄：**
- `CHATBOT/output/` - NER模型
- `CHATBOT/output2_dia_*/` - 對話模型
- `CHATBOT/new_result/` - NLU模型
- `CHATBOT/Is_Collect_or_Function/` - 收集分類模型
- `CHATBOT/NLG_TAIDE/` - NLG模型
- `CHATBOT/shibing624_text2vec-base-chinese/` - 文本向量模型

### 4. 啟動聊天機器人
```bash
cd CHATBOT
python script.py start
```

## 📋 使用指南

### 🤖 聊天機器人 (CHATBOT)

**主要功能：**
- 餐廳推薦與訂位協助
- 評論查詢與地圖導航
- 智能問答與多輪對話
- 用戶意圖識別與實體提取

**啟動方式：**
```bash
cd CHATBOT
python script.py start          # 基本啟動
python script.py start --debug  # 調試模式
python script.py start --external  # 外部訪問
```

**配置管理：**
- 所有路徑配置在 `config.py` 中統一管理
- API金鑰在 `.env` 文件中設定
- 詳細配置說明請參考 `CONFIG_SUMMARY.md`

### 🗺️ 數據收集 (Search_data)

**功能模組：**
- **座標生成**: 產生目標區域的經緯度座標
- **店家搜尋**: 使用Google API或爬蟲搜尋附近店家
- **資料收集**: 自動收集店家資訊、圖片、評論
- **批次處理**: 支援大量數據的批次處理

**使用流程：**
1. 使用 `search_coordinate` 產生目標區域座標
2. 使用 `search_store_with_google` 搜尋店家
3. 使用 `search_store_Data/Picture/Review` 收集詳細資料

**注意事項：**
- 請遵守Google Maps使用規範
- 建議使用虛擬環境
- 各模組皆有獨立README說明

### 🧠 模型訓練 (Train)

**訓練模型：**
- **多標籤分類**: 識別用戶意圖的多個標籤組合
- **二分類**: 針對特定功能進行精確分類
- **LLaMA-3微調**: 使用LoRA技術微調大語言模型

**執行順序：**
1. 先訓練基礎的二分類模型
2. 再訓練多標籤分類模型
3. 最後進行大語言模型微調

**環境需求：**
- GPU環境（推薦用於LLaMA-3微調）
- 充足的記憶體和儲存空間

### 📊 數據處理 (Data)

**數據流程：**
1. **原始數據** → 放在 `data_raw/`
2. **處理腳本** → 使用 `scripts/` 中的腳本
3. **處理結果** → 輸出到 `data_processed/`

**主要腳本：**
- `change_to_json.py`: 轉換為JSON格式
- `main_trans.py`: 主要翻譯處理
- `chat_traindata_alpach_format.py`: Alpaca格式轉換

**數據格式：**
- 原始格式：使用特殊標籤如 `<G>`, `<USER>`, `<LABEL>`, `<BOT>`
- JSON格式：標準化的對話數據格式
- Alpaca格式：適用於大語言模型微調

## 🔧 進階配置

### API金鑰設定
```bash
# 複製環境變數範本
cp CHATBOT/env_api_key.txt CHATBOT/.env

# 編輯.env文件，填入您的API金鑰
# - Google Maps API Key
# - OpenAI API Key (如需要)
# - 其他第三方服務API金鑰
```

### 模型參數調整
- **NLU模型**: 修改 `Train/` 中的notebook檔案
- **對話策略**: 修改 `CHATBOT/dp_function.py`
- **用戶管理**: 修改 `CHATBOT/user_information.py`

### 數據庫配置
- 餐廳資料：`CHATBOT/data.json`
- 評論資料：`CHATBOT/storeinfo_review.json`
- 標籤嵌入：`CHATBOT/tag_embeddings.json`

## 📈 性能優化

### 記憶體優化
- 使用4-bit量化模型
- 批次處理大量數據
- 定期清理暫存檔案

### 速度優化
- GPU加速模型推理
- 快取常用數據
- 並行處理多個請求

### 準確度提升
- 定期更新訓練數據
- 調整模型超參數
- 使用更先進的預訓練模型

## 🛠️ 開發指南

### 新增功能
1. 在對應模組中新增功能檔案
2. 更新配置檔案
3. 添加測試腳本
4. 更新文檔說明

### 除錯技巧
```bash
# 環境檢查
cd CHATBOT
python script.py setup

# 快速測試
python script.py test

# 查看狀態
python script.py status
```

### 測試流程
1. 單元測試：測試各功能模組
2. 整合測試：測試模組間互動
3. 端到端測試：測試完整流程

## 📝 常見問題

### 啟動問題
- **模型權重未下載**: 確保所有模型目錄存在
- **依賴套件缺失**: 執行 `python script.py setup`
- **API金鑰未設定**: 檢查 `.env` 文件

### 功能問題
- **詢問模式**: 輸入"0"可結束多輪詢問
- **路徑錯誤**: 檢查 `config.py` 中的路徑設定
- **模型載入失敗**: 確認模型文件完整性

### 性能問題
- **記憶體不足**: 使用量化模型或減少批次大小
- **速度慢**: 檢查GPU使用情況，考慮使用更快的模型
- **準確度低**: 增加訓練數據，調整模型參數

## 🔒 安全注意事項

- **API金鑰**: 請勿上傳至公開倉庫
- **大型文件**: 已在 `.gitignore` 中排除
- **環境變數**: 使用 `.env` 文件管理敏感信息
- **數據隱私**: 遵守相關數據保護法規

## 📊 專案統計

- **代碼行數**: 10,000+ 行
- **模型數量**: 5+ 個預訓練模型
- **數據量**: 數百MB的餐廳數據
- **支援語言**: 中文、英文
- **功能模組**: 4個主要模組

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request



## 🙏 致謝

- 感謝所有開源專案的貢獻者
- 感謝Google Maps API的支援
- 感謝Hugging Face提供的預訓練模型
- 感謝所有測試用戶的寶貴意見

---

**最後更新**: 2024年12月

**版本**: v1.0.0

**狀態**: 穩定版本，持續維護中 
=======
# restaurant-booking-recommender
>>>>>>> 80a5f999929a6f5e312c4e6cb171cccf7c87e94b
git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request



## 🙏 致謝

- 感謝所有開源專案的貢獻者
- 感謝Google Maps API的支援
- 感謝Hugging Face提供的預訓練模型
- 感謝所有測試用戶的寶貴意見

---

**最後更新**: 2024年12月

**版本**: v1.0.0

**狀態**: 穩定版本，持續維護中 