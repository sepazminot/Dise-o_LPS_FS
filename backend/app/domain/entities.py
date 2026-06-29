"""
Domain entities for Authentication.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Role(str, Enum):
    """User roles."""
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


@dataclass
class User:
    """User entity."""
    id: str
    email: str
    full_name: str
    role: Role
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class TokenPair:
    """JWT token pair."""
    access_token: str
    refresh_token: str
    expires_in: int  # seconds


@dataclass
class TokenPayload:
    """JWT token payload."""
    sub: str  # user_id
    email: str
    role: str
    exp: int  # expiration timestamp
    iat: int  # issued at
    type: str = "access"  # access or refresh


class InvalidCredentialsError(Exception):
    """Invalid credentials provided."""
    pass


class TokenExpiredError(Exception):
    """Token has expired."""
    pass


class InvalidTokenError(Exception):
    """Invalid token provided."""
    pass


class UserNotFoundError(Exception):
    """User not found."""
    pass


class UserAlreadyExistsError(Exception):
    """User with email already exists."""
    pass
