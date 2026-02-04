# BoardGame Recommender System

A professional-grade recommendation engine for board games, built to demonstrate full-stack development skills, machine learning implementation, and DevOps practices.

## Project Overview

This system helps users discover board games they'll love based on their preferences, ratings, and similar users' tastes. Built as a portfolio piece showcasing modern software engineering practices.

## Features (Planned)

### Core Features
- **User Profile Management** - Create profiles and track game preferences
- **Game Database** - Comprehensive board game catalog with rich metadata
- **Multiple Recommendation Algorithms**:
  - Content-based filtering (games similar to ones you like)
  - Collaborative filtering (find games liked by similar users)
  - Hybrid approach combining both methods
- **Rating System** - Rate games and improve recommendations
- **Search & Discovery** - Browse and filter the game catalog

### Technical Features (What Makes This Portfolio-Worthy)
- RESTful API with automatic documentation
- Type-safe frontend with TypeScript
- Comprehensive test coverage (unit, integration, e2e)
- Docker containerization
- CI/CD pipeline
- Cloud deployment
- Performance optimization with caching
- Database migrations and proper ORM usage

## Tech Stack

### Backend
- **Python 3.11+** with **FastAPI** - Modern async API framework
- **PostgreSQL** - Relational database
- **Redis** - Caching layer
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **scikit-learn** / **pandas** - ML and data processing

### Frontend
- **TypeScript** - Type safety
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **React Query** - Data fetching and caching
- **React Router** - Navigation

### DevOps & Tools
- **Docker & Docker Compose** - Containerization
- **pytest** - Backend testing
- **Vitest** - Frontend testing
- **GitHub Actions** - CI/CD
- **Ruff** - Python linting
- **ESLint** - TypeScript linting
- **Black** - Python formatting
- **Prettier** - TypeScript formatting

## Project Structure

```
boardgame-recommender/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration, security
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── ml/             # Recommendation engine
│   ├── tests/              # Backend tests
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API client
│   │   └── types/          # TypeScript types
│   └── tests/              # Frontend tests
├── docker/                 # Docker configurations
├── docs/                   # Additional documentation
│   ├── REQUIREMENTS.md     # Detailed requirements
│   ├── ARCHITECTURE.md     # System design
│   └── API.md              # API documentation
└── scripts/                # Utility scripts
```

## Development Phases

This project is being built iteratively to demonstrate professional development practices:

- [ ] **Phase 1**: Requirements, architecture, and project setup
- [ ] **Phase 2**: Backend API and database
- [ ] **Phase 3**: Data ingestion from BoardGameGeek
- [ ] **Phase 4**: Basic recommendation engine
- [ ] **Phase 5**: Frontend development
- [ ] **Phase 6**: Advanced recommendations and ML
- [ ] **Phase 7**: Testing and quality assurance
- [ ] **Phase 8**: DevOps and deployment
- [ ] **Phase 9**: Performance optimization
- [ ] **Phase 10**: Documentation and portfolio presentation

## Getting Started

(Instructions will be added as the project develops)

## Learning Outcomes

This project demonstrates proficiency in:
- Full-stack web development
- RESTful API design
- Database design and optimization
- Machine learning and recommendation systems
- Test-driven development
- Docker and containerization
- CI/CD pipelines
- Cloud deployment
- Professional code organization

## License

MIT License (for portfolio purposes)

## Author

Built as a portfolio project to demonstrate professional software engineering practices.
