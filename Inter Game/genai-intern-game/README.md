# What Beats Rock - A Word Association Game

A minimum-viable clone of the "What Beats Rock" game, where players make word associations and the AI validates their choices.

## Features

- Word association gameplay
- AI-powered validation using OpenAI
- Rate limiting and caching
- Content moderation
- Global guess counter
- Modern, responsive UI
- Containerized deployment

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache**: Redis
- **AI**: OpenAI API
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker, Docker Compose

## Project Structure

```
genai-intern-game/
├── backend/
│   ├── api/           # API routes and endpoints
│   ├── core/          # Core game logic and services
│   ├── db/            # Database models and migrations
│   └── main.py        # Application entry point
├── frontend/          # Frontend assets
├── tests/             # Test files
├── Dockerfile         # Container configuration
└── docker-compose.yml # Service orchestration
```

## Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example`
3. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Access the game at `http://localhost:8000`

## Development

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

- `POST /api/game/start` - Start a new game
- `POST /api/game/guess` - Make a guess
- `GET /api/game/history` - Get game history

## License

MIT 