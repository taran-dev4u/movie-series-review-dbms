import pytest

from movie_db.analytics import MovieAnalyticsEngine
from movie_db.manager import MovieDatabaseManager


@pytest.fixture
def seeded_db():
    mgr = MovieDatabaseManager(":memory:")
    mgr.seed_default_catalog()
    yield mgr
    mgr.close()


def test_overall_stats(seeded_db):
    engine = MovieAnalyticsEngine(seeded_db)
    stats = engine.get_overall_stats()
    assert stats["total_users"] == 5
    assert stats["total_movies"] == 6
    assert stats["total_reviews"] == 14
    assert 8.0 <= stats["average_rating"] <= 10.0


def test_top_rated_movies(seeded_db):
    engine = MovieAnalyticsEngine(seeded_db)
    top_all = engine.get_top_rated_movies(limit=3)
    assert len(top_all) == 3
    # Check that bayesian score is within plausible rating bounds
    assert 7.0 <= top_all[0]["bayesian_score"] <= 10.0

    # Test genre filtering
    sci_fi_movies = engine.get_top_rated_movies(genre="Sci-Fi")
    for m in sci_fi_movies:
        assert m["title"] in ["Inception", "Interstellar"]


def test_genre_analytics(seeded_db):
    engine = MovieAnalyticsEngine(seeded_db)
    genre_stats = engine.get_genre_analytics()
    assert len(genre_stats) > 0
    genres = [g["genre"] for g in genre_stats]
    assert "Drama" in genres
    assert "Action" in genres
    assert "Sci-Fi" in genres


def test_user_recommendations(seeded_db):
    engine = MovieAnalyticsEngine(seeded_db)
    # User 4 (retro_movie_fan) has reviewed Pulp Fiction and Inception
    recs = engine.get_user_recommendations(user_id=4, limit=3)
    assert len(recs) > 0
    # Recommendations should suggest movies user hasn't reviewed yet
    rec_titles = [r["title"] for r in recs]
    assert "Inception" not in rec_titles
    assert "Pulp Fiction" not in rec_titles
