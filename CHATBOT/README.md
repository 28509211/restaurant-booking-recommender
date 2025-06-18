# 智能餐廳聊天機器人 (Intelligent Restaurant Chatbot)

本專案是一個基於 Python、深度學習與 NLP 的智能餐廳聊天機器人，支援餐廳推薦、訂位、評論查詢、地圖導航、智能問答等多種功能，適合用於餐飲服務、智能客服、語音助理等場景。

---

## 🚀 主要功能

- **餐廳推薦**：根據用戶需求推薦合適的餐廳
- **訂位服務**：協助用戶進行餐廳訂位
- **評論查詢**：查詢餐廳評論與特色
- **地圖導航**：提供餐廳地址與導航
- **智能問答/閒聊**：支援日常對話與餐飲相關問答
- **多輪詢問模式**：可持續提問，直到用戶輸入"0"才結束
- **集中配置管理**：所有模型路徑和數據文件路徑統一在 `config.py` 中管理

---

## 📁 專案結構與檔案說明

| 檔案/資料夾                | 說明                                   |
|----------------------------|----------------------------------------|
| `main.py`                  | Flask + SocketIO 主伺服器與對話邏輯    |
| `script.py`                | 一鍵啟動/測試/環境檢查腳本             |
| `config.py`                | **所有模型、資料、權重等路徑集中設定**  |
| `chat_function.py`         | 對話生成、NLG、API串接                 |
| `classification_function.py`| NLU意圖分類模型與功能                  |
| `spacy_function.py`        | NER命名實體辨識功能                    |
| `dp_function.py`           | 對話流程管理（Dialog Policy）           |
| `user_information.py`      | 用戶狀態與對話歷史管理                 |
| `database.py`              | 餐廳資料、評論資料存取                 |
| `compare_text.py`          | 文字比對輔助工具                       |
| `multi_function_tools.py`  | 多功能輔助工具                         |
| `spacy_ruler.py`           | SpaCy規則設定                          |
| `use_function.py`          | 功能整合與調用                         |
| `test_nlu_function.py`     | NLU測試腳本                            |
| `test_ner_function.py`     | NER測試腳本                            |
| `data.json`                | 餐廳基本資料（JSON）                   |
| `storeinfo_review.json`    | 餐廳評論與詳細資料（大型JSON）         |
| `tag_embeddings.json`      | 標籤向量嵌入（大型JSON）               |
| `updated_storeinfo_tablesm.json` | 精簡版餐廳評論資料             |
| `test_review.txt`          | 測試用評論資料                         |
| `env_api_key.env`          | API金鑰環境變數檔案                     |
| `requirements.txt`         | Python 依賴套件清單                    |
| `review/`                  | 動態產生/存放各店家評論的 txt 檔案      |
| `CONFIG_SUMMARY.md`        | 配置整理完成總結                       |
| 其他                       | 其他輔助/測試/臨時檔案                 |

---

## 📥 模型權重下載

