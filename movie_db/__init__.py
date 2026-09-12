"""Movie and TV series review relational database management and analytics system."""

from movie_db.analytics import MovieAnalyticsEngine
from movie_db.manager import MovieDatabaseManager
from movie_db.schema import SCHEMA_SQL

__all__ = [
    "SCHEMA_SQL",
    "MovieAnalyticsEngine",
    "MovieDatabaseManager",
]
