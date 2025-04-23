from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import os
from dotenv import load_dotenv
from .models import Game, Guess, GlobalGuess, engine
from sqlalchemy.orm import sessionmaker
from .cache import cache_manager
from .ai_service import ai_service
import re

load_dotenv()

app = FastAPI(title="What Beats Rock", version="1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Database session
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Profanity filter
def is_profane(word: str) -> bool:
    # Simple profanity check - can be enhanced with a proper profanity filter
    profane_patterns = [
        r'\b(shit|fuck|ass|bitch|damn|hell)\b',
        r'\b\d{4,}\b',  # Numbers with 4 or more digits
        r'[^\w\s]',     # Special characters
    ]
    word = word.lower()
    return any(re.search(pattern, word) for pattern in profane_patterns)

@app.get("/")
async def root():
    return {"message": "Welcome to What Beats Rock!"}

@app.get("/game/start")
async def start_game(request: Request, db = Depends(get_db)):
    # Check rate limit
    if not cache_manager.check_rate_limit(request.client.host):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    # Create new game
    game = Game(player_id=request.client.host)
    db.add(game)
    db.commit()
    
    return {
        "current_word": "rock",
        "score": 0,
        "guesses": []
    }

@app.post("/game/guess")
async def make_guess(guess: str, request: Request, db = Depends(get_db)):
    # Check rate limit
    if not cache_manager.check_rate_limit(request.client.host):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    # Validate input
    guess = guess.strip().lower()
    if not guess or len(guess) > 50 or is_profane(guess):
        raise HTTPException(status_code=400, detail="Invalid guess")
    
    # Get current game
    game = db.query(Game).filter_by(player_id=request.client.host).order_by(Game.id.desc()).first()
    if not game:
        raise HTTPException(status_code=400, detail="No active game")
    
    # Check if guess already exists
    if any(g.word == guess for g in game.guesses):
        raise HTTPException(status_code=400, detail="Game Over! This guess has already been made.")
    
    # Get current word
    current_word = game.guesses[-1].word if game.guesses else "rock"
    
    # Validate with AI
    is_valid, explanation = await ai_service.validate_word_pair(current_word, guess)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid guess: {explanation}")
    
    # Update game state
    new_guess = Guess(game_id=game.id, word=guess)
    db.add(new_guess)
    game.score += 1
    
    # Update global guess count
    global_guess = db.query(GlobalGuess).filter_by(word=guess).first()
    if global_guess:
        global_guess.count += 1
    else:
        global_guess = GlobalGuess(word=guess)
        db.add(global_guess)
    
    db.commit()
    
    return {
        "success": True,
        "message": f"✅ Nice! '{guess}' beats '{current_word}'. {explanation}",
        "score": game.score,
        "current_word": guess,
        "global_count": global_guess.count
    }

@app.get("/game/history")
async def get_history(request: Request, db = Depends(get_db)):
    # Check rate limit
    if not cache_manager.check_rate_limit(request.client.host):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    game = db.query(Game).filter_by(player_id=request.client.host).order_by(Game.id.desc()).first()
    if not game:
        raise HTTPException(status_code=400, detail="No active game")
    
    return {
        "guesses": [g.word for g in game.guesses],
        "score": game.score
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 