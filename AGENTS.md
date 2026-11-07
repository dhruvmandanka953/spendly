# AGENTS.md

This file provides guidance to Codex (claude.ai/code) when working with code in this repository.

## Commands

- Activate the virtualenv: `source venv/Scripts/activate` (Windows/Git Bash) or `source venv/bin/activate`.
- Install dependencies: `pip install -r requirements.txt`.
- Run the app: `python app.py` (starts Flask on port 5001 in debug mode).
- Run all tests: `pytest`.
- Run a single test: `pytest path/to/test_file.py::test_name`.

## Architecture

Flask web app (server-rendered Jinja templates) for an expense tracker. Entry point is `app.py`, which defines all routes. Templates live in `templates/`; static assets in `static/` (`static/css`, `static/js`).

Database layer is the `database/` package (`database/db.py`), currently a student-facing placeholder expected to expose `get_db()`, `init_db()`, and `seed_db()`. The SQLite file `expense_tracker.db` is gitignored and created at runtime.

Several routes in `app.py` (logout, profile, add/edit/delete expense) are placeholders returning "coming in Step N" strings — students implement them in later steps; treat them as unfinished. The app currently only serves landing, register, login, terms, and privacy pages.