"""FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload

from app.config import settings
from app.db import Base, engine, get_db
from app.models import Inquiry, Product
from app.schemas import InquiryCreate, ProductRead
from app.seed import seed_catalog
from app.orders import router as orders_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with next(get_db()) as db:
        seed_catalog(db)
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/assets", StaticFiles(directory=settings.frontend_dir / "assets"), name="assets")
app.include_router(orders_router)


@app.get("/health", tags=["system"])
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "service": settings.app_name, "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/products", response_model=list[ProductRead], tags=["catalog"])
def list_products(db: Session = Depends(get_db)):
    products = db.scalars(select(Product).where(Product.is_active.is_(True)).options(selectinload(Product.variants))).all()
    return products


@app.get("/api/products/{product_id}", response_model=ProductRead, tags=["catalog"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.scalar(select(Product).where(Product.id == product_id, Product.is_active.is_(True)).options(selectinload(Product.variants)))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@app.post("/api/inquiries", status_code=status.HTTP_201_CREATED, tags=["inquiries"])
def create_inquiry(payload: InquiryCreate, db: Session = Depends(get_db)):
    inquiry = Inquiry(**payload.model_dump())
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return {"id": inquiry.id, "message": "Thank you. The Swarup Soap team will contact you."}


@app.get("/", include_in_schema=False)
def homepage():
    return FileResponse(Path(settings.frontend_dir) / "index.html")


@app.get("/manus-routes.json", include_in_schema=False)
def route_manifest():
    return FileResponse(Path(settings.frontend_dir) / "manus-routes.json", media_type="application/json")


@app.get("/styles.css", include_in_schema=False)
def styles():
    return FileResponse(Path(settings.frontend_dir) / "styles.css", media_type="text/css")


@app.get("/script.js", include_in_schema=False)
def script():
    return FileResponse(Path(settings.frontend_dir) / "script.js", media_type="text/javascript")
