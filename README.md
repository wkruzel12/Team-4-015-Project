# Bistro Burnett Web Prototype

This is the browser-based Bistro Burnett ordering prototype for Bistro Burnett. It is designed to run locally or in GitHub Codespaces through the browser.

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

## Branching workflow

Use the branch strategy in `CONTRIBUTING.md` to split work into multiple PRs, creating one feature branch at a time from `develop` (frontend first, then backend, then data, then docs).
