from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from database.db import get_db, init_db, seed_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")
        if len(password) < 8:
            return render_template(
                "register.html", error="Password must be at least 8 characters."
            )
        if "@" not in email or "." not in email.split("@")[-1]:
            return render_template(
                "register.html", error="Enter a valid email address."
            )

        conn = get_db()
        try:
            existing = conn.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()
            if existing:
                return render_template(
                    "register.html", error="Email already registered."
                )

            conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, generate_password_hash(password)),
            )
            conn.commit()
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            return render_template("login.html", error="All fields are required.")

        conn = get_db()
        try:
            user = conn.execute(
                "SELECT id, name, email, password_hash FROM users WHERE email = ?",
                (email,),
            ).fetchone()
        finally:
            conn.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.")

        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        return redirect(url_for("landing"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db()
    try:
        row = conn.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?",
            (session.get("user_id"),),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        session.clear()
        return redirect(url_for("login"))

    name = row["name"]
    initials = "".join(part[0] for part in name.split() if part)[:2].upper() or "U"

    created_at = row["created_at"]
    try:
        member_since = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%B %Y")
    except (TypeError, ValueError):
        member_since = created_at or ""

    profile_user = {
        "name": name,
        "email": row["email"],
        "initials": initials,
        "member_since": member_since,
    }

    stats = {
        "total_spent": 2875.00,
        "transaction_count": 8,
        "top_category": "Bills",
    }

    transactions = [
        {"date": "2025-01-01", "description": "Lunch at cafe", "category": "Food", "amount": 45.00},
        {"date": "2025-01-03", "description": "Cab to office", "category": "Transport", "amount": 120.00},
        {"date": "2025-01-05", "description": "Electricity bill", "category": "Bills", "amount": 890.00},
        {"date": "2025-01-07", "description": "Pharmacy", "category": "Health", "amount": 320.00},
        {"date": "2025-01-10", "description": "Movie tickets", "category": "Entertainment", "amount": 250.00},
        {"date": "2025-01-12", "description": "Clothes", "category": "Shopping", "amount": 650.00},
        {"date": "2025-01-15", "description": "Misc expense", "category": "Other", "amount": 100.00},
        {"date": "2025-01-18", "description": "Groceries", "category": "Food", "amount": 500.00},
    ]

    categories = [
        {"name": "Bills", "amount": 890.00, "percent": 31},
        {"name": "Shopping", "amount": 650.00, "percent": 23},
        {"name": "Food", "amount": 545.00, "percent": 19},
        {"name": "Health", "amount": 320.00, "percent": 11},
        {"name": "Entertainment", "amount": 250.00, "percent": 9},
        {"name": "Transport", "amount": 120.00, "percent": 4},
        {"name": "Other", "amount": 100.00, "percent": 3},
    ]

    return render_template(
        "profile.html",
        user=profile_user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )

@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
