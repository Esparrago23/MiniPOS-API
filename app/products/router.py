from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.products.repository import ProductRepository
from app.products.schemas import (
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest,
)
from app.products.service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_current_user)],
)


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))


@router.get("", response_model=list[ProductResponse])
def list_products(
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    return service.list_products()


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    request: ProductCreateRequest,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return service.create(request)


@router.get("/barcode/{barcode}", response_model=ProductResponse)
def get_product_by_barcode(
    barcode: str,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return service.get_by_barcode(barcode)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return service.get_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    request: ProductUpdateRequest,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return service.update(product_id, request)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> dict[str, str]:
    service.delete(product_id)
    return {"message": "Product deleted."}
