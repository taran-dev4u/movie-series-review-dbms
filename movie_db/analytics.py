"""Relational analytics engine: Bayesian weighted rating, genre aggregations, and collaborative filtering."""

from __future__ import annotations

from typing import Any

import numpy as np

from movie_db.manager import MovieDatabaseManager


class MovieAnalyticsEngine:
    """Performs SQL aggregations, Bayesian score rankings, and user recommendation algorithms."""

    def __init__(self, manager: MovieDatabaseManager) -> None:
        self.manager = manager

    def get_overall_stats(self) -> dict[str, Any]:
        """Compute top-level summary metrics across the database."""
        conn = self.manager.get_connection()
        total_users = conn.execute("SELECT COUNT(*) as c FROM users;").fetchone()["c"]
        total_movies = conn.execute("SELECT COUNT(*) as c FROM movies;").fetchone()["c"]
        total_reviews = conn.execute("SELECT COUNT(*) as c FROM reviews;").fetchone()["c"]
        avg_rating = conn.execute("SELECT AVG(rating) as a FROM reviews;").fetchone()["a"] or 0.0

        return {
            "total_users": total_users,
            "total_movies": total_movies,
            "total_reviews": total_reviews,
            "average_rating": round(float(avg_rating), 2),
        }

    def get_top_rated_movies(
        self,
        limit: int = 10,
        genre: str | None = None,
        bayesian_m: int = 2,
    ) -> list[dict[str, Any]]:
        """Rank movies using IMDb-style Bayesian weighted average ratings.

        Formula: WR = (v / (v + m)) * R + (m / (v + m)) * C
        where:
            v = review count for movie
            m = minimum threshold weight (default 2)
            R = arithmetic mean rating of movie
            C = global mean rating across whole catalog
        """
        conn = self.manager.get_connection()

        # Global average rating (C)
        global_avg_row = conn.execute("SELECT AVG(rating) as c FROM reviews;").fetchone()
        c = float(global_avg_row["c"]) if global_avg_row and global_avg_row["c"] else 7.0

        genre_filter = ""
        params: list[Any] = []
        if genre:
            genre_filter = """
            JOIN movie_genres mg ON m.movie_id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.genre_id
            WHERE g.genre_name = ?
            """
            params.append(genre)

        query = f"""
        SELECT
            m.movie_id,
            m.title,
            m.release_year,
            m.director,
            COUNT(r.review_id) as review_count,
            AVG(r.rating) as avg_rating
        FROM movies m
        LEFT JOIN reviews r ON m.movie_id = r.movie_id
        {genre_filter}
        GROUP BY m.movie_id
        """

        rows = conn.execute(query, params).fetchall()

        results = []
        for row in rows:
            v = int(row["review_count"])
            r = float(row["avg_rating"]) if row["avg_rating"] is not None else c
            # Bayesian weighted formula
            wr = (v / (v + bayesian_m)) * r + (bayesian_m / (v + bayesian_m)) * c

            results.append({
                "movie_id": row["movie_id"],
                "title": row["title"],
                "release_year": row["release_year"],
                "director": row["director"],
                "review_count": v,
                "raw_avg_rating": round(r, 2),
                "bayesian_score": round(wr, 3),
            })

        # Sort by bayesian_score descending
        results.sort(key=lambda x: x["bayesian_score"], reverse=True)
        return results[:limit]

    def get_genre_analytics(self) -> list[dict[str, Any]]:
        """Compute performance metrics grouped by film genre."""
        conn = self.manager.get_connection()
        query = """
        SELECT
            g.genre_name,
            COUNT(DISTINCT m.movie_id) as movie_count,
            COUNT(r.review_id) as review_count,
            AVG(r.rating) as avg_rating
        FROM genres g
        JOIN movie_genres mg ON g.genre_id = mg.genre_id
        JOIN movies m ON mg.movie_id = m.movie_id
        LEFT JOIN reviews r ON m.movie_id = r.movie_id
        GROUP BY g.genre_id
        ORDER BY review_count DESC, avg_rating DESC;
        """
        rows = conn.execute(query).fetchall()

        return [
            {
                "genre": row["genre_name"],
                "movie_count": row["movie_count"],
                "review_count": row["review_count"],
                "avg_rating": round(float(row["avg_rating"]), 2) if row["avg_rating"] else 0.0,
            }
            for row in rows
        ]

    def get_user_recommendations(self, user_id: int, limit: int = 5) -> list[dict[str, Any]]:
        """Generate personalized movie recommendations via user-based collaborative filtering."""
        conn = self.manager.get_connection()

        # Get all reviews by target user
        user_reviews = conn.execute(
            "SELECT movie_id, rating FROM reviews WHERE user_id = ?;",
            (user_id,),
        ).fetchall()

        if not user_reviews:
            # Fallback to top-rated movies if user has no rating history
            top_movies = self.get_top_rated_movies(limit=limit)
            return [
                {
                    "movie_id": m["movie_id"],
                    "title": m["title"],
                    "predicted_rating": m["bayesian_score"],
                    "reason": "Popularity fallback (unrated user)",
                }
                for m in top_movies
            ]

        user_ratings_map = {row["movie_id"]: float(row["rating"]) for row in user_reviews}
        reviewed_movie_ids = set(user_ratings_map.keys())

        # Retrieve all reviews by other users
        other_reviews = conn.execute(
            "SELECT user_id, movie_id, rating FROM reviews WHERE user_id != ?;",
            (user_id,),
        ).fetchall()

        # Group ratings by other user
        other_users_ratings: dict[int, dict[int, float]] = {}
        for row in other_reviews:
            u = row["user_id"]
            other_users_ratings.setdefault(u, {})[row["movie_id"]] = float(row["rating"])

        # Compute cosine similarity between target user and other users over common movies
        user_similarities: list[tuple[int, float]] = []
        for other_u, ratings_dict in other_users_ratings.items():
            common_movies = set(ratings_dict.keys()).intersection(reviewed_movie_ids)
            if not common_movies:
                continue

            v1 = np.array([user_ratings_map[m] for m in common_movies])
            v2 = np.array([ratings_dict[m] for m in common_movies])

            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            sim = float(np.dot(v1, v2) / (norm1 * norm2)) if (norm1 > 0 and norm2 > 0) else 0.0

            if sim > 0:
                user_similarities.append((other_u, sim))

        # Sort neighbors by similarity
        user_similarities.sort(key=lambda x: x[1], reverse=True)

        # Candidate movies: unreviewed movies rated by similar users
        candidate_scores: dict[int, list[tuple[float, float]]] = {}
        for other_u, sim in user_similarities:
            for m_id, r in other_users_ratings[other_u].items():
                if m_id not in reviewed_movie_ids:
                    candidate_scores.setdefault(m_id, []).append((r, sim))

        recommendations = []
        for m_id, ratings_and_weights in candidate_scores.items():
            total_weighted_rating = sum(r * w for r, w in ratings_and_weights)
            total_weight = sum(w for _, w in ratings_and_weights)
            pred_rating = total_weighted_rating / total_weight if total_weight > 0 else 7.0

            movie_info = conn.execute(
                "SELECT title, release_year, director FROM movies WHERE movie_id = ?;",
                (m_id,),
            ).fetchone()

            recommendations.append({
                "movie_id": m_id,
                "title": movie_info["title"],
                "release_year": movie_info["release_year"],
                "director": movie_info["director"],
                "predicted_rating": round(pred_rating, 2),
                "neighbor_votes": len(ratings_and_weights),
            })

        recommendations.sort(key=lambda x: x["predicted_rating"], reverse=True)
        return recommendations[:limit]
