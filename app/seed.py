"""Repeatable catalog seeding for local development."""
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product, ProductVariant


PRODUCTS = [
    ("Swarup Soap", "Everyday bathing bars made in Nadgaon, Nashik.", "assets/soap-15gm.jpg"),
]

VARIANTS = [
    (15, 1, "SWARUP-15-SINGLE", Decimal("15"), 100, False),
    (20, 1, "SWARUP-20-SINGLE", Decimal("20"), 100, False),
    (50, 1, "SWARUP-50-SINGLE", Decimal("30"), 100, False),
    (100, 1, "SWARUP-100-SINGLE", Decimal("50"), 100, False),
    (15, 10, "SWARUP-15-PACK10", Decimal("100"), 50, False),
    (20, 10, "SWARUP-20-PACK10", None, 0, True),
    (50, 10, "SWARUP-50-PACK10", Decimal("250"), 50, False),
    (100, 10, "SWARUP-100-PACK10", Decimal("400"), 50, False),
]


def seed_catalog(db: Session) -> None:
    product = db.scalar(select(Product).limit(1))
    if product is None:
        product = Product(name=PRODUCTS[0][0], description=PRODUCTS[0][1], image_path=PRODUCTS[0][2])
        db.add(product)
        db.flush()
        for size_gm, pack_quantity, sku, price, stock, pending in VARIANTS:
            db.add(ProductVariant(product_id=product.id, size_gm=size_gm, pack_quantity=pack_quantity, sku=sku, price=price, stock_quantity=stock, price_pending=pending, is_active=not pending))
        db.commit()
