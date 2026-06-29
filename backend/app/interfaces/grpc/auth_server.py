"""
gRPC server implementation for AuthService.
"""
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import grpc
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.grpc import auth_pb2, auth_pb2_grpc
from app.application.auth_service import AuthService
from app.domain.entities import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
    TokenExpiredError,
    InvalidTokenError,
)


class AuthGrpcService(auth_pb2_grpc.AuthServiceServicer):
    """gRPC service implementation for authentication."""

    def __init__(self, session_factory):
        """Initialize gRPC service with session factory."""
        self.session_factory = session_factory

    async def _get_service(self) -> AuthService:
        """Get auth service instance with session."""
        session: AsyncSession = self.session_factory()
        return AuthService(session)

    def _role_to_proto(self, role: str) -> int:
        """Convert domain role to protobuf enum."""
        role_map = {
            "admin": auth_pb2.ROLE_ADMIN,
            "teacher": auth_pb2.ROLE_TEACHER,
            "student": auth_pb2.ROLE_STUDENT,
        }
        return role_map.get(role, auth_pb2.ROLE_UNSPECIFIED)

    def _user_to_proto(self, user) -> auth_pb2.User:
        """Convert domain user to protobuf message."""
        created_at = Timestamp()
        if user.created_at:
            created_at.FromDatetime(user.created_at)

        updated_at = Timestamp()
        if user.updated_at:
            updated_at.FromDatetime(user.updated_at)

        return auth_pb2.User(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=self._role_to_proto(user.role.value),
            is_active=user.is_active,
            created_at=created_at,
            updated_at=updated_at,
        )

    async def Register(self, request, context):
        """Register a new user."""
        try:
            service = await self._get_service()
            user, token_pair = await service.register(
                email=request.email,
                password=request.password,
                full_name=request.full_name,
                role=request.role.name.lower() if request.role else "student",
            )

            return auth_pb2.RegisterResponse(
                user=self._user_to_proto(user),
                access_token=token_pair.access_token,
                refresh_token=token_pair.refresh_token,
                expires_in=token_pair.expires_in,
            )
        except UserAlreadyExistsError as e:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(str(e))
            return auth_pb2.RegisterResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.RegisterResponse()

    async def Login(self, request, context):
        """Login user."""
        try:
            service = await self._get_service()
            user, token_pair = await service.login(
                email=request.email,
                password=request.password,
            )

            return auth_pb2.LoginResponse(
                user=self._user_to_proto(user),
                access_token=token_pair.access_token,
                refresh_token=token_pair.refresh_token,
                expires_in=token_pair.expires_in,
            )
        except InvalidCredentialsError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(str(e))
            return auth_pb2.LoginResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.LoginResponse()

    async def RefreshToken(self, request, context):
        """Refresh access token."""
        try:
            service = await self._get_service()
            token_pair = await service.refresh_token(
                refresh_token=request.refresh_token,
            )

            return auth_pb2.RefreshTokenResponse(
                access_token=token_pair.access_token,
                refresh_token=token_pair.refresh_token,
                expires_in=token_pair.expires_in,
            )
        except InvalidCredentialsError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(str(e))
            return auth_pb2.RefreshTokenResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.RefreshTokenResponse()

    async def ValidateToken(self, request, context):
        """Validate access token."""
        try:
            service = await self._get_service()
            valid, user, permissions = await service.validate_token(
                access_token=request.access_token,
            )

            return auth_pb2.ValidateTokenResponse(
                valid=valid,
                user=self._user_to_proto(user) if user else None,
                permissions=permissions,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.ValidateTokenResponse(valid=False)

    async def GetProfile(self, request, context):
        """Get user profile."""
        # For now, return error since we need user_id from token
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("GetProfile requires authentication context")
        return auth_pb2.GetProfileResponse()

    async def ChangePassword(self, request, context):
        """Change user password."""
        # For now, return error since we need user_id from token
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("ChangePassword requires authentication context")
        return auth_pb2.ChangePasswordResponse()
