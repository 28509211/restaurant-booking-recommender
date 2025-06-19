# App 資料夾說明

本資料夾為 Android 前端應用程式的主要原始碼，負責餐廳推薦與訂位系統的使用者介面與互動邏輯。  
主要功能包含：用戶帳號管理、餐廳推薦、地圖顯示、聊天助理、訂單管理等。

## 目錄結構與說明

- `MainActivity.java`  
  應用程式的主入口，負責底部導覽列與 Fragment 切換（如助理、地圖、收藏、帳號）。

- `AssistentFragment.java`  
  智能助理頁面，提供與聊天機器人互動的入口。

- `ChatActivity.java`  
  聊天室頁面，與推薦助理進行對話、獲取餐廳推薦與導航。

- `FavorFragment.java`  
  收藏與推薦頁面，顯示個人化推薦、分類瀏覽與歷史紀錄。

- `MapsFragment.java`  
  地圖頁面，顯示附近餐廳位置，支援定位與地圖互動。

- `AccountFragment.java`  
  用戶帳號資訊頁面，顯示與編輯個人資料，支援登出功能。

- `OrderActivity.java`  
  訂單管理頁面，顯示用戶的訂單資訊。

- `CartActivity.java`  
  購物車頁面，管理用戶選購的餐點。

- `RegisterActivity.java`、`LoginActivity.java`  
  用戶註冊與登入頁面。

- `IntroduceActivity.java`  
  應用程式介紹頁面。

- `InterestSelectActivity.java`  
  用戶興趣選擇頁面，用於個人化推薦。

- `SearchResultActivity.java`  
  餐廳搜尋結果頁面。

- `StoreDetailActivity.java`、`StoreInfoBottomSheet.java`  
  餐廳詳細資訊顯示與底部彈窗。

### 子資料夾

- `Adapter/`  
  放置 RecyclerView 與 Spinner 等 UI 元件的 Adapter 及相關資料結構（如餐點、分類、訊息等）。

- `ForGoogleMaps/`  
  Google Maps 相關功能的輔助類別（如地點解析、下載、附近地點查詢等）。

---

如需更詳細的類別與方法說明，請參考各檔案內註解。  
如有新功能或頁面，請同步更新本說明文件。 