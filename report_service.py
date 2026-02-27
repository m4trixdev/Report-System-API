from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_admin
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserCreate, UserResponse, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    payload: UserCreate,
    service: AuthService = Depends(get_service),
    _: dict = Depends(require_admin),
):
    return await service.register(payload)


@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_service),
):
    return await service.login(form_data.username, form_data.password)
