# Swarup Soap E-Commerce

A beginner-friendly e-commerce project for Swarup Soap, a Nashik-based soap brand. The project preserves the supplied editorial storefront design and adds a Python FastAPI backend, SQLAlchemy data model, catalog API, order validation, migrations, tests, and a GitHub-ready workflow.

## Current status

Phase 2A is implemented: the supplied website is in `frontend/`, the FastAPI server serves the website and assets, catalog data is seeded into SQLite, the catalog API is available, order creation validates server-side prices and stock, and tests cover health/catalog/not-found behavior. Razorpay, email, admin dashboard, and advanced checkout UI remain later phases. The Pack of 10 20 GM price remains pending confirmation and is not purchasable.

## Stack

- HTML, CSS, vanilla JavaScript
- Python FastAPI and Uvicorn
- SQLAlchemy 2.0 and Alembic
- SQLite locally; PostgreSQL-compatible URL for production
- Pydantic validation and pytest

## Project map

`frontend/` contains the existing visual site and supplied images. `app/main.py` provides FastAPI routes and static serving. `app/models.py` defines database tables. `app/seed.py` inserts the initial catalog once. `app/orders.py` recalculates order totals and checks stock. `alembic/` contains migration configuration and the initial schema migration. `tests/` contains automated API tests.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
```

Open `http://localhost:3000`. API documentation is available at `/docs`, health is `/health`, and the catalog is `/api/products`.

For a clean local database, remove `data/swarupsoap.db` and run the migration plus server again. Never remove a production database without a backup and approval.

## API examples

```bash
curl http://localhost:3000/health
curl http://localhost:3000/api/products
curl http://localhost:3000/api/products/1
```

Create a COD order after checking the variant ID returned by the catalog endpoint:

```bash
curl -X POST http://localhost:3000/api/orders \
  -H 'Content-Type: application/json' \
  -d '{"customer_name":"Example Customer","phone":"8888799462","address_line":"Main Road","city":"Nashik","state":"Maharashtra","pincode":"422001","payment_method":"cod","items":[{"variant_id":1,"quantity":1}]}'
```

## Tests

```bash
pytest -q
```

Tests use a separate SQLite file. Development and production database writes are real data, so avoid destructive test fixtures against a shared database.

## GitHub upload

Create a GitHub repository named `swarup-soap-ecommerce`, then run:

```bash
git init
git add .
git commit -m "chore: add Swarup Soap e-commerce foundation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/swarup-soap-ecommerce.git
git push -u origin main
```

Before pushing, confirm `.env`, real credentials, customer data, database files, virtual environments, and caches are excluded. Use `.env.example` as the safe template. Do not claim the repository is uploaded until GitHub confirms the push.

## Important business decisions

Before making Pack of 10 20 GM purchasable, confirm its correct price. Also confirm delivery charges/free-delivery geography, initial stock values, product claims, Razorpay credentials, and notification provider details. These are intentionally not invented in this repository.

## License

Choose a license with the business owner before adding one. For a portfolio-only private brand project, keep the repository private or add a clear proprietary notice. If the code will be openly reused, MIT is a simple permissive choice, but the brand assets and product photos should not automatically be treated as MIT-licensed.
