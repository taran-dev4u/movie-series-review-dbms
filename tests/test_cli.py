import json

from movie_db.cli import main


def test_cli_init_and_stats(tmp_path, capsys):
    db_file = tmp_path / "test_movies.db"

    # Init with seed
    ret = main(["--db", str(db_file), "init", "--seed"])
    assert ret == 0
    capsys.readouterr()

    # Stats JSON
    ret = main(["--db", str(db_file), "stats", "--json"])
    assert ret == 0
    captured = capsys.readouterr()
    stats = json.loads(captured.out)
    assert stats["total_movies"] == 6

    # Top rated JSON
    ret = main(["--db", str(db_file), "top", "--limit", "2", "--json"])
    assert ret == 0
    captured = capsys.readouterr()
    top = json.loads(captured.out)
    assert len(top) == 2

    # Genre analytics JSON
    ret = main(["--db", str(db_file), "genres", "--json"])
    assert ret == 0
    captured = capsys.readouterr()
    genres = json.loads(captured.out)
    assert len(genres) > 0
