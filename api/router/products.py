from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from database.product import Product
from database.dbHandler import DBHandler
from typing import Optional
from sqlalchemy import or_
from router.authorization import is_admin
from fastapi.responses import FileResponse
from starlette import status
from fastapi import HTTPException
from fastapi.responses import FileResponse
from config.app_contex import image_location

import os

router = APIRouter(prefix="/products")

def get_db(request: Request):
    db = DBHandler()
    session = db.session
    try:
        yield session
    finally:
        session.close()

# Define filter expressions
filters = {
    'id': lambda queryset, value: queryset.filter(Product.id == value),
    'category': lambda queryset, value: queryset.filter(Product.category == value),
    'name': lambda queryset, value: queryset.filter(Product.name == value),
    'original_price': lambda queryset, value: queryset.filter(Product.original_price == value),
    'current_price': lambda queryset, value: queryset.filter(Product.current_price == value),
    'gender': lambda queryset, value: queryset.filter(Product.gender == value),
        'sizes': lambda queryset, values: queryset.filter(
        or_(*[Product.sizes.contains(size) for size in values.split(',')])
    ),
}

@router.get('/')
def get_products(
    id: Optional[int] = Query(None, description="Filter by product ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    name: Optional[str] = Query(None, description="Filter by product name"),
    original_price: Optional[float] = Query(None, description="Filter by original price"),
    current_price: Optional[float] = Query(None, description="Filter by current price"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    sizes: Optional[str] = Query(None, description="Filter by sizes (comma-separated)"),
    session: Session = Depends(get_db),
    current_user: dict = Depends(is_admin)
):
    query = session.query(Product)

    # Create a dictionary of filter parameters and values
    filter_params = {
        'id': id,
        'category': category,
        'name': name,
        'original_price': original_price,
        'current_price': current_price,
        'gender': gender,
        'sizes': sizes,
    }

    # Apply filters based on query parameters
    for param_name, param_value in filter_params.items():
        if param_value is not None:
            query = filters[param_name](query, param_value)

    products = query.all()
    return products

@router.get('/{product_id}/image')
def get_product_image(product_id: int, session: Session = Depends(get_db)):
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    extention = product.image_location.split(".")[-1]
    image_path = f"{image_location}/{product_id}.{extention}"
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path, media_type="image/jpeg")  # Adjust media_type accordingly