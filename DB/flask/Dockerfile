FROM python:3.11-slim

WORKDIR /app

# 安裝依賴
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式
COPY . .

# 服務埠（與 .env 的 FLASK_PORT 對應）
EXPOSE 5001

CMD ["python", "app.py"]
