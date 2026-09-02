# Movie & TV Series Review Portal — Full-Stack DBMS Web Application

[![PHP](https://img.shields.io/badge/PHP-7.4%2F8.x-purple.svg)](https://www.php.net/)
[![MySQL](https://img.shields.io/badge/MySQL-Relational%20DB-blue.svg)](https://www.mysql.com/)
[![Apache](https://img.shields.io/badge/Server-Apache%20%2F%20XAMPP-orange.svg)](https://www.apachefriends.org/)
[![University](https://img.shields.io/badge/Institution-Vellore%20Institute%20of%20Technology%20(VIT)-blue.svg)](https://vit.ac.in/)
[![Course](https://img.shields.io/badge/Course-Database%20Management%20Systems-red.svg)](https://vit.ac.in/)

---

## 📌 Executive Summary & Academic Context

This repository contains the complete full-stack database-backed web application developed for the **Database Management Systems (DBMS)** curriculum at **Vellore Institute of Technology (VIT)**.

The platform provides an interactive entertainment portal where users can explore movies and television series, create authenticated user accounts, submit structured reviews and 1-to-10 numerical ratings, bookmark watchlist titles, and view aggregated community analytics powered by a relational MySQL backend.

---

## 🚀 Key System Features & Architecture

### 1. Relational Database Backend (`database/movie_reviews.sql`)
- Normalized tables (`users`, `movies`, `series`, `reviews`, `ratings`, `categories`, `watchlist`).
- Referential integrity with cascading foreign keys ensuring clean record deletions.
- SQL triggers automatically recalculating aggregate movie score averages upon new review insertion.

### 2. User Authentication & Session Security
- User registration and login validation with hashed password verification.
- Secure PHP session tracking (`$_SESSION`) guarding protected user actions (submitting reviews, managing watchlist).

### 3. Responsive Web Frontend
- Modular PHP architecture (`header.php`, `footer.php`, `dbConn.php`).
- Interactive review forms with AJAX validation, responsive CSS styling, and movie poster asset management.

---

## 📂 Repository Structure

```
movie-series-review-dbms/
├── movie-review-app/                # PHP application endpoints and scripts
│   ├── index.php                    # Homepage displaying trending movies and top ratings
│   ├── movie.php                    # Individual movie details, cast, and review stream
│   ├── series.php                   # TV Series catalog and episode guide
│   ├── addreview.php                # Review and star-rating submission handler
│   ├── login.php / register.php     # Session authentication and user creation
│   ├── dbConn.php                   # MySQL PDO/mysqli database connection wrapper
│   └── About.php / contact.php      # Informational and support pages
├── database/                        # Database schema dumps
│   ├── movie_reviews.sql            # Table definitions and seed data
│   └── ms.sql                       # Supplemental database scripts
└── README.md                        # Documentation
```

---

## 🛠️ Setup & Local Deployment

```bash
# 1. Clone repository into your local Apache webroot (e.g., C:/xampp/htdocs/)
git clone https://github.com/taran-dev4u/movie-series-review-dbms.git

# 2. Import database schema into MySQL
mysql -u root -p < movie-series-review-dbms/database/movie_reviews.sql

# 3. Configure dbConn.php with your local MySQL credentials
# 4. Open browser at http://localhost/movie-series-review-dbms/movie-review-app/
```

---

## 👨‍💻 Author & Academic Attribution
- **Author:** Taran Mamidala (Reg: 19BCE7346)
- **Institution:** Vellore Institute of Technology (VIT)
- **Course:** CSE 2004 — Database Management Systems
