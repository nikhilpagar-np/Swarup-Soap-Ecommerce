# Swarup Soap E-Commerce — Implementation Plan

## Scope and working assumptions

This project will turn the supplied static Swarup Soap website into a beginner-friendly, database-driven e-commerce website while preserving its current visual identity, content direction, typography, colors, layout, and supplied product/client images.

The implementation will be incremental rather than a single opaque rewrite. The website will remain usable after each major phase.

The Pack of 10 price for 20 GM is **not finalized**. The current ₹50 value will be represented as pending confirmation and must not become an authoritative business price until the owner confirms it.

## Technical approach

- Frontend: existing semantic HTML, CSS, and vanilla JavaScript.
- Backend: Python FastAPI served by Uvicorn.
- ORM: SQLAlchemy 2.0.
- Local database: SQLite.
- Production database target: PostgreSQL through a `DATABASE_URL` environment variable.
- Migrations: Alembic.
- Validation: Pydantic v2.
- Testing: pytest plus FastAPI test client tests.
- Payments: Razorpay order creation/signature verification when credentials are supplied; Cash on Delivery remains available.
- Notifications: WhatsApp handoff immediately; email notification adapter behind environment configuration.
- Admin authentication: hashed passwords, signed secure session cookie, role-protected admin routes.
- Static serving: FastAPI serves the preserved frontend and assets so Preview can run from one listener on port 3000.
- Secrets: only `.env.example` is committed; real credentials are never written to source files.

## Product and order model

The database will be the source of truth for product names, size, pack quantity, prices, active state, and stock. The frontend may display catalog data but cannot determine the authoritative checkout total.

Core tables:

- `products`: product identity, description, image path, active state, timestamps.
- `product_variants`: size in GM, pack quantity, SKU, price, stock quantity, active state, and pending-price flag.
- `orders`: order number, customer details, address, payment method/status, order status, totals, timestamps.
- `order_items`: ordered variant, name/price snapshot, quantity, and line total.
- `inquiries`: contact/bulk/support enquiry details and status.
- `admin_users`: admin email, password hash, active state, timestamps.
- `payments`: Razorpay identifiers, amount, signature verification, status, timestamps.
- `coupons`: code, discount rule, validity window, usage limits, active state.

The main relationships are:

```text
products 1 ──── many product_variants
orders   1 ──── many order_items
product_variants 1 ──── many order_items
orders   1 ──── many payments
```

Initial confirmed catalog values from the supplied site:

- Single 15 GM: ₹15
- Single 20 GM: ₹20
- Single 50 GM: ₹30
- Single 100 GM: ₹50
- Pack of 10: 15 GM ₹100, 50 GM ₹250, 100 GM ₹400
- Pack of 10: 20 GM currently shown as ₹50, pending owner confirmation

## API and application flow

### Catalog

- `GET /api/products` returns active products and variants.
- `GET /api/products/{id}` returns one product and its active variants.

### Enquiries

- `POST /api/inquiries` validates contact or bulk-order forms and stores the enquiry.
- WhatsApp links remain available as an immediate alternative.

### Checkout and orders

1. The browser stores the cart in `localStorage` for convenience.
2. The browser sends variant IDs and quantities plus customer/address data to the backend.
3. The backend reloads prices and stock from the database.
4. The backend validates quantities, active state, price rules, delivery rules, and stock.
5. The backend calculates subtotal, delivery charge, and total.
6. The backend creates a readable order number and order records.
7. COD orders are confirmed directly.
8. Razorpay orders are created server-side; payment signatures are verified server-side before marking an order paid.
9. The customer receives a confirmation response and can use an order tracking endpoint.

### Admin

Admin routes will be separated from public catalog/order routes. Admin users can manage products, variants, stock, orders, enquiries, coupons, and basic reports. Passwords will be hashed and never stored in plaintext.

## Proposed repository structure

```text
swarupsoap/
├── app/
│   ├── main.py                 # FastAPI app, lifespan, static serving
│   ├── core/
│   │   ├── config.py           # environment-backed settings
│   │   └── security.py         # password/session helpers
│   ├── db/
│   │   ├── base.py             # SQLAlchemy metadata
│   │   ├── session.py          # engine and session factory
│   │   └── seed.py             # repeatable initial catalog seed
│   ├── models/
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── inquiry.py
│   │   ├── admin.py
│   │   ├── coupon.py
│   │   └── payment.py
│   ├── schemas/
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── inquiry.py
│   │   └── admin.py
│   ├── api/
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── inquiries.py
│   │   ├── payments.py
│   │   └── admin.py
│   └── services/
│       ├── pricing.py
│       ├── inventory.py
│       ├── payments.py
│       └── notifications.py
├── alembic/
├── tests/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── assets/
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
├── README.md
├── TODO.md
├── app.config.ts
├── manus-routes.json
├── plan.md
└── Dockerfile
```

