from fastapi import HTTPException, status

from app.products.models import ProductModel
from app.products.repository import ProductRepository
from app.products.schemas import ProductCreateRequest, ProductUpdateRequest


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def list_products(self) -> list[ProductModel]:
        return self._repository.list_products()

    def get_by_id(self, product_id: int) -> ProductModel:
        product = self._repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )
        return product

    def get_by_barcode(self, barcode: str) -> ProductModel:
        product = self._repository.get_by_barcode(barcode.strip())
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )
        return product

    def create(self, request: ProductCreateRequest) -> ProductModel:
        existing_product = self._repository.get_by_barcode(request.barcode)
        if existing_product is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barcode already registered.",
            )

        return self._repository.create(
            ProductModel(
                name=request.name,
                barcode=request.barcode,
                price=request.price,
                stock=request.stock,
                category=request.category,
            ),
        )

    def update(
        self,
        product_id: int,
        request: ProductUpdateRequest,
    ) -> ProductModel:
        product = self.get_by_id(product_id)

        if request.barcode is not None and request.barcode != product.barcode:
            existing_product = self._repository.get_by_barcode(request.barcode)
            if existing_product is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Barcode already registered.",
                )

        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        return self._repository.update(product)

    def delete(self, product_id: int) -> None:
        product = self.get_by_id(product_id)
        self._repository.delete(product)
