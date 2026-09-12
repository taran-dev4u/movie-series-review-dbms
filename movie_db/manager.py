"""Database manager handling connections, schema migration, and CRUD operations."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from movie_db.schema import SCHEMA_SQL


class MovieDatabaseManager:
    """Manages SQLite database connections, schema provisioning, and transactional records."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.db_path = str(db_path)
        self._conn: sqlite3.Connection | None = None

    def get_connection(self) -> sqlite3.Connection:
        """Establish or return an active connection with foreign key enforcement."""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON;")
        return self._conn

    def close(self) -> None:
        """Close the active database connection if open."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def init_schema(self) -> None:
        """Execute schema migrations to build tables and indices."""
        conn = self.get_connection()
        conn.executescript(SCHEMA_SQL)
        conn.commit()

    def add_user(self, username: str, email: str) -> int:
        """Create a new user account."""
        conn = self.get_connection()
        cur = conn.execute(
            "INSERT INTO users (username, email) VALUES (?, ?);",
            (username, email),
        )
        conn.commit()
        return cur.lastrowid

    def add_genre(self, genre_name: str) -> int:
        """Add a genre category or retrieve existing genre_id."""
        conn = self.get_connection()
        conn.execute(
            "INSERT OR IGNORE INTO genres (genre_name) VALUES (?);",
            (genre_name,),
        )
        conn.commit()
        row = conn.execute("SELECT genre_id FROM genres WHERE genre_name = ?;", (genre_name,)).fetchone()
        return int(row["genre_id"])

    def add_movie(
        self,
        title: str,
        release_year: int,
        director: str,
        genres: list[str] | None = None,
        duration_minutes: int | None = None,
        summary: str | None = None,
    ) -> int:
        """Insert a movie and associate it with specified genre tags."""
        conn = self.get_connection()
        cur = conn.execute(
            """
            INSERT INTO movies (title, release_year, duration_minutes, director, summary)
            VALUES (?, ?, ?, ?, ?);
            """,
            (title, release_year, duration_minutes, director, summary),
        )
        movie_id = cur.lastrowid

        if genres:
            for g_name in genres:
                g_id = self.add_genre(g_name)
                conn.execute(
                    "INSERT OR IGNORE INTO movie_genres (movie_id, genre_id) VALUES (?, ?);",
                    (movie_id, g_id),
                )
        conn.commit()
        return movie_id

    def add_review(self, movie_id: int, user_id: int, rating: int, review_text: str = "") -> int:
        """Record or update a user rating and review for a movie."""
        if not (1 <= rating <= 10):
            raise ValueError(f"Rating must be between 1 and 10, got {rating}")

        conn = self.get_connection()
        cur = conn.execute(
            """
            INSERT INTO reviews (movie_id, user_id, rating, review_text)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(movie_id, user_id) DO UPDATE SET
                rating = excluded.rating,
                review_text = excluded.review_text,
                created_at = CURRENT_TIMESTAMP;
            """,
            (movie_id, user_id, rating, review_text),
        )
        conn.commit()
        return cur.lastrowid

    def seed_default_catalog(self) -> None:
        """Seed the database with a curated benchmark catalog of movies, users, and reviews."""
        self.init_schema()

        # Seed Users
        users = [
            ("cinephile_alex", "alex@cinema.org"),
            ("film_critic_sara", "sara@critics.com"),
            ("scifi_fan_mark", "mark@scifi.net"),
            ("retro_movie_fan", "retro@classicfilms.org"),
            ("casual_viewer_emma", "emma@gmail.com"),
        ]
        user_ids = [self.add_user(u, e) for u, e in users]

        # Seed Movies
        movies_data = [
            {
                "title": "The Lord of the Rings: The Fellowship of the Ring",
                "year": 2001,
                "director": "Peter Jackson",
                "duration": 178,
                "genres": ["Action", "Adventure", "Fantasy"],
                "summary": "A Hobbit sets out on a journey across Middle-earth to destroy the One Ring.",
            },
            {
                "title": "Inception",
                "year": 2010,
                "director": "Christopher Nolan",
                "duration": 148,
                "genres": ["Action", "Sci-Fi", "Thriller"],
                "summary": "A thief who steals corporate secrets through dream-sharing technology is given a task of inception.",
            },
            {
                "title": "Interstellar",
                "year": 2014,
                "director": "Christopher Nolan",
                "duration": 169,
                "genres": ["Adventure", "Drama", "Sci-Fi"],
                "summary": "A team of explorers travel through a wormhole in space to ensure humanity's survival.",
            },
            {
                "title": "Spirited Away",
                "year": 2001,
                "director": "Hayao Miyazaki",
                "duration": 125,
                "genres": ["Animation", "Adventure", "Fantasy"],
                "summary": "A young girl enters a magical world ruled by spirits and must work to save her parents.",
            },
            {
                "title": "Pulp Fiction",
                "year": 1994,
                "director": "Quentin Tarantino",
                "duration": 154,
                "genres": ["Crime", "Drama"],
                "summary": "The lives of two mob hitmen, a boxer, and a gangster's wife intertwine in four tales of violence.",
            },
            {
                "title": "Parasite",
                "year": 2019,
                "director": "Bong Joon Ho",
                "duration": 132,
                "genres": ["Drama", "Thriller"],
                "summary": "Greed and class discrimination threaten the newly formed symbiotic relationship between two families.",
            },
        ]

        movie_ids = [
            self.add_movie(
                m["title"],
                m["year"],
                m["director"],
                genres=m["genres"],
                duration_minutes=m["duration"],
                summary=m["summary"],
            )
            for m in movies_data
        ]

        # Seed Reviews
        reviews_data = [
            (movie_ids[0], user_ids[0], 10, "A timeless cinematic masterpiece."),
            (movie_ids[0], user_ids[1], 9, "Brilliant adaptation and production design."),
            (movie_ids[0], user_ids[2], 9, "Phenomenal world building."),
            (movie_ids[1], user_ids[0], 9, "Mind-bending narrative structure."),
            (movie_ids[1], user_ids[2], 10, "Incredible sci-fi concept executed with precision."),
            (movie_ids[1], user_ids[3], 8, "Complex but highly rewarding."),
            (movie_ids[2], user_ids[2], 10, "Emotional depth combined with relativistic physics."),
            (movie_ids[2], user_ids[0], 9, "Hans Zimmer score elevates the entire film."),
            (movie_ids[3], user_ids[1], 10, "Ghibli's peak animated storytelling."),
            (movie_ids[3], user_ids[4], 9, "Visually mesmerizing and deeply charming."),
            (movie_ids[4], user_ids[0], 10, "Iconic dialogue and nonlinear editing."),
            (movie_ids[4], user_ids[3], 9, "A cultural landmark of 90s cinema."),
            (movie_ids[5], user_ids[0], 10, "Impeccable social satire and tension."),
            (movie_ids[5], user_ids[1], 10, "Deserved every Oscar it won."),
        ]

        for m_id, u_id, rating, comment in reviews_data:
            self.add_review(m_id, u_id, rating, comment)
