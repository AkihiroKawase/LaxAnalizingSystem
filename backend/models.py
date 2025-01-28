from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Float,
    ForeignKey,
    Date,
    Time,
    func
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.engine import Engine

Base = declarative_base()

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # リレーション
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    coaches = relationship("Coach", back_populates="team", cascade="all, delete-orphan")

    # Home/Away 両方を紐づけるために2種類のリレーションを定義
    home_matches = relationship(
        "Match",
        foreign_keys="[Match.home_team_id]",
        back_populates="home_team"
    )
    away_matches = relationship(
        "Match",
        foreign_keys="[Match.away_team_id]",
        back_populates="away_team"
    )

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    name = Column(String, nullable=False)
    uniform_number = Column(Integer)
    position = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # リレーション
    team = relationship("Team", back_populates="players")
    shots = relationship("Shot", back_populates="player")
    faceoffs = relationship("Faceoff", back_populates="player")
    turnovers = relationship("Turnover", back_populates="player")
    goalie_saves = relationship("GoalieSave", back_populates="player")

class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String)  # 例: "Head Coach", "Analyst" など
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # リレーション
    team = relationship("Team", back_populates="coaches")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    match_date = Column(Date)
    location = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # リレーション
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")

    shots = relationship("Shot", back_populates="match")
    faceoffs = relationship("Faceoff", back_populates="match")
    turnovers = relationship("Turnover", back_populates="match")
    goalie_saves = relationship("GoalieSave", back_populates="match")

class Shot(Base):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    is_goal = Column(Boolean)
    assist = Column(Boolean)
    position_x = Column(Float)
    position_y = Column(Float)
    shot_time = Column(Time)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # リレーション
    match = relationship("Match", back_populates="shots")
    player = relationship("Player", back_populates="shots")

class Faceoff(Base):
    __tablename__ = "faceoffs"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    result = Column(String)  # 例: "WIN", "LOSE"
    faceoff_time = Column(Time)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # リレーション
    match = relationship("Match", back_populates="faceoffs")
    player = relationship("Player", back_populates="faceoffs")

class Turnover(Base):
    __tablename__ = "turnovers"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    turnover_type = Column(String)  # 例: "Forced", "Unforced" など
    turnover_time = Column(Time)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # リレーション
    match = relationship("Match", back_populates="turnovers")
    player = relationship("Player", back_populates="turnovers")

class GoalieSave(Base):
    __tablename__ = "goalie_saves"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)  # GK
    shot_id = Column(Integer, ForeignKey("shots.id"))  # セーブ対象のシュートID
    save_time = Column(Time)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # リレーション
    match = relationship("Match", back_populates="goalie_saves")
    player = relationship("Player", back_populates="goalie_saves")
    shot = relationship("Shot", backref="saved_by", uselist=False)

def create_tables(engine: Engine):
    """
    エンジン（DB接続情報）を受け取り、テーブルを作成する関数。
    例: create_tables(engine)
    """
    Base.metadata.create_all(bind=engine)
