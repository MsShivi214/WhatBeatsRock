import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.models import Game, Guess, get_db
from sqlalchemy.orm import Session

client = TestClient(app)

def test_duplicate_guess_game_over():
    # Start a new game
    response = client.get("/api/game/start")
    assert response.status_code == 200
    data = response.json()
    assert data["current_word"] == "rock"
    assert data["score"] == 0
    assert data["guesses"] == []
    
    # Make a valid guess
    response = client.post("/api/game/guess", json={"guess": "paper"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "paper" in data["message"]
    assert data["score"] == 1
    
    # Make the same guess again (should fail)
    response = client.post("/api/game/guess", json={"guess": "paper"})
    assert response.status_code == 400
    assert "Game Over" in response.json()["detail"]
    
    # Verify game state in database
    with Session(get_db()) as db:
        game = db.query(Game).order_by(Game.id.desc()).first()
        assert game is not None
        assert game.score == 1
        assert len(game.guesses) == 1
        assert game.guesses[0].word == "paper"
        
        # Try to make another guess (should fail)
        response = client.post("/api/game/guess", json={"guess": "scissors"})
        assert response.status_code == 400
        assert "No active game" in response.json()["detail"] 