請先至 [Google Drive模型權重下載](https://drive.google.com/drive/folders/1xt2j6hwjhCDhpAqlXl1bVf1dRDx-EIxc?usp=sharing) 下載所有模型資料夾，並放置於專案根目錄。

**必要模型目錄：**
- `CHATBOT/output/` - NER模型
- `CHATBOT/output2_dia_*/` - 對話模型
- `CHATBOT/new_result/` - NLU模型
- `CHATBOT/Is_Collect_or_Function/` - 收集分類模型
- `CHATBOT/NLG_TAIDE/` - NLG模型
- `CHATBOT/shibing624_text2vec-base-chinese/` - 文本向量模型

---

## 🛠️ 環境安裝與設定

### 1. 快速安裝（推薦）
```bash
# 使用腳本自動安裝和檢查
python script.py setup
```

### 2. 手動安裝
```bash
# 安裝 Python 3.8+
# 安裝依賴套件
pip install -r requirements.txt

# 下載 SpaCy 中文模型
python -m spacy download zh_core_web_sm

# 設定環境變數
手動修改 env_api_key.env
# 編輯 .env 文件，填入您的 API 金鑰
```

### 3. 依賴套件說明
- **Web框架**：Flask, Flask-SocketIO, Gevent
- **深度學習**：Transformers, Torch, SpaCy, Sentence-Transformers
- **LangChain**：LangChain, LangChain-Community, LangChain-HuggingFace
- **特殊模型**：LLaMA-Factory
- **工具庫**：Pandas, OpenPyXL, Python-Levenshtein, Requests

### 4. 安裝問題解決
- 若遇到 `llama-factory` 安裝問題：
  ```bash
  pip install git+https://github.com/hiyouga/LLaMA-Factory.git
  ```
- 若遇到 C++ 編譯錯誤，請安裝 Visual C++ Build Tools
- 建議先升級 pip：`pip install --upgrade pip`

---

## 🎯 使用方式

### 1. 推薦啟動方式
```bash
# 基本啟動
python script.py start

# 調試模式
python script.py start --debug

# 外部訪問
python script.py start --external

# 自定義主機和端口
python script.py start --host 0.0.0.0 --port 8080
```

### 2. 其他常用指令
```bash
# 環境檢查與安裝
python script.py setup

# 快速測試
python script.py test

# 查看狀態
python script.py status

# 參數說明
python script.py help
```

### 3. 直接執行
```bash
python main.py
```

---

## 🔧 進階設定與可修改區域

### 配置修改
- **所有路徑配置**：修改 `config.py` 中的常量
- **API 金鑰**：在 `.env` 文件中設定
- **模型參數**：在各對應的 Python 文件中調整

### 功能自定義
- **對話策略**：修改 `dp_function.py`
- **用戶管理**：修改 `user_information.py`
- **NLU/NER/NLG**：修改對應的 function 文件
- **數據庫**：修改 `database.py`

### 數據文件
- **評論資料**：`review/` 目錄自動產生各店家評論
- **測試資料**：`test_review.txt` 用於測試
- **配置總結**：`CONFIG_SUMMARY.md` 記錄配置變更

---

## 💡 常見問題與解決方案

### 啟動問題
- **模型權重未下載**：確保所有模型目錄存在
- **依賴套件缺失**：執行 `python script.py setup`
- **API金鑰未設定**：檢查 `.env` 文件

### 功能問題
- **詢問模式**：輸入"0"可結束多輪詢問
- **路徑錯誤**：檢查 `config.py` 中的路徑設定
- **模型載入失敗**：確認模型文件完整性

### 安全注意事項
- **API金鑰**：請勿上傳至公開倉庫
- **大型文件**：已在 `.gitignore` 中排除
- **環境變數**：使用 `.env` 文件管理敏感信息

---

## 📊 功能特色

### 智能對話
- **多輪對話**：支援上下文理解
- **意圖識別**：準確識別用戶意圖
- **實體提取**：自動提取關鍵信息

### 餐廳服務
- **智能推薦**：基於用戶偏好推薦
- **訂位協助**：自動化訂位流程
- **評論查詢**：快速獲取餐廳評價
- **導航指引**：提供地址和路線

### 技術優勢
- **模組化設計**：易於維護和擴展
- **配置集中**：統一管理所有設定
- **錯誤處理**：完善的異常處理機制
- **測試友好**：提供完整的測試腳本

---

## 🙏 聯絡與貢獻

- **問題回報**：歡迎提交 Issue
- **功能建議**：歡迎提出改進建議
- **代碼貢獻**：歡迎提交 Pull Request
- **模型下載**：[Google Drive模型權重](https://drive.google.com/drive/folders/1xt2j6hwjhCDhpAqlXl1bVf1dRDx-EIxc?usp=sharing)

---

## 📝 更新日誌

### v2.0.0 (最新)
- ✅ 新增集中配置管理系統 (`config.py`)
- ✅ 更新啟動腳本 (`script.py`)
- ✅ 改進依賴管理 (`requirements.txt`)
- ✅ 優化文檔結構 (`README.md`)
- ✅ 新增配置總結文檔 (`CONFIG_SUMMARY.md`)
- ✅ 修復詢問模式持續對話功能
- ✅ 統一所有路徑配置

---

**請務必詳閱本說明文件與程式內註解，確保順利運行與開發！** 
