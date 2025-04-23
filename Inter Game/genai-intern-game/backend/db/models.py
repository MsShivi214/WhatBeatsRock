from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(String)
    score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    guesses = relationship("Guess", back_populates="game", order_by="Guess.created_at")

class Guess(Base):
    __tablename__ = "guesses"
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    word = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    game = relationship("Game", back_populates="guesses")

class GlobalGuess(Base):
    __tablename__ = "global_guesses"
    
    id = Column(Integer, primary_key=True)
    word = Column(String, unique=True)
    count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create database engine
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rockgame")
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine) 