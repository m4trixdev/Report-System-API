from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserCreate, UserResponse, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.logging import get_logger

logger = get_logger(__name__)


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, payload: UserCreate) -> UserResponse:
        if await self.repo.username_exists(payload.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )

        hashed = hash_password(payload.password)
        user = await self.repo.create(payload.username, hashed, payload.role)
        logger.info("user_registered", username=user.username)
        return UserResponse.model_validate(user)

    async def login(self, username: str, password: str) -> TokenResponse:
        user = await self.repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")

        token = create_access_token({"sub": user.username, "role": user.role})
        logger.info("user_login", username=user.username)
        return TokenResponse(access_token=token)
