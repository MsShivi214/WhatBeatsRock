from typing import List, Optional
from ..db.models import Game, Guess, GlobalGuess
from .ai_client import ai_client
from .cache import cache_manager
import re

class GameLogic:
    def __init__(self):
        self.profane_patterns = [
            r'\b(shit|fuck|ass|bitch|damn|hell)\b',
            r'\b\d{4,}\b',  # Numbers with 4 or more digits
            r'[^\w\s]',     # Special characters
        ]
    
    def is_profane(self, word: str) -> bool:
        """Check if a word contains profanity or invalid characters"""
        word = word.lower()
        return any(re.search(pattern, word) for pattern in self.profane_patterns)
    
    def validate_guess(self, guess: str) -> bool:
        """Validate the format of a guess"""
        guess = guess.strip().lower()
        return bool(guess and len(guess) <= 50 and not self.is_profane(guess))
    
    async def process_guess(self, game: Game, guess: str) -> dict:
        """Process a new guess and update game state"""
        # Validate input
        if not self.validate_guess(guess):
            return {"success": False, "message": "Invalid guess"}
        
        # Check if guess already exists
        if any(g.word == guess for g in game.guesses):
            return {"success": False, "message": "Game Over! This guess has already been made."}
        
        # Get current word
        current_word = game.guesses[-1].word if game.guesses else "rock"
        
        # Validate with AI
        is_valid, explanation = await ai_client.validate_word_pair(current_word, guess)
        
        if not is_valid:
            return {"success": False, "message": f"Invalid guess: {explanation}"}
        
        # Update game state
        new_guess = Guess(game_id=game.id, word=guess)
        game.score += 1
        
        # Update global guess count
        global_count = cache_manager.increment_global_guess(guess)
        
        return {
            "success": True,
            "message": f"✅ Nice! '{guess}' beats '{current_word}'. {explanation}",
            "score": game.score,
            "current_word": guess,
            "global_count": global_count
        }

# Create a singleton instance
game_logic = GameLogic() 