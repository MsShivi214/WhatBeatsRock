from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_start_game():
    response = client.get("/game/start")
    assert response.status_code == 200
    data = response.json()
    assert data["current_word"] == "rock"
    assert data["score"] == 0
    assert data["guesses"] == []

def test_make_guess():
    # Start a new game
    client.get("/game/start")
    
    # Make a valid guess
    response = client.post("/game/guess", json={"guess": "paper"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "paper" in data["message"]
    assert data["score"] == 1
    
    # Make the same guess again (should fail)
    response = client.post("/game/guess", json={"guess": "paper"})
    assert response.status_code == 400
    assert "Game Over" in response.json()["detail"]

def test_get_history():
    # Start a new game
    client.get("/game/start")
    
    # Make some guesses
    client.post("/game/guess", json={"guess": "paper"})
    client.post("/game/guess", json={"guess": "scissors"})
    
    # Get history
    response = client.get("/game/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data["guesses"]) == 2
    assert data["score"] == 2 