# Data 資料夾

此資料夾包含餐廳訂位推薦系統的所有數據處理相關檔案，已按功能分類整理。

## 📁 資料夾結構

### 📂 data_raw/
**原始數據檔案**
- 包含所有未經處理的原始文本數據
- 主要檔案：
  - `chat_train_data.txt` - 聊天訓練數據
  - `chat_traindata_reserve_情況*.txt` - 訂位情況訓練數據
  - `有關reservedata改_zh.txt` - 中文訂位數據
  - 各種英文對話學習資料（餐廳訂位相關）

### 📂 data_processed/
**已處理的數據檔案**
- 包含經過格式化和處理後的JSON數據
- 主要檔案：
  - `conversation*.json` - 對話格式數據
  - `dialogue*.json` - 對話數據
  - `chat_traindata_reserve_情況*.json` - 訂位情況JSON格式
  - `chat_normal.json` - 一般聊天數據
  - `output.json` - 處理輸出結果

### 📂 scripts/
**數據處理腳本**
- 包含所有Python處理腳本
- 主要腳本：
  - `change_to_json.py` - 轉換為JSON格式
  - `change_format.py` - 格式轉換
  - `chat_traindata_alpach_format.py` - Alpaca格式轉換
  - `chat_traindata_sharegpt_format.py` - ShareGPT格式轉換
  - `main_trans.py` - 主要翻譯腳本
  - `translatess.py` - 翻譯處理
  - `constant.py` - 常數定義
  - `new_format_json.py` - 新JSON格式處理


## 🔧 使用說明

### 數據處理流程
1. **原始數據** → 放在 `data_raw/`
2. **處理腳本** → 使用 `scripts/` 中的腳本
3. **處理結果** → 輸出到 `data_processed/`

### 常用腳本說明
- `change_to_json.py`: 將txt格式轉換為JSON格式
- `main_trans.py`: 主要翻譯處理腳本
- `chat_traindata_alpach_format.py`: 轉換為Alpaca訓練格式

### 數據格式
- **原始格式**: 使用特殊標籤如 `<G>`, `<USER>`, `<LABEL>`, `<BOT>`
- **JSON格式**: 標準化的對話數據格式
- **Alpaca格式**: 適用於大語言模型微調的格式

## 📊 數據統計

### 原始數據
- 聊天訓練數據: ~545KB
- 訂位情況數據: 7個不同情況檔案
- 英文學習資料: 多個餐廳訂位對話檔案

### 處理後數據
- 對話JSON檔案: 多個conversation檔案
- 訂位JSON檔案: 多個reserve情況檔案
- 總計: 15個JSON檔案

## 🚀 快速開始

1. 檢查 `data_raw/` 中的原始數據
2. 根據需求選擇 `scripts/` 中的處理腳本
3. 執行腳本處理數據
4. 在 `data_processed/` 中查看結果

## 📝 注意事項

- 所有敏感資訊已清理
- 暫存檔案已移至 `temp/` 資料夾
- 建議定期清理 `temp/` 資料夾
- 處理腳本執行前請備份重要數據

---

**最後更新**: 2024年整理完成 