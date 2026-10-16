"""initial commerce schema"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("products", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("image_path", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("product_variants", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False), sa.Column("size_gm", sa.Integer(), nullable=False), sa.Column("pack_quantity", sa.Integer(), nullable=False), sa.Column("sku", sa.String(80), unique=True, nullable=False), sa.Column("price", sa.Numeric(10, 2)), sa.Column("stock_quantity", sa.Integer(), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("price_pending", sa.Boolean(), nullable=False))
    op.create_table("orders", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("order_number", sa.String(40), unique=True, nullable=False), sa.Column("customer_name", sa.String(120), nullable=False), sa.Column("phone", sa.String(30), nullable=False), sa.Column("email", sa.String(255)), sa.Column("address_line", sa.String(255), nullable=False), sa.Column("city", sa.String(100), nullable=False), sa.Column("state", sa.String(100), nullable=False), sa.Column("pincode", sa.String(12), nullable=False), sa.Column("payment_method", sa.String(20), nullable=False), sa.Column("payment_status", sa.String(20), nullable=False), sa.Column("order_status", sa.String(20), nullable=False), sa.Column("subtotal", sa.Numeric(10, 2), nullable=False), sa.Column("delivery_charge", sa.Numeric(10, 2), nullable=False), sa.Column("total_amount", sa.Numeric(10, 2), nullable=False), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("order_items", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False), sa.Column("product_variant_id", sa.Integer(), sa.ForeignKey("product_variants.id"), nullable=False), sa.Column("product_name_snapshot", sa.String(180), nullable=False), sa.Column("unit_price", sa.Numeric(10, 2), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("line_total", sa.Numeric(10, 2), nullable=False))
    op.create_table("inquiries", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("phone", sa.String(30), nullable=False), sa.Column("email", sa.String(255)), sa.Column("message", sa.Text(), nullable=False), sa.Column("inquiry_type", sa.String(30), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("admin_users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), unique=True, nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False))
    op.create_table("coupons", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("code", sa.String(40), unique=True, nullable=False), sa.Column("discount_percent", sa.Integer(), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False))
    op.create_table("payments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False), sa.Column("provider", sa.String(40), nullable=False), sa.Column("provider_order_id", sa.String(120)), sa.Column("provider_payment_id", sa.String(120)), sa.Column("signature_verified", sa.Boolean(), nullable=False), sa.Column("amount", sa.Numeric(10, 2), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))

def downgrade():
    for table in ["payments", "coupons", "admin_users", "inquiries", "order_items", "orders", "product_variants", "products"]:
        op.drop_table(table)