The existing single-page site will be moved into `frontend/` with only the minimum markup changes needed to make catalog data and checkout dynamic. No new frontend framework will be introduced.

## Delivery phases

### Phase 2A — Backend foundation and catalog

- Copy the supplied website and assets into the managed project.
- Add Python dependency files and environment configuration.
- Create SQLAlchemy models and initial Alembic migration.
- Add repeatable seed data, keeping the 20 GM pack price pending.
- Add `GET /api/products` and health endpoint.
- Serve the preserved homepage through FastAPI.
- Add product API tests.

### Phase 2B — Frontend connection

- Replace hard-coded product rendering with catalog API data.
- Preserve existing cards, layout, typography, and product photos.
- Add localStorage cart persistence.
- Add quantity controls, accessible labels, and safer DOM rendering.
- Keep WhatsApp enquiry behavior available.

### Phase 2C — Checkout and orders

- Add checkout/customer address form.
- Add server-side total and stock validation.
- Add order numbers and order status.
- Add COD order creation.
- Add order tracking lookup.
- Add confirmation screen and notification adapter.

### Phase 2D — Payments and enquiries

- Add Razorpay server-side order creation and signature verification.
- Add contact and bulk enquiry forms.
- Add email notification integration through environment-configured provider.
- Add delivery charge/free-delivery rules only after business confirmation.

### Phase 2E — Admin and operations

- Add secure admin login/logout.
- Add product and variant management.
- Add stock and order status management.
- Add enquiry and coupon management.
- Add basic reporting views.

### Phase 2F — Quality and portfolio readiness

- Expand pytest coverage.
- Add accessibility, SEO, and security improvements.
- Add README, GitHub upload guide, screenshots guidance, and deployment notes.
- Add `.gitignore`, `.env.example`, license explanation, and seed instructions.
- Prepare honest resume bullets and interview walkthroughs based only on completed features.

## Design direction

### Design movement

**Editorial botanical minimalism**: a warm, tactile, small-batch personal-care identity expressed through quiet layouts, generous spacing, earthy color, and product photography.

### Core principles

1. Preserve familiarity: keep the existing visual language and supplied imagery recognizable.
2. Make commerce calm: shopping controls should feel like part of the brand rather than an intrusive storefront.
3. Keep hierarchy clear: use strong serif headlines, compact labels, and short descriptive copy.
4. Prefer truthful warmth: avoid unsupported product claims and keep business rules explicit.

### Color philosophy

Dark ink and moss establish trust and readability. Cream and paper tones create the feel of a handcrafted package. Clay is the owning accent for calls to action, prices, and small moments of warmth. Sage supports the botanical, everyday-care character without making medical claims.

### Layout paradigm

Use editorial split sections and offset content blocks rather than a dense centered dashboard layout. Product cards remain a simple responsive row for scanability; story and process sections use asymmetric two-column compositions.

### Signature elements

- Clay-colored circular marks and numbered section kickers.
- Serif italic emphasis for emotionally important words.
- Tactile product photography framed by paper, moss, and cream surfaces.

### Interaction philosophy

Interactions should be direct and low-friction: clear add-to-bag actions, visible cart count, immediate price updates, and readable feedback. WhatsApp remains a human handoff, while checkout and payments progressively move into the structured backend flow.

### Animation

Use subtle opacity/translate-in reveals already present in the supplied site, restrained hover lift for product cards, and short cart/toast transitions. Avoid continuous motion that distracts from product information or harms accessibility.

### Typography system

- Headings: Playfair Display, with italic clay emphasis.
- Body and controls: DM Sans.
- Labels: compact uppercase DM Sans with letter spacing.
- Maintain responsive `clamp()` sizing and readable line lengths.

### Brand essence

**Everyday bathing care from Nashik, made with human attention.** Personality: warm, grounded, considered.

### Brand voice

Headlines should be calm, specific, and human. CTAs should be action-oriented without pressure.

- “Good skin days start here.”
- “Choose a single bar, or stock up for the people you serve.”

### Wordmark and logo

Keep the supplied Swarup logo as the primary site mark. Use the existing clay circular mark and serif wordmark treatment in the footer as a supporting text-only fallback.

### Signature brand color

Clay `#c57755` is the owning accent used sparingly for prices, section indices, stamps, and primary action emphasis.

## Business decisions kept open

- Confirm the 20 GM Pack of 10 price before exposing it as a final purchasable price.
- Confirm whether “free local delivery over ₹499” applies only to Nashik/Nadgaon and define the charge below the threshold.
- Confirm initial stock quantities and whether the initial release should allow out-of-stock backorders.
- Confirm which product claims are factually approved.
- Add Razorpay/email credentials only through protected environment configuration when ready.

## Definition of implementation completion

The implementation is complete only when the requested features are either working and tested or explicitly documented as pending because a required business rule or credential has not been supplied. No users, orders, revenue, credentials, or deployment status will be invented.
