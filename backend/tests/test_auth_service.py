"""
Tests for AuthService.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.auth_service import AuthService
from app.domain.entities import (
    User,
    TokenPair,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.infrastructure.auth.jwt import JWTAdapter


@pytest.mark.asyncio
async def test_register_user(db_session: AsyncSession):
    """Test user registration."""
    auth_service = AuthService(db_session)
    user, token_pair = await auth_service.register(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User",
        role="student",
    )
    
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.role.value == "student"
    assert user.is_active is True
    assert token_pair.access_token
    assert token_pair.refresh_token
    assert token_pair.expires_in > 0


@pytest.mark.asyncio
async def test_register_duplicate_email(db_session: AsyncSession):
    """Test registration with duplicate email fails."""
    auth_service = AuthService(db_session)
    
    # First registration
    await auth_service.register(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User",
    )
    
    # Second registration with same email should fail
    with pytest.raises(UserAlreadyExistsError):
        await auth_service.register(
            email="test@example.com",
            password="AnotherPass123!",
            full_name="Another User",
        )


@pytest.mark.asyncio
async def test_login_user(db_session: AsyncSession):
    """Test user login."""
    auth_service = AuthService(db_session)
    
    # Register user first
    await auth_service.register(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User",
    )
    
    # Login
    user, token_pair = await auth_service.login(
        email="test@example.com",
        password="SecurePass123!",
    )
    
    assert user.email == "test@example.com"
    assert token_pair.access_token
    assert token_pair.refresh_token


@pytest.mark.asyncio
async def test_login_invalid_credentials(db_session: AsyncSession):
    """Test login with invalid credentials fails."""
    auth_service = AuthService(db_session)
    
    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            email="nonexistent@example.com",
            password="WrongPass123!",
        )


@pytest.mark.asyncio
async def test_refresh_token(db_session: AsyncSession):
    """Test token refresh."""
    auth_service = AuthService(db_session)
    
    # Register user
    user, token_pair = await auth_service.register(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User",
    )
    
    # Refresh token
    new_token_pair = await auth_service.refresh_token(token_pair.refresh_token)
    
    assert new_token_pair.access_token
    assert new_token_pair.refresh_token
    assert new_token_pair.expires_in > 0


@pytest.mark.asyncio
async def test_validate_token(db_session: AsyncSession):
    """Test token validation."""
    auth_service = AuthService(db_session)
    
    # Register user
    user, token_pair = await auth_service.register(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User",
    )
    
    # Validate token
    valid, validated_user, permissions = await auth_service.validate_token(
        token_pair.access_token,
    )
    
    assert valid is True
    assert validated_user.email == "test@example.com"
    assert len(permissions) > 0


@pytest.mark.asyncio
async def test_validate_invalid_token(db_session: AsyncSession):
    """Test validation of invalid token."""
    auth_service = AuthService(db_session)
    
    valid, user, permissions = await auth_service.validate_token("invalid_token")
    
    assert valid is False
    assert user is None
    assert permissions == []


@pytest.mark.asyncio
async def test_get_profile(db_session: AsyncSession):
    """Test getting user profile."""
    auth_service = AuthService(db_session)
    
    # Register user
    user, _ = await auth_service.register(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User",
    )
    
    # Get profile
    profile = await auth_service.get_profile(user.id)
    
    assert profile.email == "test@example.com"
    assert profile.full_name == "Test User"


@pytest.mark.asyncio
async def test_get_profile_not_found(db_session: AsyncSession):
    """Test getting profile for non-existent user."""
    auth_service = AuthService(db_session)
    
    with pytest.raises(UserNotFoundError):
        await auth_service.get_profile("non-existent-id")


@pytest.mark.asyncio
async def test_change_password(db_session: AsyncSession):
    """Test password change."""
    auth_service = AuthService(db_session)
    
    # Register user
    user, _ = await auth_service.register(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User",
    )
    
    # Change password
    success = await auth_service.change_password(
        user_id=user.id,
        current_password="SecurePass123!",
        new_password="NewSecurePass456!",
    )
    
    assert success is True
    
    # Login with new password should work
    user, _ = await auth_service.login(
        email="test@example.com",
        password="NewSecurePass456!",
    )
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_change_password_wrong_current(db_session: AsyncSession):
    """Test password change with wrong current password fails."""
    auth_service = AuthService(db_session)
    
    # Register user
    user, _ = await auth_service.register(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User",
    )
    
    # Try to change with wrong current password
    with pytest.raises(InvalidCredentialsError):
        await auth_service.change_password(
            user_id=user.id,
            current_password="WrongPass123!",
            new_password="NewSecurePass456!",
        )


def test_jwt_adapter_create_token():
    """Test JWT adapter token creation."""
    jwt_adapter = JWTAdapter()
    
    access_token, refresh_token, expires_in = jwt_adapter.create_token_pair(
        user_id="test-id",
        email="test@example.com",
        role="student",
    )
    
    assert access_token
    assert refresh_token
    assert expires_in > 0


def test_jwt_adapter_validate_token():
    """Test JWT adapter token validation."""
    jwt_adapter = JWTAdapter()
    
    # Create token
    access_token, _, _ = jwt_adapter.create_token_pair(
        user_id="test-id",
        email="test@example.com",
        role="student",
    )
    
    # Validate token
    payload = jwt_adapter.validate_access_token(access_token)
    
    assert payload.sub == "test-id"
    assert payload.email == "test@example.com"
    assert payload.role == "student"
