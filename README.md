# Bistro Burnett Web Prototype

This is the browser-based Bistro Burnett ordering prototype for Bistro Burnett, which is designed to run either locally or in GitHub Codespaces through the browser!

## Tech stack

- Python
- Flask
- HTML/CSS
- SQLite for the menu only

## Features

- welcome, name entry, category, build, review, customer info, payment, and confirmation screens
- a five-table SQLite menu database
- menu database search/filter, insert, and update tools
- returning-customer persistence and order-history persistence
- visual styling matched to the Bistro Burnett interface

## Project structure

- `app.py`: run entry point
- `bistro_burnett_web/app.py`: Flask routes and ordering logic
- `bistro_burnett_web/db.py`: SQLite helpers and seed data
- `bistro_burnett_web/storage.py`: JSON persistence for customers and orders
- `templates/`: HTML templates
- `static/`: CSS and image assets
- `data/schema.sql`: visible five-table SQLite schema

## Branch organization

Use the following long-lived branches so work stays in the right place:

- `main`: integration/stable branch for reviewed code.
- `feature/ui-polish`: UI and styling updates only.
- `feature/menu-database-admin`: menu admin and database workflow changes.
- `10-digit-validation-change`: phone-number validation changes.

Recommended workflow:

1. Branch from `main` for each focused task.
2. Keep each branch scoped to one area listed above.
3. Run tests/checks before merging into `main`.
4. Delete short-lived task branches after merge.

### File ownership by branch

Exact file lists (no duplicates):

- `main`
  - `README.md`
  - `requirements.txt`
  - `app.py`
  - `bistro_burnett_web/__init__.py`
  - `bistro_burnett_web/app.py` (shared integration file; feature branches should only touch scoped areas)

- `feature/menu-database-admin`
  - `bistro_burnett_web/db.py`
  - `bistro_burnett_web/storage.py`
  - `data/schema.sql`
  - `templates/menu_admin.html`

- `10-digit-validation-change`
  - validation sections in `bistro_burnett_web/app.py`
  - `templates/welcome.html`

- `feature/ui-polish`
  - `templates/base.html`
  - `templates/build_order.html`
  - `templates/category.html`
  - `templates/confirmation.html`
  - `templates/customer_info.html`
  - `templates/name_entry.html`
  - `templates/payment.html`
  - `templates/review_order.html`
  - `static/style.css`
  - `static/assets/addons.png`
  - `static/assets/bread.png`
  - `static/assets/campus_background.png`
  - `static/assets/cheese.png`
  - `static/assets/dressings.png`
  - `static/assets/logo.png`
  - `static/assets/mascot.png`
  - `static/assets/protein.png`
  - `static/assets/sandwich.png`
  - `static/assets/toppings.png`
  - `static/assets/wordmark.png`
  - `static/assets/wrap.png`

Duplicate-root copies were removed from the repository so only the canonical files above remain.

## Run locally

```powershell
cd bistro_burnett_web
py -m pip install -r requirements.txt
py app.py
```

Then open:

`http://127.0.0.1:8000`

## Run in Codespaces

1. Open the repository in GitHub Codespaces.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python app.py
```

4. Open the forwarded port for `8000`.

## Database design

- SQLite is used for the menu only.
- The visible schema is in `data/schema.sql`.
- The five menu tables are:
  - `bases`
  - `proteins`
  - `cheeses`
  - `toppings`
  - `extras`
- The `Menu Database` button in the app opens an admin page that reads and updates the SQLite-backed menu data through Flask/Python.

## Notes

- SQLite is used for the menu only, matching the project requirement.
- Customer and submitted-order persistence are stored in local JSON files for simplicity.
- The repository should not include `data/menu.db`, `data/customers.json`, or `data/orders.json`; those are created locally when the app runs.
