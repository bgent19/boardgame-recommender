# System Architecture

## Overview

The BoardGame Recommender System follows a modern three-tier architecture:

1. **Presentation Layer** - React SPA
2. **Application Layer** - FastAPI REST API
3. **Data Layer** - PostgreSQL + Redis

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  React SPA (TypeScript)                               │  │
│  │  - Components (UI)                                    │  │
│  │  - React Query (State & Caching)                      │  │
│  │  - React Router (Navigation)                          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND API                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI Application                                  │  │
│  │  ├── API Routes (Controllers)                         │  │
│  │  ├── Services (Business Logic)                        │  │
│  │  │   ├── User Service                                 │  │
│  │  │   ├── Game Service                                 │  │
│  │  │   ├── Rating Service                               │  │
│  │  │   └── Recommendation Service                       │  │
│  │  ├── ML Module                                        │  │
│  │  │   ├── Content-Based Engine                         │  │
│  │  │   ├── Collaborative Engine                         │  │
│  │  │   └── Hybrid Engine                                │  │
│  │  └── Data Access Layer                                │  │
│  │      └── SQLAlchemy ORM                               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬───────────────────────────┬────────────────────┘
             │                           │
             ▼                           ▼
┌─────────────────────────┐   ┌──────────────────────┐
│   PostgreSQL             │   │      Redis           │
│   - Users                │   │   - Session Store    │
│   - Games                │   │   - API Cache        │
│   - Ratings              │   │   - Recommendation   │
│   - Categories           │   │     Cache            │
│   - Mechanics            │   └──────────────────────┘
└─────────────────────────┘
             ▲
             │
┌────────────┴────────────┐
│  Data Ingestion Service  │
│  (BoardGameGeek API)     │
└─────────────────────────┘
```

## Component Details

### Frontend (React SPA)

**Responsibilities:**
- User interface and interactions
- Client-side routing
- Form validation
- API communication
- Client-side caching

**Key Technologies:**
- **React 18**: Component library with hooks
- **TypeScript**: Type safety and better IDE support
- **Vite**: Fast development and optimized builds
- **TailwindCSS**: Utility-first styling
- **React Query**: Server state management and caching
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Zod**: Runtime validation

**Structure:**
```
frontend/src/
├── components/       # Reusable UI components
│   ├── common/       # Buttons, inputs, cards
│   ├── game/         # Game card, detail, list
│   └── user/         # Profile, rating components
├── pages/            # Route-level components
│   ├── Home.tsx
│   ├── GameDetail.tsx
│   ├── Recommendations.tsx
│   └── Profile.tsx
├── hooks/            # Custom React hooks
├── services/         # API client functions
├── types/            # TypeScript definitions
├── utils/            # Helper functions
└── App.tsx           # Root component
```

### Backend API (FastAPI)

**Responsibilities:**
- Authentication and authorization
- Business logic enforcement
- Data validation
- Database operations
- Recommendation generation
- External API integration

**Key Technologies:**
- **FastAPI**: Modern, fast async framework
- **SQLAlchemy 2.0**: ORM with async support
- **Alembic**: Database migrations
- **Pydantic**: Data validation and serialization
- **Python-Jose**: JWT handling
- **Passlib**: Password hashing
- **scikit-learn**: ML algorithms
- **pandas**: Data manipulation
- **Redis-py**: Caching client

**Structure:**
```
backend/app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py
│       │   ├── users.py
│       │   ├── games.py
│       │   ├── ratings.py
│       │   └── recommendations.py
│       └── router.py
├── core/
│   ├── config.py      # Settings and environment
│   ├── security.py    # JWT, password hashing
│   └── deps.py        # Dependency injection
├── models/            # SQLAlchemy models
│   ├── user.py
│   ├── game.py
│   ├── rating.py
│   └── associations.py
├── schemas/           # Pydantic schemas
│   ├── user.py
│   ├── game.py
│   └── rating.py
├── services/          # Business logic
│   ├── user_service.py
│   ├── game_service.py
│   ├── rating_service.py
│   └── recommendation_service.py
├── ml/                # Recommendation engines
│   ├── content_based.py
│   ├── collaborative.py
│   ├── hybrid.py
│   └── utils.py
├── db/
│   ├── session.py     # Database connection
│   └── init_db.py     # Database initialization
└── main.py            # Application entry point
```

### Database Layer (PostgreSQL)

**Schema Design:**

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Games table
CREATE TABLE games (
    id INTEGER PRIMARY KEY,  -- BGG ID
    name VARCHAR(255) NOT NULL,
    year_published INTEGER,
    description TEXT,
    image_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    min_players INTEGER,
    max_players INTEGER,
    min_playtime INTEGER,
    max_playtime INTEGER,
    min_age INTEGER,
    average_rating DECIMAL(3,2),
    rating_count INTEGER,
    weight DECIMAL(3,2),  -- Complexity
    rank INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Mechanics table
CREATE TABLE mechanics (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Game-Category association (many-to-many)
CREATE TABLE game_categories (
    game_id INTEGER REFERENCES games(id),
    category_id INTEGER REFERENCES categories(id),
    PRIMARY KEY (game_id, category_id)
);

-- Game-Mechanic association (many-to-many)
CREATE TABLE game_mechanics (
    game_id INTEGER REFERENCES games(id),
    mechanic_id INTEGER REFERENCES mechanics(id),
    PRIMARY KEY (game_id, mechanic_id)
);

-- Ratings table
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    rating DECIMAL(3,1) CHECK (rating >= 1 AND rating <= 10),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (user_id, game_id)
);

-- Indexes for performance
CREATE INDEX idx_ratings_user_id ON ratings(user_id);
CREATE INDEX idx_ratings_game_id ON ratings(game_id);
CREATE INDEX idx_games_rank ON games(rank);
CREATE INDEX idx_games_rating ON games(average_rating DESC);
```

