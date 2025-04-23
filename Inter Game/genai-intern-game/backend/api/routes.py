from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from ..db.models import Game, Guess
from ..core.game_logic import game_logic
from ..core.cache import cache_manager
from ..db.models import get_db

router = APIRouter()

@router.get("/game/start")
async def start_game(request: Request, db: Session = Depends(get_db)):
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

@router.post("/game/guess")
async def make_guess(guess: str, request: Request, db: Session = Depends(get_db)):
    # Check rate limit
    if not cache_manager.check_rate_limit(request.client.host):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    # Get current game
    game = db.query(Game).filter_by(player_id=request.client.host).order_by(Game.id.desc()).first()
    if not game:
        raise HTTPException(status_code=400, detail="No active game")
    
    # Process guess
    result = await game_logic.process_guess(game, guess)
    
    if result["success"]:
        # Save the new guess
        new_guess = Guess(game_id=game.id, word=guess)
        db.add(new_guess)
        db.commit()
        
        return result
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@router.get("/game/history")
async def get_history(request: Request, db: Session = Depends(get_db)):
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