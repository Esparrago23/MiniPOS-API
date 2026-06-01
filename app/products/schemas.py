from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ProductCreateRequest(BaseModel):
    name: str
    barcode: str
    price: float
    stock: int = 0
    category: str | None = None

    @field_validator("name", "barcode")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field is required.")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price must be greater than 0.")
        return value

    @field_validator("stock")
    @classmethod
    def validate_stock(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        return value

    @field_validator("category")
    @classmethod
    def clean_category(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class ProductUpdateRequest(BaseModel):
    name: str | None = None
    barcode: str | None = None
    price: float | None = None
    stock: int | None = None
    category: str | None = None

    @field_validator("name", "barcode")
    @classmethod
    def validate_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty.")
        return value

    @field_validator("price")
    @classmethod
    def validate_optional_price(cls, value: float | None) -> float | None:
        if value is not None and value <= 0:
            raise ValueError("Price must be greater than 0.")
        return value

    @field_validator("stock")
    @classmethod
    def validate_optional_stock(cls, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise ValueError("Stock cannot be negative.")
        return value

    @field_validator("category")
    @classmethod
    def clean_optional_category(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    barcode: str
    price: float
    stock: int
    category: str | None
    created_at: datetime
    updated_at: datetime