### Caching Layer (Redis)

**Cache Strategy:**

1. **Session Storage**
   - JWT token blacklist (logout)
   - Key: `session:{user_id}`
   - TTL: Token expiration time

2. **Game Data Cache**
   - Popular games list
   - Key: `games:popular`
   - TTL: 1 hour

3. **Recommendation Cache**
   - User recommendations
   - Key: `recommendations:{user_id}:{algorithm}`
   - TTL: 1 hour (invalidate on new rating)

4. **API Response Cache**
   - Game details
   - Key: `game:{game_id}`
   - TTL: 24 hours

## Data Flow Examples

### User Rates a Game

```
1. Frontend: User submits rating (POST /api/v1/ratings)
2. API: Validate JWT token
3. API: Validate rating data (Pydantic schema)
4. Service: Check if user has existing rating for this game
5. Service: Create/update rating in database
6. Service: Invalidate recommendation cache for this user
7. API: Return success response
8. Frontend: Update UI and refetch recommendations
```

### Get Recommendations

```
1. Frontend: Request recommendations (GET /api/v1/recommendations)
2. API: Validate JWT token
3. Service: Check Redis cache for recommendations
4. If cache miss:
   a. Fetch user's ratings from database
   b. Run recommendation algorithm (content-based or collaborative)
   c. Store results in Redis cache
5. API: Return recommendations
6. Frontend: Display game recommendations
```

### Search Games

```
1. Frontend: User types in search (GET /api/v1/games?search=catan)
2. API: Validate query parameters
3. Service: Build SQL query with filters
4. Database: Execute full-text search with indexes
5. Service: Return paginated results
6. API: Serialize response
7. Frontend: Display results
```

## API Design Principles

### RESTful Conventions

```
GET    /api/v1/games           # List games
GET    /api/v1/games/{id}      # Get game details
POST   /api/v1/games           # Create game (admin only)
PUT    /api/v1/games/{id}      # Update game (admin only)
DELETE /api/v1/games/{id}      # Delete game (admin only)

POST   /api/v1/auth/register   # Register user
POST   /api/v1/auth/login      # Login user
POST   /api/v1/auth/logout     # Logout user

GET    /api/v1/users/me        # Get current user
PUT    /api/v1/users/me        # Update current user

GET    /api/v1/ratings         # Get user's ratings
POST   /api/v1/ratings         # Create rating
PUT    /api/v1/ratings/{id}    # Update rating
DELETE /api/v1/ratings/{id}    # Delete rating

GET    /api/v1/recommendations # Get recommendations
```

### Response Format

