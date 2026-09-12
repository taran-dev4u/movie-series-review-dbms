import pytest

from movie_db.manager import MovieDatabaseManager


def test_init_schema_and_tables():
    mgr = MovieDatabaseManager(":memory:")
    mgr.init_schema()
    conn = mgr.get_connection()

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    ).fetchall()
    table_names = [t["name"] for t in tables]

    assert "users" in table_names
    assert "movies" in table_names
    assert "genres" in table_names
    assert "movie_genres" in table_names
    assert "reviews" in table_names
    assert "watchlists" in table_names
    mgr.close()


def test_foreign_key_cascade_deletion():
    mgr = MovieDatabaseManager(":memory:")
    mgr.init_schema()
    conn = mgr.get_connection()

    u_id = mgr.add_user("test_user", "test@domain.com")
    m_id = mgr.add_movie("Test Movie", 2024, "Director A", genres=["Drama"])
    mgr.add_review(m_id, u_id, rating=9, review_text="Great!")

    # Verify review and genre associations exist
    rev_count = conn.execute("SELECT COUNT(*) as c FROM reviews WHERE movie_id = ?;", (m_id,)).fetchone()["c"]
    assert rev_count == 1

    # Delete the movie
    conn.execute("DELETE FROM movies WHERE movie_id = ?;", (m_id,))
    conn.commit()

    # Cascade should automatically clean reviews and movie_genres
    rev_after = conn.execute("SELECT COUNT(*) as c FROM reviews WHERE movie_id = ?;", (m_id,)).fetchone()["c"]
    mg_after = conn.execute("SELECT COUNT(*) as c FROM movie_genres WHERE movie_id = ?;", (m_id,)).fetchone()["c"]
    assert rev_after == 0
    assert mg_after == 0
    mgr.close()


def test_rating_check_constraint():
    mgr = MovieDatabaseManager(":memory:")
    mgr.init_schema()
    u_id = mgr.add_user("test_user2", "test2@domain.com")
    m_id = mgr.add_movie("Test Movie 2", 2024, "Director B")

    with pytest.raises(ValueError):
        mgr.add_review(m_id, u_id, rating=11)

    with pytest.raises(ValueError):
        mgr.add_review(m_id, u_id, rating=0)

    mgr.close()


def test_upsert_review():
    mgr = MovieDatabaseManager(":memory:")
    mgr.init_schema()
    u_id = mgr.add_user("reviewer", "rev@domain.com")
    m_id = mgr.add_movie("Film", 2023, "Director")

    mgr.add_review(m_id, u_id, rating=7, review_text="Initial thought")
    # Upsert on same movie and user
    mgr.add_review(m_id, u_id, rating=9, review_text="Revised thought")

    conn = mgr.get_connection()
    row = conn.execute("SELECT rating, review_text FROM reviews WHERE movie_id = ? AND user_id = ?;", (m_id, u_id)).fetchone()
    assert row["rating"] == 9
    assert row["review_text"] == "Revised thought"
    mgr.close()
