## 🚀 快速啟動

### 📋 系統需求

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **8GB+ RAM** (建議)

### ⚡ 一鍵啟動

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

## 服務端點

| 服務 | 端口 | 用途 | 訪問地址 |
|------|------|------|----------|
| **MariaDB** | 3306 | 資料庫服務 | `localhost:3306` |
| **phpMyAdmin** | 8081 | 資料庫管理 | `http://localhost:8081` |
| **PHP API** | 8080 | REST API | `http://localhost:8080` |
| **Flask API** | 5001 | AI 推薦 | `http://localhost:5001` |

