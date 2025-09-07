# 📱 訂食吧 - 智能餐廳推薦 App

## 📖 專案簡介

**訂食吧** 是一個基於 Android 的智能餐廳推薦與訂餐應用程式。結合 AI 聊天機器人、地圖導航、購物車系統等功能，為用戶提供個性化的餐廳推薦和便捷的訂餐體驗。

## 🎯 主要功能

### 🤖 AI 語音助理
- 即時文字對話
- 餐廳推薦查詢
- 訂位服務

### 🗺️ 美食地圖
- GPS 定位搜尋
- 附近餐廳顯示
- 地圖導航功能

### 🍽️ 餐廳服務
- 關鍵字搜尋
- 分類篩選
- 詳細資訊查看
- 購物車管理

## 📱 應用介面

### 🔐 登入/註冊頁面
- **LoginActivity** - 用戶登入介面
- **RegisterActivity** - 新用戶註冊介面
- **IntroduceActivity** - 應用介紹頁面

### 🏠 主頁面
- **MainActivity** - 主導航頁面
- **FavorFragment** - 推薦餐廳頁面
- **MapsFragment** - 美食地圖頁面
- **AssistentFragment** - AI 助理頁面
- **AccountFragment** - 個人帳號頁面

### 🍴 餐廳相關
- **StoreDetailActivity** - 餐廳詳細資訊
- **SearchResultActivity** - 搜尋結果頁面
- **InterestSelectActivity** - 興趣偏好設定

### 🛒 訂餐功能
- **CartActivity** - 購物車頁面
- **OrderActivity** - 訂單確認頁面
- **ChatActivity** - AI 聊天介面

## 🚀 快速開始

### 📱 使用 Android Studio 開啟專案

1. 開啟 **Android Studio**
2. 選擇 **Open an existing project**
3. 選擇 `App` 資料夾
4. 等待 Gradle 同步完成
5. 連接 Android 裝置或啟動模擬器
6. 點擊 **Run** 按鈕

### ⚙️ API 配置

在 `apiURLs.java` 檔案中設定後端服務位址：

```java
public class apiURLs {
    // 主要 API 服務
    public static final String BASE_URL = "http://YOUR_SERVER_IP:8080/";
    
    // Flask AI 服務
    public static final String BASE_FLASK_URL = "http://YOUR_SERVER_IP:5001/";
    
    // Socket.IO 聊天服務(根據CHATBOT\templates\index.html去設定)
    public static final String BASE_SOCKET_URL = "http://YOUR_SERVER_IP:5000/";
}
```

**重要**: 請將 `YOUR_SERVER_IP` 替換為您的實際伺服器 IP 位址。

### 🔑 Google Maps API

在 `AndroidManifest.xml`(App/app/src/main/AndroidManifest.xml) 中設定 Google Maps API Key：

```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_GOOGLE_MAPS_API_KEY" />
```

## 📋 系統需求

- **Android Studio**: Arctic Fox 或更新版本
- **Android SDK**: API Level 24+ (Android 7.0)
- **Java**: JDK 8 或更新版本

## 🔧 權限需求

應用程式需要以下權限：
- 網路存取
- GPS 定位
- 電話撥打
- 外部儲存讀取

---

*最後更新：2024年12月*