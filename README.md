# Movie & TV Series Review Portal

Full-stack database-backed entertainment review application built with PHP, MySQL, and Apache for a Database Management Systems course.

## Features

- **Relational Backend:** Normalized MySQL tables for users, movies, TV series, reviews, categories, and watchlists.
- **User Authentication:** Session-based login and registration (`$_SESSION`).
- **Interactive Reviews:** Star ratings, review submissions, and aggregate community score recalculations via SQL triggers.
- `academic_dbms_report/19bce7346_dbms_project_report (2)(1).pdf` — Official project report with ER diagrams, 3NF normalization proofs, and SQL query verification.

## Setup

```bash
# 1. Clone into Apache web root (e.g., C:/xampp/htdocs/)
# 2. Import database schema:
mysql -u root -p < database/movie_reviews.sql
# 3. Configure dbConn.php with database credentials
# 4. Open http://localhost/movie-series-review-dbms/movie-review-app/
```
