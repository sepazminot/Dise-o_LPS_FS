"""
Database repositories for authentication.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.infrastructure.database.models import User
from app.domain.entities import User as UserEntity, Role, UserAlreadyExistsError, UserNotFoundError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    """Repository for User entity."""

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def _to_entity(self, model: User) -> UserEntity:
        """Convert database model to domain entity."""
        return UserEntity(
            id=str(model.id),
            email=model.email,
            full_name=model.full_name,
            role=Role(model.role),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create(
        self,
        email: str,
        password: str,
        full_name: str,
        role: str = "student",
    ) -> UserEntity:
        """Create a new user."""
        # Check if user exists
        existing = await self.get_by_email(email)
        if existing:
            raise UserAlreadyExistsError(f"User with email {email} already exists")

        user = User(
            email=email,
            password_hash=self.hash_password(password),
            full_name=full_name,
            role=role,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return self._to_entity(user)

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """Get user by ID."""
        from uuid import UUID
        result = await self.session.execute(
            select(User).where(User.id == UUID(user_id))
        )
        user = result.scalar_one_or_none()
        if user is None:
            return None
        return self._to_entity(user)

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Get user by email."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        if user is None:
            return None
        return self._to_entity(user)

    async def verify_credentials(
        self,
        email: str,
        password: str,
    ) -> UserEntity | None:
        """Verify user credentials."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        if user is None:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        if not user.is_active:
            return None
        return self._to_entity(user)

    async def update_password(
        self,
        user_id: str,
        new_password: str,
    ) -> UserEntity:
        """Update user password."""
        from uuid import UUID
        result = await self.session.execute(
            select(User).where(User.id == UUID(user_id))
        )
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFoundError(f"User with id {user_id} not found")

        user.password_hash = self.hash_password(new_password)
        await self.session.commit()
        await self.session.refresh(user)
        return self._to_entity(user)
