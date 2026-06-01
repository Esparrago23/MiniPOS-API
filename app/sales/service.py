from fastapi import HTTPException, status

from app.auth.models import UserModel
from app.products.models import ProductModel
from app.products.repository import ProductRepository
from app.sales.models import SaleItemModel, SaleModel
from app.sales.repository import SaleRepository
from app.sales.schemas import SaleCreateRequest


class SaleService:
    def __init__(
        self,
        sale_repository: SaleRepository,
        product_repository: ProductRepository,
    ) -> None:
        self._sale_repository = sale_repository
        self._product_repository = product_repository

    def list_sales(self) -> list[SaleModel]:
        return self._sale_repository.list_sales()

    def get_by_id(self, sale_id: int) -> SaleModel:
        sale = self._sale_repository.get_by_id(sale_id)
        if sale is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale not found.",
            )
        return sale

    def create(self, request: SaleCreateRequest, user: UserModel) -> SaleModel:
        quantities_by_product_id: dict[int, int] = {}
        for item in request.items:
            quantities_by_product_id[item.product_id] = (
                quantities_by_product_id.get(item.product_id, 0) + item.quantity
            )

        products = self._product_repository.get_many_by_ids(
            list(quantities_by_product_id.keys()),
        )
        products_by_id = {product.id: product for product in products}

        missing_ids = [
            product_id
            for product_id in quantities_by_product_id
            if product_id not in products_by_id
        ]
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Products not found: {missing_ids}.",
            )

        for product_id, quantity in quantities_by_product_id.items():
            product = products_by_id[product_id]
            if product.stock < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock for product {product.name}.",
                )

        try:
            sale_items: list[SaleItemModel] = []
            total = 0.0

            for product_id, quantity in quantities_by_product_id.items():
                product = products_by_id[product_id]
                subtotal = round(product.price * quantity, 2)
                product.stock -= quantity
                total += subtotal
                sale_items.append(
                    self._build_sale_item(
                        product=product,
                        quantity=quantity,
                        subtotal=subtotal,
                    ),
                )

            sale = SaleModel(
                user_id=user.id,
                total=round(total, 2),
                items=sale_items,
            )
            return self._sale_repository.save(sale)
        except Exception:
            self._sale_repository.rollback()
            raise

    def _build_sale_item(
        self,
        *,
        product: ProductModel,
        quantity: int,
        subtotal: float,
    ) -> SaleItemModel:
        return SaleItemModel(
            product_id=product.id,
            product_name=product.name,
            barcode=product.barcode,
            quantity=quantity,
            unit_price=product.price,
            subtotal=subtotal,
        )
