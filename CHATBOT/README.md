# 智能餐廳聊天機器人（CHATBOT）

本模組為基於 Python、深度學習與 NLP 的智能餐廳聊天機器人，支援餐廳推薦、訂位、評論查詢、地圖導航、智能問答等多種功能。

---

## 🚀 主要功能
- 餐廳推薦、訂位、評論查詢、地圖導航
- 智能問答與多輪對話
- 用戶意圖識別與實體抽取
- 集中配置管理，易於擴充

---

## ⚡ 安裝環境與資料解壓縮

1. **安裝 Python 依賴與 SpaCy 中文模型**
   ```bash
   pip install -r requirements.txt
   python -m spacy download zh_core_web_sm
   ```
2. **解壓縮資料檔案**（若程式無法直接讀取 .zip 請先解壓）
   ```bash
   gunzip data.json.zip
   gunzip storeinfo_review.json.zip
   gunzip tag_embeddings.json.zip
   gunzip updated_storeinfo_tablesm.json.zip
   ```
3. **下載模型權重**
   - 請至 [Google Drive模型權重下載](https://drive.google.com/drive/folders/1xt2j6hwjhCDhpAqlXl1bVf1dRDx-EIxc?usp=sharing) 下載所有模型資料夾，依說明放置本資料夾下的model資料夾中。

---

## 🔑 API 金鑰設定

- 請編輯 `env_api_key.env` 或 `.env` 檔案，填入您的 API 金鑰，例如：
  ```env
  # Bland AI API Key (用於電話訂位功能)
  BLAND_AI_API_KEY=your_bland_ai_api_key_here
  ```

---

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
   ```

---

## 🌐 聊天網頁前端（templates 資料夾）

- `templates/` 資料夾內含 `index.html`，為 Flask 伺服器的聊天網頁前端模板。
- 啟動伺服器後（預設 http://localhost:5000/ ），可用瀏覽器開啟 `http://[你的IP]:5000/` 進行聊天測試。
- `index.html` 提供打字特效與互動介面

---

## 📁 主要檔案與資料夾說明

| 檔案/資料夾                | 說明                                   |
|----------------------------|----------------------------------------|
| `main.py`                  | Flask + SocketIO 主伺服器與對話邏輯    |
| `script.py`                | 一鍵啟動/測試/環境檢查腳本             |
| `config.py`                | 所有模型、資料、權重等路徑集中設定      |
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
| `requirements.txt`         | Python 依賴套件清單                    |
| `env_api_key.env`          | API金鑰環境變數檔案                     |
| `CONFIG_SUMMARY.md`        | 配置整理總結與說明                     |
| `data.json`                | 餐廳基本資料（JSON）                   |
| `storeinfo_review.json`    | 餐廳評論與詳細資料（大型JSON）         |
| `tag_embeddings.json`      | 標籤向量嵌入（大型JSON）               |
| `updated_storeinfo_tablesm.json` | 精簡版餐廳評論資料             |
| `templates/`               | Flask 聊天網頁前端模板                  |

---

## ⚙️ 配置管理與修改
- **所有路徑、模型、資料設定皆集中於 `config.py`**，如需更換模型或資料路徑，請直接修改該檔案。
- API 金鑰請於 `env_api_key.env` 或 `.env` 設定。
- 進階配置與常量說明請參考 `CONFIG_SUMMARY.md`。

---

## ❓ 常見問題
- 啟動失敗：請確認依賴、資料、模型、API金鑰皆已正確安裝與設定。
- 缺少檔案：請依照上方步驟下載並解壓所有必要資料與模型。
- 其他問題：可先執行 `python script.py test` 進行快速檢查。

---

## 📬 聯絡與貢獻
- 歡迎提交 Issue 或 Pull Request 改進本專案。
- 有任何問題可於專案頁面留言討論。

---

**最後更新：2024/06**