```json
{
  "data": { ... },       // Success response data
  "meta": {              // Metadata (pagination, etc.)
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

```json
{
  "error": {             // Error response
    "code": "VALIDATION_ERROR",
    "message": "Invalid rating value",
    "details": { ... }
  }
}
```

## Recommendation Algorithm Evolution

### Phase 1: Content-Based Filtering

**Approach:** Recommend games similar to user's highly-rated games

**Algorithm:**
1. Get user's games rated >= 7
2. Extract features: categories, mechanics, weight, player count
3. Create feature vectors for all games
4. Calculate cosine similarity
5. Recommend top-N similar games user hasn't rated

**Pros:** Works for new users with few ratings
**Cons:** Limited diversity, can't discover different types of games

### Phase 2: Collaborative Filtering

**Approach:** Recommend games liked by similar users

**Algorithm:**
1. Build user-item rating matrix
2. Apply matrix factorization (SVD) or k-NN
3. Predict ratings for unrated games
4. Recommend top-N predicted ratings

**Pros:** Discovers unexpected recommendations
**Cons:** Cold start problem for new users

### Phase 3: Hybrid Approach

**Approach:** Combine both methods with weighting

**Algorithm:**
1. Calculate content-based score
2. Calculate collaborative score
3. Weighted average based on:
   - Number of user ratings (more ratings → favor collaborative)
   - Confidence in predictions
4. Recommend top-N combined scores

**Pros:** Best of both worlds
**Cons:** More complex to tune

## Security Architecture

### Authentication Flow

```
1. User registers → Store hashed password (bcrypt)
2. User logs in → Verify password → Generate JWT
3. JWT contains: user_id, expiration
4. JWT sent in Authorization header: "Bearer <token>"
5. API validates JWT on protected routes
6. Logout → Add token to Redis blacklist
```

### Security Measures

- **Password Storage**: bcrypt with salt (cost factor: 12)
- **JWT**: HS256 algorithm, 24-hour expiration
- **SQL Injection**: ORM with parameterized queries
- **XSS**: React escapes by default, CSP headers
- **CORS**: Configured allowlist for frontend domain
- **Rate Limiting**: 100 requests per minute per IP
- **HTTPS**: Required in production
- **Environment Secrets**: Never committed to git

## Deployment Architecture

### Development

```
Docker Compose with:
- Backend container (hot reload)
- Frontend container (Vite dev server)
- PostgreSQL container
- Redis container
```

### Production (Minimal)

```
Cloud Provider (Railway/Render):
- Backend: Docker container
- Frontend: Static files on CDN
- Database: Managed PostgreSQL
- Cache: Managed Redis
- HTTPS: Automatic certificates
```

### Production (Advanced - Future)

```
AWS/GCP:
- Backend: ECS/Cloud Run (multiple instances)
- Frontend: S3/Cloud Storage + CloudFront/CDN
- Database: RDS/Cloud SQL (with replicas)
- Cache: ElastiCache/Memorystore
- Load Balancer: ALB/Cloud Load Balancer
- Monitoring: CloudWatch/Cloud Monitoring
```

## Monitoring & Observability

### Logging Strategy

- **Structured JSON logs** for machine parsing
- **Log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log aggregation**: CloudWatch, DataDog, or Sentry

### Metrics to Track

- Request count by endpoint
- Response times (p50, p95, p99)
- Error rates
- Database query performance
- Cache hit rates
- Recommendation generation time

### Health Checks

```
GET /health           # Basic health check
GET /health/detailed  # Check database, redis, etc.
```

## Scalability Considerations

### Horizontal Scaling

- **Stateless API** - Any instance can handle any request
- **Database connection pooling** - Limit connections per instance
- **Cache warming** - Pre-populate common queries
- **CDN for static assets** - Reduce server load

### Database Optimization

- **Indexes** on frequently queried columns
- **Read replicas** for analytics queries
- **Connection pooling** (e.g., PgBouncer)
- **Query optimization** with EXPLAIN ANALYZE

### Caching Strategy

- **Cache expensive operations** (recommendations, aggregations)
- **Cache invalidation** on data changes
- **TTL-based expiration** for stale data tolerance
- **Cache aside pattern** (check cache → miss → query DB → store in cache)

## Development Workflow

### Local Development

```bash
# Start all services
docker-compose up

# Run backend tests
cd backend && pytest

# Run frontend tests
cd frontend && npm test

# Database migrations
cd backend && alembic upgrade head
```

### CI/CD Pipeline

```yaml
On Push:
1. Lint code (ruff, eslint)
2. Run tests (pytest, vitest)
3. Build Docker images
4. Push to registry

On Main Branch:
5. Deploy to staging
6. Run integration tests
7. Deploy to production (manual approval)
```

## Design Decisions & Trade-offs

### Why FastAPI over Flask/Django?
- **Async support** for better performance
- **Automatic API docs** (OpenAPI/Swagger)
- **Type hints** for better code quality
- **Modern and actively developed**

### Why PostgreSQL over MongoDB?
- **Structured data** with clear relationships
- **ACID compliance** for data integrity
- **Rich query capabilities** (joins, aggregations)
- **Industry standard** for web applications

### Why React over Vue/Angular?
- **Largest ecosystem** and job market
- **Component model** well-suited for this app
- **Strong TypeScript support**
- **Most recognizable for portfolio**

### Why Content-Based + Collaborative over Deep Learning?
- **Interpretable** recommendations
- **Less data required** for good results
- **Faster** training and inference
- **Easier to debug** and explain
- **Portfolio demonstrates understanding** of fundamentals

## Next Steps

Once this architecture is approved, we'll begin implementation in this order:

1. Set up project structure and dependencies
2. Implement database models and migrations
3. Build authentication system
4. Create game and rating endpoints
5. Develop content-based recommendation engine
6. Build frontend components
7. Add collaborative filtering
8. Implement caching
9. Write comprehensive tests
10. Set up CI/CD and deployment
