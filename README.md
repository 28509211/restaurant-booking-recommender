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

## 快速開始，⚠️ 開始前請先解壓縮資料

請先解壓縮下列壓縮檔案，否則後續資料處理與模型訓練將無法順利進行：

1. 進入 `CHATBOT` 資料夾，解壓縮DATA資料夾下的檔案：
   ```bash
   cd Data
    ```

   安裝解壓縮工具(如下) 或是 手動解壓縮:
   ```bash
   sudo apt-get update
   sudo apt-get install p7zip-full p7zip-rar
   ```

   ```bash
   7za x data.7z
   7za x storeinfo_review.7z
   7za x tag_embeddings.7z
   7za x updated_storeinfo_tablesm.7z
   ```

2. 根據模型連結下載模型權重([Google Drive模型權重下載](https://drive.google.com/drive/folders/1xt2j6hwjhCDhpAqlXl1bVf1dRDx-EIxc?usp=sharing) )，放到model資料夾中
  
3. 建立CHATBOT環境

cd CHATBOT

</details>
<summary><b>📦 方法一：使用 pip 安裝</b></summary>

```bash
# 安裝 Python 依賴套件
pip install -r requirements.txt
```

</details>

<details>
<summary><b>🐍 方法二：使用 Conda 環境</b></summary>

```bash
# 創建並激活 Conda 環境
conda env create -f environment.yml
conda activate chatbot
```

</details>

<details>
<summary><b>🐳 方法三：使用 Docker 容器</b></summary>

```bash
# 建構 Docker 映像
docker build -t t-chatbot .

# 運行容器 (支援 GPU)   /path/to/data 可以在本機中的放置data資料夾的位置  /path/to/model 可以在本機中的放置model資料夾的位置
docker run --gpus all -it \
  --name chatbot_env \
  -v /path/to/data:/app/data \
  -v /path/to/model:/app/model \
  -p 5000:5000 \
  t-chatbot /bin/bash

# 裝編譯修改氣，方便修改code
apt-get update
apt-get install nano -y

# 激活環境
conda activate chatbot

```
</details>

4.🔑 API 金鑰設定

- 請編輯 `env_api_key.env` 或 `.env` 檔案，填入您的 API 金鑰，例如：
  ```env
  # Bland AI API Key (用於電話訂位功能)
  BLAND_AI_API_KEY=your_bland_ai_api_key_here
  ```

5. 開啟CHATBOT SERVER

## 🛠️ 一鍵啟動與常用指令

1. **一鍵安裝與啟動（推薦）**
   ```bash
   python script.py setup    # 檢查/安裝依賴、下載模型、檢查資料
   python script.py start    # 啟動伺服器
   ```
2. **手動啟動主程式**
   ```bash
   python main.py
   ```
3. **其他常用指令**
   ```bash
   python script.py test     # 快速測試
   python script.py status   # 查看狀態
   python script.py help     # 參數說明
   python script.py setup    # 首次使用 - 完整設定
   python script.py config-ip --ip YOUR_SERVER_IP #配置模板 IP（如果需要外部訪問）
   python script.py restore-template #如果需要還原模板
   
6. 開啟資料庫(DB) SERVER

## ⚡ 一鍵啟動

```bash
# 1. 進入 DB 目錄
cd DB

# 2. 停止並清理舊容器
docker compose down -v

# 3. 重新建構所有服務
docker compose build --no-cache

# 4. 啟動所有服務
docker compose up -d

```

7.使用Android Studio開啟App資料夾即可進入介面


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
