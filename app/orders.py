from __future__ import annotations

from decimal import Decimal
from secrets import token_hex

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models import Order, OrderItem, ProductVariant
from app.schemas import OrderCreate

router = APIRouter(prefix="/api/orders", tags=["orders"])


def make_order_number() -> str:
    return f"SS-{token_hex(4).upper()}"


@router.post("", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if any(item.quantity < 1 for item in payload.items):
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    ids = [item.variant_id for item in payload.items]
    variants = db.scalars(select(ProductVariant).where(ProductVariant.id.in_(ids)).options(selectinload(ProductVariant.product))).all()
    by_id = {variant.id: variant for variant in variants}
    subtotal = Decimal("0")
    order_items = []
    for requested in payload.items:
        variant = by_id.get(requested.variant_id)
        if variant is None or not variant.is_active or variant.price is None or variant.price_pending:
            raise HTTPException(status_code=400, detail=f"Variant {requested.variant_id} is unavailable")
        if requested.quantity > variant.stock_quantity:
            raise HTTPException(status_code=409, detail=f"Insufficient stock for {variant.sku}")
        line_total = Decimal(variant.price) * requested.quantity
        subtotal += line_total
        order_items.append(OrderItem(product_variant_id=variant.id, product_name_snapshot=f"{variant.product.name} · {variant.size_gm} GM", unit_price=variant.price, quantity=requested.quantity, line_total=line_total))
    delivery_charge = Decimal("0")
    order = Order(order_number=make_order_number(), customer_name=payload.customer_name, phone=payload.phone, email=payload.email, address_line=payload.address_line, city=payload.city, state=payload.state, pincode=payload.pincode, payment_method=payload.payment_method, payment_status="pending" if payload.payment_method == "razorpay" else "cod_pending", order_status="pending", subtotal=subtotal, delivery_charge=delivery_charge, total_amount=subtotal, items=order_items)
    for requested in payload.items:
        by_id[requested.variant_id].stock_quantity -= requested.quantity
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"order_number": order.order_number, "status": order.order_status, "payment_status": order.payment_status, "subtotal": order.subtotal, "delivery_charge": order.delivery_charge, "total_amount": order.total_amount}


@router.get("/{order_number}")
def track_order(order_number: str, db: Session = Depends(get_db)):
    order = db.scalar(select(Order).where(Order.order_number == order_number))
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_number": order.order_number, "order_status": order.order_status, "payment_status": order.payment_status, "total_amount": order.total_amount, "created_at": order.created_at}
