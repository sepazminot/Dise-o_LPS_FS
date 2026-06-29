"""
Application service for Authentication.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import (
    User,
    TokenPair,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.infrastructure.database.repositories import UserRepository
from app.infrastructure.auth.jwt import JWTAdapter


class AuthService:
    """Application service for authentication operations."""

    def __init__(
        self,
        session: AsyncSession,
        jwt_adapter: JWTAdapter | None = None,
    ):
        """Initialize auth service."""
        self.session = session
        self.user_repo = UserRepository(session)
        self.jwt_adapter = jwt_adapter or JWTAdapter()

    async def register(
        self,
        email: str,
        password: str,
        full_name: str,
        role: str = "student",
    ) -> tuple[User, TokenPair]:
        """Register a new user and return tokens."""
        try:
            user = await self.user_repo.create(
                email=email,
                password=password,
                full_name=full_name,
                role=role,
            )
            access_token, refresh_token, expires_in = self.jwt_adapter.create_token_pair(
                user_id=user.id,
                email=user.email,
                role=user.role.value,
            )
            token_pair = TokenPair(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
            )
            return user, token_pair
        except UserAlreadyExistsError as e:
            raise UserAlreadyExistsError(str(e)) from e

    async def login(
        self,
        email: str,
        password: str,
    ) -> tuple[User, TokenPair]:
        """Login user and return tokens."""
        user = await self.user_repo.verify_credentials(email, password)
        if user is None:
            raise InvalidCredentialsError("Invalid email or password")

        access_token, refresh_token, expires_in = self.jwt_adapter.create_token_pair(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
        )
        token_pair = TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )
        return user, token_pair

    async def refresh_token(
        self,
        refresh_token: str,
    ) -> TokenPair:
        """Refresh access token using refresh token."""
        payload = self.jwt_adapter.validate_refresh_token(refresh_token)
        user = await self.user_repo.get_by_id(payload.sub)
        if user is None:
            raise InvalidCredentialsError("User not found")

        access_token, new_refresh_token, expires_in = self.jwt_adapter.create_token_pair(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
        )
        return TokenPair(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=expires_in,
        )

    async def validate_token(
        self,
        access_token: str,
    ) -> tuple[bool, User | None, list[str]]:
        """Validate access token and return user info."""
        try:
            payload = self.jwt_adapter.validate_access_token(access_token)
            user = await self.user_repo.get_by_id(payload.sub)
            if user is None:
                return False, None, []

            # Map role to permissions
            permissions = self._get_permissions(user.role)
            return True, user, permissions
        except Exception:
            return False, None, []

    async def get_profile(
        self,
        user_id: str,
    ) -> User:
        """Get user profile."""
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user

    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ) -> bool:
        """Change user password."""
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {user_id} not found")

        # Verify current password
        verified = await self.user_repo.verify_credentials(
            user.email,
            current_password,
        )
        if verified is None:
            raise InvalidCredentialsError("Current password is incorrect")

        await self.user_repo.update_password(user_id, new_password)
        return True

    def _get_permissions(self, role: str) -> list[str]:
        """Get permissions based on role."""
        permissions_map = {
            "admin": [
                "users:create",
                "users:read",
                "users:update",
                "users:delete",
                "courses:create",
                "courses:read",
                "courses:update",
                "courses:delete",
                "grades:create",
                "grades:read",
                "grades:update",
                "grades:delete",
            ],
            "teacher": [
                "courses:create",
                "courses:read",
                "courses:update",
                "grades:create",
                "grades:read",
                "grades:update",
            ],
            "student": [
                "courses:read",
                "grades:read",
            ],
        }
        return permissions_map.get(role, [])
