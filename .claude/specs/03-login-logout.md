# Spec: Login and Logout

## Overview
Implement authentication state for Spendly by upgrading the existing `/login` stub into a working sign-in flow and implementing `/logout`. Visitors submit their email and password; the route verifies them against the `users` table, stores the authenticated user's id in the Flask session on success, and redirects to the landing page. Logging out clears the session and returns the visitor to the landing page. This step builds on registration and unlocks the authenticated features (profile, expenses) that follow.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`/register` creates the account being authenticated)

## Routes
- `GET /login` — render the sign-in form — public (existing stub, upgrade to accept GET/POST)
- `POST /login` — validate credentials, start a session, redirect to landing — public
- `GET /logout` — clear the session and redirect to landing — logged-in

## Database changes
No database changes. The existing `users` table (id, name, email, password_hash, created_at) provides everything required. Authentication is performed with a parameterised `SELECT ... FROM users WHERE email = ?` and password verification with `werkzeug.security.check_password_hash`.

## Templates
- **Modify**: `templates/login.html`
  - Change the form `action` to `url_for('login')` with `method="post"`
  - Keep the existing error display block
  - Keep all existing visual design
- **Modify**: `templates/base.html`
  - Make the navbar auth-aware: show "Sign out" (linking to `/logout`) when a user is in the session, otherwise show "Sign in" and "Get started"

## Files to change
- `app.py` — set `app.secret_key`, upgrade `login()` to handle GET/POST, implement `logout()`
- `templates/login.html` — wire the form action/method with `url_for`
- `templates/base.html` — conditional auth links in the navbar

## Files to create
None.

## New dependencies
No new dependencies. Uses Flask's built-in `session`, and `werkzeug.security.check_password_hash` (already installed).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Verify passwords with `werkzeug.security.check_password_hash` — never compare plaintext
- Set `app.secret_key` (a hardcoded dev string is acceptable for now) so sessions work
- On login, store only the user id (and optionally name) in `session` — never the password or hash
- Use a generic error message such as "Invalid email or password." to avoid account enumeration
- Normalize the submitted email with `.strip().lower()` before lookup, matching the registration flow
- Logout must call `session.clear()` (or `session.pop` for the user keys) before redirecting
- Authenticated users visiting `/login` or `/register` are redirected to the landing page
- Redirect on success: `url_for('landing')`; on logout: `url_for('landing')`
- Use `url_for()` for every internal link — never hardcode URLs
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values

## Definition of done
- [ ] `GET /login` renders the sign-in form without errors
- [ ] Submitting valid credentials for the seeded demo user (`demo@spendly.com` / `demo123`) starts a session and redirects to `/`
- [ ] Submitting an unknown email re-renders the form with "Invalid email or password."
- [ ] Submitting a correct email with the wrong password re-renders the form with "Invalid email or password."
- [ ] Submitting empty fields re-renders the form with a validation error
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] After logout, visiting a page shows the signed-out navbar state
- [ ] An authenticated user visiting `/login` or `/register` is redirected to `/`
- [ ] No password or hash is stored in the session or templates