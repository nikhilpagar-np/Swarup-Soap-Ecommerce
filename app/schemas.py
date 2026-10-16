"""Pydantic request and response schemas."""
from __future__ import annotations

from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class VariantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    size_gm: int
    pack_quantity: int
    sku: str
    price: Decimal | None
    stock_quantity: int
    is_active: bool
    price_pending: bool


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    image_path: str
    is_active: bool
    variants: list[VariantRead] = Field(default_factory=list)


class CartItemInput(BaseModel):
    variant_id: int
    quantity: int = Field(ge=1, le=100)


class CustomerAddressInput(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=10, max_length=30)
    email: str | None = None
    address_line: str = Field(min_length=5, max_length=255)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    pincode: str = Field(min_length=4, max_length=12)


class OrderCreate(CustomerAddressInput):
    items: list[CartItemInput] = Field(min_length=1)
    payment_method: str = Field(default="cod", pattern="^(cod|razorpay)$")


class InquiryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=10, max_length=30)
    email: str | None = None
    message: str = Field(min_length=5, max_length=2000)
    inquiry_type: str = Field(default="contact", pattern="^(contact|bulk|support)$")
