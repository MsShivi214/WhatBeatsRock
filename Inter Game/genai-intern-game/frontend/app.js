class Game {
    constructor() {
        this.score = 0;
        this.currentWord = 'rock';
        this.guesses = [];
        this.isGameOver = false;
        
        this.initializeElements();
        this.attachEventListeners();
        this.startNewGame();
    }
    
    initializeElements() {
        this.currentWordElement = document.getElementById('currentWord');
        this.scoreElement = document.getElementById('score');
        this.guessInput = document.getElementById('guessInput');
        this.submitButton = document.getElementById('submitButton');
        this.messageElement = document.getElementById('message');
        this.historyList = document.getElementById('guessHistory');
    }
    
    attachEventListeners() {
        this.submitButton.addEventListener('click', () => this.makeGuess());
        this.guessInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.makeGuess();
            }
        });
    }
    
    async makeGuess() {
        if (this.isGameOver) return;
        
        const guess = this.guessInput.value.trim();
        if (!guess) return;
        
        try {
            const response = await fetch('/api/game/guess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ guess }),
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.handleSuccess(data);
            } else {
                this.handleError(data);
            }
        } catch (error) {
            console.error('Error:', error);
            this.showMessage('An error occurred. Please try again.', 'error');
        }
        
        this.guessInput.value = '';
    }
    
    handleSuccess(data) {
        this.score = data.score;
        this.currentWord = data.current_word;
        this.guesses.push(data.current_word);
        
        this.updateUI();
        this.showMessage(data.message, 'success');
        this.createConfetti();
    }
    
    handleError(data) {
        this.isGameOver = true;
        this.showMessage(data.detail, 'error');
        
        setTimeout(() => {
            this.startNewGame();
        }, 2000);
    }
    
    async startNewGame() {
        try {
            const response = await fetch('/api/game/start');
            const data = await response.json();
            
            this.score = data.score;
            this.currentWord = data.current_word;
            this.guesses = data.guesses;
            this.isGameOver = false;
            
            this.updateUI();
            this.showMessage('', '');
        } catch (error) {
            console.error('Error:', error);
            this.showMessage('Failed to start new game', 'error');
        }
    }
    
    updateUI() {
        this.currentWordElement.textContent = this.currentWord;
        this.scoreElement.textContent = this.score;
        this.updateHistory();
    }
    
    updateHistory() {
        this.historyList.innerHTML = '';
        this.guesses.forEach(guess => {
            const li = document.createElement('li');
            li.textContent = guess;
            this.historyList.appendChild(li);
        });
    }
    
    showMessage(message, type) {
        this.messageElement.textContent = message;
        this.messageElement.className = `message ${type}`;
    }
    
    createConfetti() {
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.animationDelay = Math.random() * 2 + 's';
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 3000);
        }
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new Game();
}); 