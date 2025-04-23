import os
import openai
from typing import Tuple
from ..core.cache import cache_manager

class AIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        openai.api_key = self.api_key
        
    async def validate_word_pair(self, current_word: str, guess: str) -> Tuple[bool, str]:
        """
        Validate if the guess word beats the current word using AI
        Returns (is_valid, explanation)
        """
        # Check cache first
        word_pair = f"{current_word}:{guess}"
        cached_verdict = cache_manager.get_cached_verdict(word_pair)
        if cached_verdict is not None:
            return cached_verdict, "Cached verdict"
            
        # Prepare the prompt
        prompt = f"""
        In the game "What Beats Rock", players try to find words that "beat" the current word.
        For example, "paper" beats "rock" because paper can wrap around rock.
        
        Current word: {current_word}
        Guess: {guess}
        
        Does the guess word beat the current word in a creative and logical way?
        Respond with only "YES" or "NO" followed by a brief explanation.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a game judge for 'What Beats Rock'. Be creative but logical in your assessments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            result = response.choices[0].message.content.strip()
            verdict = result.split()[0].upper() == "YES"
            explanation = " ".join(result.split()[1:])
            
            # Cache the result
            cache_manager.cache_verdict(word_pair, (verdict, explanation))
            
            return verdict, explanation
            
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return False, "Error validating word pair"

# Create a singleton instance
ai_client = AIClient() 