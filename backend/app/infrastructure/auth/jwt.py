"""
JWT RS256 infrastructure adapter.
"""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from app.domain.entities import TokenPayload, TokenExpiredError, InvalidTokenError
from app.infrastructure.config.settings import get_settings

settings = get_settings()


class JWTAdapter:
    """JWT RS256 adapter for token generation and validation."""

    def __init__(
        self,
        private_key_path: Optional[str] = None,
        public_key_path: Optional[str] = None,
    ):
        """Initialize JWT adapter with RS256 keys."""
        self.private_key_path = private_key_path or settings.JWT_PRIVATE_KEY_PATH
        self.public_key_path = public_key_path or settings.JWT_PUBLIC_KEY_PATH
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        self.issuer = settings.JWT_ISSUER
        self.audience = settings.JWT_AUDIENCE

    def _load_private_key(self) -> str:
        """Load private key from file."""
        path = Path(self.private_key_path)
        if not path.exists():
            # For development, generate a fallback key
            return self._generate_fallback_private_key()
        return path.read_text()

    def _load_public_key(self) -> str:
        """Load public key from file."""
        path = Path(self.public_key_path)
        if not path.exists():
            # For development, generate a fallback key
            return self._generate_fallback_public_key()
        return path.read_text()

    def _generate_fallback_private_key(self) -> str:
        """Generate fallback private key for development (NOT FOR PRODUCTION)."""
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

    def _generate_fallback_public_key(self) -> str:
        """Generate fallback public key for development (NOT FOR PRODUCTION)."""
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    def create_access_token(
        self,
        user_id: str,
        email: str,
        role: str,
    ) -> str:
        """Create JWT access token."""
        now = datetime.utcnow()
        expire = now + timedelta(minutes=self.access_token_expire_minutes)
        
        payload = {
            "sub": user_id,
            "email": email,
            "role": role,
            "exp": expire.timestamp(),
            "iat": now.timestamp(),
            "type": "access",
            "iss": self.issuer,
            "aud": self.audience,
        }
        
        private_key = self._load_private_key()
        return jwt.encode(payload, private_key, algorithm=self.algorithm)

    def create_refresh_token(
        self,
        user_id: str,
        email: str,
    ) -> str:
        """Create JWT refresh token."""
        now = datetime.utcnow()
        expire = now + timedelta(days=self.refresh_token_expire_days)
        
        payload = {
            "sub": user_id,
            "email": email,
            "exp": expire.timestamp(),
            "iat": now.timestamp(),
            "type": "refresh",
            "iss": self.issuer,
            "aud": self.audience,
        }
        
        private_key = self._load_private_key()
        return jwt.encode(payload, private_key, algorithm=self.algorithm)

    def create_token_pair(
        self,
        user_id: str,
        email: str,
        role: str,
    ) -> tuple[str, str, int]:
        """Create access and refresh token pair."""
        access_token = self.create_access_token(user_id, email, role)
        refresh_token = self.create_refresh_token(user_id, email)
        expires_in = self.access_token_expire_minutes * 60
        return access_token, refresh_token, expires_in

    def decode_token(self, token: str) -> TokenPayload:
        """Decode and validate JWT token."""
        try:
            public_key = self._load_public_key()
            payload = jwt.decode(
                token,
                public_key,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                audience=self.audience,
            )
            return TokenPayload(**payload)
        except ExpiredSignatureError as e:
            raise TokenExpiredError("Token has expired") from e
        except JWTError as e:
            raise InvalidTokenError("Invalid token") from e

    def validate_access_token(self, token: str) -> TokenPayload:
        """Validate access token."""
        payload = self.decode_token(token)
        if payload.type != "access":
            raise InvalidTokenError("Invalid token type")
        return payload

    def validate_refresh_token(self, token: str) -> TokenPayload:
        """Validate refresh token."""
        payload = self.decode_token(token)
        if payload.type != "refresh":
            raise InvalidTokenError("Invalid token type")
        return payload


# Global instance
jwt_adapter = JWTAdapter()
