"""Command-line interface for movie database provisioning, querying, and analytics."""

from __future__ import annotations

import argparse
import json
import sys

from movie_db.analytics import MovieAnalyticsEngine
from movie_db.manager import MovieDatabaseManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="movie-db",
        description="Movie and TV Series relational database management and analytics CLI.",
    )
    parser.add_argument("--db", default="movies.db", help="Path to SQLite database file")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Init subcommand
    init_parser = subparsers.add_parser("init", help="Initialize schema and optionally seed benchmark catalog")
    init_parser.add_argument("--seed", action="store_true", help="Populate database with curated movies and reviews")

    # Top-rated subcommand
    top_parser = subparsers.add_parser("top", help="Rank top movies by Bayesian weighted average rating")
    top_parser.add_argument("--genre", help="Filter by genre name (e.g., Sci-Fi, Drama)")
    top_parser.add_argument("--limit", type=int, default=5, help="Number of records to display")
    top_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    # Genres subcommand
    genres_parser = subparsers.add_parser("genres", help="View aggregate metrics per genre")
    genres_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    # Recommend subcommand
    rec_parser = subparsers.add_parser("recommend", help="Generate collaborative filtering recommendations")
    rec_parser.add_argument("--user-id", type=int, required=True, help="Target user ID")
    rec_parser.add_argument("--limit", type=int, default=3, help="Max recommendations to return")
    rec_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    # Stats subcommand
    stats_parser = subparsers.add_parser("stats", help="View database summary statistics")
    stats_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    mgr = MovieDatabaseManager(args.db)
    engine = MovieAnalyticsEngine(mgr)

    try:
        if args.command == "init":
            if args.seed:
                mgr.seed_default_catalog()
                print(f"Database {args.db} initialized and seeded with curated benchmark catalog.")
            else:
                mgr.init_schema()
                print(f"Database {args.db} schema initialized successfully.")

        elif args.command == "top":
            results = engine.get_top_rated_movies(limit=args.limit, genre=args.genre)
            if args.json:
                print(json.dumps(results, indent=2))
            else:
                print(f"=== Top Rated Movies {f'[{args.genre}]' if args.genre else ''} ===")
                for rank, m in enumerate(results, 1):
                    print(f"  {rank:2d}. {m['title']} ({m['release_year']}) - Score: {m['bayesian_score']} ({m['review_count']} reviews)")

        elif args.command == "genres":
            results = engine.get_genre_analytics()
            if args.json:
                print(json.dumps(results, indent=2))
            else:
                print("=== Genre Performance Analytics ===")
                for g in results:
                    print(f"  {g['genre']:15s} | Movies: {g['movie_count']:2d} | Reviews: {g['review_count']:2d} | Avg: {g['avg_rating']:.2f}")

        elif args.command == "recommend":
            recs = engine.get_user_recommendations(args.user_id, limit=args.limit)
            if args.json:
                print(json.dumps(recs, indent=2))
            else:
                print(f"=== Recommendations for User #{args.user_id} ===")
                for r in recs:
                    print(f"  - {r['title']} ({r['release_year']}) | Predicted: {r['predicted_rating']}")

        elif args.command == "stats":
            stats = engine.get_overall_stats()
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                print("=== Movie DBMS Summary Statistics ===")
                for k, v in stats.items():
                    print(f"  {k:18s}: {v}")

    finally:
        mgr.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
