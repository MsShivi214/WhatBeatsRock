# What Beats Rock Game

A fun word association game where players try to find words that "beat" the current word, powered by Generative AI.

## Features

- Simple and intuitive gameplay
- AI-powered word validation
- Real-time scoring and history tracking
- Caching layer for improved performance
- Docker-based deployment
- Rate limiting and concurrency handling

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- OpenAI API key (for AI validation)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd what-beats-rock
```

2. Create a `.env` file in the root directory with the following variables:
```
OPENAI_API_KEY=your_api_key_here
REDIS_URL=redis://redis:6379
DATABASE_URL=postgresql://postgres:postgres@db:5432/rockgame
```

3. Start the services using Docker Compose:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## How to Play

1. Start with the word "rock"
2. Enter a word you think "beats" the current word
3. The AI will validate your guess
4. If valid, your score increases and the word becomes the new challenge
5. If you repeat a word, the game ends
6. Try to get the highest score possible!

## Architecture

The application is built using:
- FastAPI for the backend
- PostgreSQL for persistent storage
- Redis for caching
- OpenAI API for word validation
- HTML/CSS/JavaScript for the frontend

### Key Components

- **Game Logic**: Handles word validation and scoring
- **Caching Layer**: Stores AI validation results
- **Database**: Tracks game history and global statistics
- **Rate Limiting**: Prevents abuse and ensures fair play

## Development

To run the application locally:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the services:
```bash
docker-compose up -d redis db
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Testing

Run the test suite:
```bash
pytest
```

## License

MIT License 