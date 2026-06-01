from sqlalchemy.orm import Session

from app.products.models import ProductModel


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_products(self) -> list[ProductModel]:
        return self._db.query(ProductModel).order_by(ProductModel.name).all()

    def get_by_id(self, product_id: int) -> ProductModel | None:
        return (
            self._db.query(ProductModel)
            .filter(ProductModel.id == product_id)
            .first()
        )

    def get_by_barcode(self, barcode: str) -> ProductModel | None:
        return (
            self._db.query(ProductModel)
            .filter(ProductModel.barcode == barcode)
            .first()
        )

    def get_many_by_ids(self, product_ids: list[int]) -> list[ProductModel]:
        return (
            self._db.query(ProductModel)
            .filter(ProductModel.id.in_(product_ids))
            .all()
        )

    def create(self, product: ProductModel) -> ProductModel:
        self._db.add(product)
        self._db.commit()
        self._db.refresh(product)
        return product

    def update(self, product: ProductModel) -> ProductModel:
        self._db.commit()
        self._db.refresh(product)
        return product

    def delete(self, product: ProductModel) -> None:
        self._db.delete(product)
        self._db.commit()
