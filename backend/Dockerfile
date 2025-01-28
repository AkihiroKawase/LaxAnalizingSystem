FROM python:3.11-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt .

# pip をアップデートし、依存関係をインストール
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルをすべてコピー
COPY . .

# 必要な環境変数を設定
ENV DATABASE_URL="sqlite:///./test.db"

# FastAPI アプリケーションを起動
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

