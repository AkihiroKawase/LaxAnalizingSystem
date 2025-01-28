from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import SessionLocal, engine
from backend.database import init_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shots/", response_model=schemas.ShotCreate)
def create_shot(shot: schemas.ShotCreate, db: Session = Depends(get_db)):
    # Shot モデルのインスタンスを作成
    db_shot = models.Shot(**shot.dict())
    db.add(db_shot)
    db.commit()
    db.refresh(db_shot)
    return db_shot

# 新しいエンドポイント: 試合作成
@app.post("/matches/", response_model=schemas.MatchCreate)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    # Match.create_match を利用して新しい試合を作成
    try:
        new_match = models.Match.create_match(
            db_session=db,
            home_team_id=match.home_team_id,
            away_team_id=match.away_team_id,
            match_date=match.match_date,
            location=match.location
        )
    except Exception as e:
        # エラー処理（必要に応じて適切な HTTPException を投げる）
        raise HTTPException(status_code=400, detail=str(e))
    return new_match