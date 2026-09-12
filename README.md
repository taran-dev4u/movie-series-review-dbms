# Movie & Series Review Relational DBMS

Normalized relational database management, Bayesian rating analytics, and collaborative recommendation engine for film and television reviews.

## Architecture & Modules

The repository provides a modular Python package (`movie_db`) alongside the underlying SQL schema:

- `movie_db.schema`: Normalized relational schema (BCNF) covering `users`, `movies`, `genres`, `movie_genres`, `reviews`, and `watchlists`, with foreign key constraints, cascade deletions, and index optimization.
- `movie_db.manager.MovieDatabaseManager`: Connection handling, automated schema provisioning, and transactional CRUD operations for users, titles, and review submissions.
- `movie_db.analytics.MovieAnalyticsEngine`:
  - **Bayesian Weighted Average Rating:** Calculates calibrated movie scores using IMDb-style formulation:
    \[
    \text{WR} = \frac{v}{v + m} R + \frac{m}{v + m} C
    \]
    where $v$ is review count, $m$ is minimum threshold weight, $R$ is mean movie rating, and $C$ is global mean catalog rating.
  - **Genre Analytics:** Aggregates review volumes, title counts, and average ratings across categories.
  - **User Collaborative Filtering:** Recommends unreviewed movies based on cosine rating similarity across shared reviewed titles.
- `movie_db.cli`: Command-line tool with `init`, `top`, `genres`, `recommend`, and `stats` subcommands.

## Repository Layout

- `movie_db/` — Core Python database and analytics package.
- `movie-review-app/` — Historical PHP/MySQL web portal and baseline SQL schemas.
- `academic_dbms_report/movie_dbms_project_report.pdf` — Academic DBMS report with entity-relationship (ER) diagrams, normalization proofs, and query plans.
- `tests/` — Automated pytest test suite covering schema constraints, cascade behavior, and recommendation logic.

## Installation

Requires Python 3.9+.

```bash
git clone https://github.com/taran-dev4u/movie-series-review-dbms.git
cd movie-series-review-dbms
pip install -e .
```

To install test dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from movie_db import MovieDatabaseManager, MovieAnalyticsEngine

# Initialize database manager with file or in-memory instance
mgr = MovieDatabaseManager("movies.db")
mgr.seed_default_catalog()

engine = MovieAnalyticsEngine(mgr)

# Get top-rated movies weighted by Bayesian formula
top_movies = engine.get_top_rated_movies(limit=5, genre="Sci-Fi")
for m in top_movies:
    print(f"{m['title']} ({m['release_year']}) — Score: {m['bayesian_score']}")

# Personalized collaborative filtering recommendations
recommendations = engine.get_user_recommendations(user_id=4, limit=3)
for rec in recommendations:
    print(f"Recommended: {rec['title']} (Predicted: {rec['predicted_rating']})")

mgr.close()
```

### Command-Line Interface

Initialize and seed the database:

```bash
movie-db --db movies.db init --seed
```

Query top rated titles:

```bash
movie-db --db movies.db top --limit 5
```

Filter top titles by genre with JSON output:

```bash
movie-db --db movies.db top --genre Action --json
```

Generate recommendations for a user:

```bash
movie-db --db movies.db recommend --user-id 2
```

Inspect database summary metrics:

```bash
movie-db --db movies.db stats --json
```

## Testing

Run the test suite verifying relational constraints, cascade deletions, rating calculations, and CLI commands:

```bash
pytest tests/ -v
```

Linting:

```bash
ruff check .
```
