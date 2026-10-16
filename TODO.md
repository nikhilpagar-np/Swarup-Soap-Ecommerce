# Swarup Soap E-Commerce — Delivery Outcomes

## Phase 2A — Backend foundation and catalog

- [ ] The supplied static website and all supplied images remain available in the managed project without unnecessary visual redesign.
- [ ] A FastAPI application serves the homepage, CSS, JavaScript, supplied assets, and the route manifest on port 3000.
- [ ] The backend uses SQLAlchemy 2.0 models and reads its database URL from environment configuration, using SQLite locally and accepting PostgreSQL in production.
- [ ] Product information is stored in database tables, including product variants, soap size, pack quantity, price, active state, and stock quantity.
- [ ] The initial catalog contains 15 GM ₹15, 20 GM ₹20, 50 GM ₹30, and 100 GM ₹50 single bars.
- [ ] The initial catalog contains Pack of 10 options for 15 GM ₹100, 50 GM ₹250, and 100 GM ₹400.
- [ ] The Pack of 10 20 GM value remains pending confirmation and is not treated as a final purchasable price.
- [ ] Catalog and health endpoints are available and tested.
- [ ] Repeatable seed logic does not overwrite later catalog edits.

## Complete project outcomes

- [ ] Frontend catalog loads from the API while preserving visual design and supplied images.
- [ ] Cart persists in localStorage, supports quantity changes, and keeps WhatsApp handoff.
- [ ] Checkout validates address fields and server recalculates totals and stock.
- [ ] Orders receive order numbers, statuses, and tracking behavior.
- [ ] COD works and Razorpay verification is server-side when credentials are configured.
- [ ] Contact and bulk enquiry forms are validated, stored, and notification-ready.
- [ ] Admin authentication/dashboard manages products, inventory, orders, enquiries, coupons, and reports.
- [ ] Tests, security, accessibility, SEO, README, environment examples, migrations, GitHub guidance, resume content, and interview documentation are complete.
