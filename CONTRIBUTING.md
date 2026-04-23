# Contributing and Branch Strategy

## Recommended long-lived branches

- `main`: production-ready, tagged releases only.
- `develop`: integration branch for completed features before release.

## Rule: one branch per pull request

Create **one** feature branch, complete that scope, open a PR, merge, then create the next branch from updated `develop`.

Do **not** create all feature branches in advance.

## Recommended short-lived branch prefixes

- `feature/frontend-*`: templates and styling work.
- `feature/backend-*`: Flask routes, business logic, and persistence.
- `feature/data-*`: schema and database-layer updates.
- `chore/docs-*`: README/docs/process updates.
- `hotfix/*`: urgent fixes that target `main` first, then merge back to `develop`.

## File ownership by branch type

Use this mapping so your current files are organized by responsibility when creating feature branches:

### PR 1 — Front-end (`feature/frontend-*`)

- `templates/base.html`
- `templates/welcome.html`
- `templates/name_entry.html`
- `templates/category.html`
- `templates/build_order.html`
- `templates/review_order.html`
- `templates/customer_info.html`
- `templates/payment.html`
- `templates/confirmation.html`
- `templates/menu_admin.html`
- `static/style.css`

### PR 2 — Back-end (`feature/backend-*`)

- `app.py`
- `bistro_burnett_web/app.py`
- `bistro_burnett_web/storage.py`

### PR 3 — Data (`feature/data-*`)

- `bistro_burnett_web/db.py`
- `data/schema.sql`

### PR 4 — Docs/ops (`chore/docs-*`)

- `README.md`
- `requirements.txt`
- `CONTRIBUTING.md`

## One-at-a-time branch workflow

Run from the repository root.

### 0) Prepare integration branch once

```bash
git checkout main
git pull origin main
git checkout -b develop
git push -u origin develop
```

### 1) Start only the next branch (example: PR 1 front-end)

```bash
git checkout develop
git pull origin develop
git checkout -b feature/frontend-ui-cleanup
```

Open PR to `develop` after commits:

```bash
git push -u origin feature/frontend-ui-cleanup
```

### 2) After merge, create the next branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/backend-order-validation
```

Repeat this same pattern for PR 3 and PR 4.
