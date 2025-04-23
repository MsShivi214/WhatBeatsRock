import re
from typing import List, Pattern

class ContentModerator:
    def __init__(self):
        self.profane_patterns: List[Pattern] = [
            re.compile(r'\b(shit|fuck|ass|bitch|damn|hell)\b', re.IGNORECASE),
            re.compile(r'\b\d{4,}\b'),  # Numbers with 4 or more digits
            re.compile(r'[^\w\s]'),     # Special characters
        ]
        
        # Add more patterns as needed
        self.disallowed_patterns: List[Pattern] = [
            re.compile(r'\b(hack|exploit|cheat)\b', re.IGNORECASE),
            re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
        ]
    
    def is_profane(self, text: str) -> bool:
        """Check if text contains profanity"""
        return any(pattern.search(text) for pattern in self.profane_patterns)
    
    def is_disallowed(self, text: str) -> bool:
        """Check if text contains disallowed content"""
        return any(pattern.search(text) for pattern in self.disallowed_patterns)
    
    def validate_content(self, text: str) -> tuple[bool, str]:
        """
        Validate content against moderation rules
        Returns (is_valid, reason)
        """
        if not text or len(text) > 50:
            return False, "Content length invalid"
        
        if self.is_profane(text):
            return False, "Content contains profanity"
        
        if self.is_disallowed(text):
            return False, "Content contains disallowed terms"
        
        return True, "Content is valid"

# Create a singleton instance
content_moderator = ContentModerator() 