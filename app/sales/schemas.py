from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class SaleItemCreateRequest(BaseModel):
    product_id: int
    quantity: int

    @field_validator("product_id")
    @classmethod
    def validate_product_id(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Product id must be greater than 0.")
        return value

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Quantity must be greater than 0.")
        return value


class SaleCreateRequest(BaseModel):
    items: list[SaleItemCreateRequest]

    @field_validator("items")
    @classmethod
    def validate_items(cls, value: list[SaleItemCreateRequest]) -> list[SaleItemCreateRequest]:
        if not value:
            raise ValueError("Sale must have at least one item.")
        return value


class SaleItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    barcode: str
    quantity: int
    unit_price: float
    subtotal: float


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    total: float
    created_at: datetime
    items: list[SaleItemResponse]
