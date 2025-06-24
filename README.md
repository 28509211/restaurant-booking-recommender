# Restaurant Booking Recommender System
# 智能餐廳訂位推薦系統

一個整合聊天機器人、數據收集、機器學習訓練、Android前端App的全流程智能餐廳推薦與訂位系統。

## 🌟 專案特色

- **🤖 智能聊天機器人**: 基於深度學習的多輪對話系統，支援餐廳推薦、訂位、評論查詢
- **🧠 機器學習模型**: 多標籤分類、二分類、LLaMA-3微調等多種模型
- **📊 數據處理管道**: 完整的數據清洗、格式轉換、訓練數據生成流程
- **📱 Android前端App**: 提供用戶友善的推薦、訂位、地圖、聊天等功能
- **🔧 模組化設計**: 各功能模組獨立，易於維護和擴展

---

## ⚠️ 開始前請先解壓縮資料

請先解壓縮下列壓縮檔案，否則後續資料處理與模型訓練將無法順利進行：

1. 進入 `Data` 資料夾，解壓縮原始與處理後數據：
   ```bash
   cd Data
   unzip data_raw.zip
   unzip data_processed.zip
   ```
2. 進入 `CHATBOT` 資料夾，確認下列 `.gz` 檔案是否需要解壓縮（如有需要可用 `gunzip` 解壓）：
   - `data.json.gz`
   - `storeinfo_review.json.gz`
   - `tag_embeddings.json.gz`
   - `updated_storeinfo_tablesm.json.gz`
   ```bash
   cd ../CHATBOT
   gunzip data.json.gz
   gunzip storeinfo_review.json.gz
   gunzip tag_embeddings.json.gz
   gunzip updated_storeinfo_tablesm.json.gz
   ```
   > 若程式可直接讀取 `.gz` 檔案則可略過此步驟，否則請先解壓。

---

## 目錄結構

- `CHATBOT/`：聊天機器人後端（Python Flask + NLP）
- `App/`：Android 前端原始碼
- `Data/`：資料處理與轉換腳本
- `Train/`：機器學習模型訓練

---



## 📋 使用指南

### 1. 聊天機器人後端（CHATBOT）

1. 進入資料夾：
   ```bash
   cd CHATBOT
   ```
2. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   python -m spacy download zh_core_web_sm
   ```
3. 下載模型（詳見 CHATBOT/README.md 說明，需將模型資料夾放在指定路徑）。
4. 設定 API 金鑰：
   - 編輯 `env_api_key.env` 或 `.env` 檔案，填入金鑰。
5. 一鍵安裝與啟動（推薦）：
   ```bash
   python script.py setup
   python script.py start
   ```
   也可直接執行主程式：
   ```bash
   python main.py
   ```
6. 其他常用指令請參考 `CHATBOT/README.md`。

---

### 2. Android 前端（App）

1. 進入資料夾：
   ```bash
   cd App
   ```
2. 使用 Android Studio 開啟本資料夾，依需求編譯與執行。
3. 主要功能與頁面說明請參考 `App/README.md`。

---

### 3. 資料處理（Data）

1. 進入資料夾：
   ```bash
   cd Data
   ```
2. 原始資料放於 `data_raw/`，處理後資料於 `data_processed/`。
3. 使用 `scripts/` 內的 Python 腳本進行格式轉換、翻譯等：
   ```bash
   cd scripts
   python change_to_json.py
   # 其他腳本請參考 Data/README.md
   ```
4. 詳細資料格式與流程請參考 `Data/README.md`。

---

### 4. 機器學習訓練（Train）

1. 進入資料夾：
   ```bash
   cd Train
   ```
2. 依需求執行 Jupyter Notebook 進行模型訓練：
   - `NLU_BERT_MULTILABEL.ipynb`：多標籤分類
   - `NLU_FOR_Binary.ipynb`：二分類
   - `Finetune_Llama3_with_LLaMA_Factory_ipynb`：LLaMA-3 微調
3. 需先安裝相關 Python 套件：
   ```bash
   pip install transformers datasets accelerate torch
   ```
4. 詳細訓練流程與參數請參考 `Train/README.md`。

---

## 注意事項

- 請依各子資料夾 README 進行詳細操作。
- 敏感金鑰請勿上傳至公開倉庫。
- 大型模型與資料檔案請依說明下載並放置正確路徑。
- 執行訓練前請備份重要資料。

---

如需更詳細的說明，請參考各子資料夾內的 `README.md` 文件。
