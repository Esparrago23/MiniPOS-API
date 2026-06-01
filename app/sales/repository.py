from sqlalchemy.orm import Session, selectinload

from app.sales.models import SaleModel


class SaleRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_sales(self) -> list[SaleModel]:
        return (
            self._db.query(SaleModel)
            .options(selectinload(SaleModel.items))
            .order_by(SaleModel.created_at.desc())
            .all()
        )

    def get_by_id(self, sale_id: int) -> SaleModel | None:
        return (
            self._db.query(SaleModel)
            .options(selectinload(SaleModel.items))
            .filter(SaleModel.id == sale_id)
            .first()
        )

    def save(self, sale: SaleModel) -> SaleModel:
        self._db.add(sale)
        self._db.commit()
        self._db.refresh(sale)
        return sale

    def rollback(self) -> None:
        self._db.rollback()
