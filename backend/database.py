import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# 環境変数から DATABASE_URL を取得
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# ベースクラスの定義
Base = declarative_base()

# 再試行回数と間隔を設定
MAX_RETRIES = 5
RETRY_DELAY = 5  # 秒

def create_db_engine_with_retries():
    """データベース接続を再試行しながらエンジンを作成"""
    for attempt in range(MAX_RETRIES):
        try:
            engine = create_engine(DATABASE_URL)
            # 接続テストを実行
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection established.")
            return engine
        except OperationalError as e:
            print(f"Database connection failed. Retrying in {RETRY_DELAY} seconds... ({attempt + 1}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
    raise Exception("Failed to connect to the database after multiple retries.")

# データベースエンジンの作成（再試行付き）
engine = create_db_engine_with_retries()

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from backend import models  # 絶対インポートに変更
    Base.metadata.create_all(bind=engine)
