# Branch Progress Tracker

This file tracks the one-branch-at-a-time workflow for splitting work into multiple pull requests.

## Planned PR order

1. ✅ `feature/frontend-ui-cleanup`
2. 🚧 `feature/backend-order-validation` (next branch created)
3. ⏳ `feature/data-menu-schema-updates`
4. ⏳ `chore/docs-repo-standards`

## Backend PR scope (PR 2)

Target branch: `develop`

Files to change in this PR:
- `app.py`
- `bistro_burnett_web/app.py`
- `bistro_burnett_web/storage.py`

After PR 2 is merged, create PR 3 from updated `develop`.
