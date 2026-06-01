from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserModel
from app.core.database import get_db
from app.products.repository import ProductRepository
from app.sales.repository import SaleRepository
from app.sales.schemas import SaleCreateRequest, SaleResponse
from app.sales.service import SaleService

router = APIRouter(prefix="/sales", tags=["sales"])


def get_sale_service(db: Session = Depends(get_db)) -> SaleService:
    return SaleService(
        sale_repository=SaleRepository(db),
        product_repository=ProductRepository(db),
    )


@router.get("", response_model=list[SaleResponse])
def list_sales(
    current_user: UserModel = Depends(get_current_user),
    service: SaleService = Depends(get_sale_service),
) -> list[SaleResponse]:
    return service.list_sales()


@router.post("", response_model=SaleResponse, status_code=201)
def create_sale(
    request: SaleCreateRequest,
    current_user: UserModel = Depends(get_current_user),
    service: SaleService = Depends(get_sale_service),
) -> SaleResponse:
    return service.create(request, current_user)


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: SaleService = Depends(get_sale_service),
) -> SaleResponse:
    return service.get_by_id(sale_id)
