"""
Authentication and authorization utilities.
JWT token validation and OAuth 2.0 integration placeholder.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

security = HTTPBearer()


class TokenData(BaseModel):
    """Token payload data."""

    username: Optional[str] = None
    scopes: list[str] = []
    exp: Optional[datetime] = None


class User(BaseModel):
    """User model."""

    username: str
    scopes: list[str] = []
    is_active: bool = True


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.

    Args:
        data: Token payload
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """
    Decode and validate JWT token.

    Args:
        token: JWT token string

    Returns:
        Token data

    Raises:
        HTTPException: If token is invalid
    """
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception

        scopes: list[str] = payload.get("scopes", [])
        exp_timestamp: Optional[float] = payload.get("exp")
        exp = datetime.fromtimestamp(exp_timestamp) if exp_timestamp else None

        return TokenData(username=username, scopes=scopes, exp=exp)

    except JWTError as e:
        logger.warning("jwt_decode_error", error=str(e))
        raise credentials_exception


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    Dependency to get current authenticated user.

    Args:
        credentials: HTTP Authorization credentials

    Returns:
        Current user

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    token_data = decode_access_token(token)

    if token_data.username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # In production, fetch user from database
    # For now, return user from token data
    user = User(username=token_data.username, scopes=token_data.scopes)

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


async def require_scope(required_scope: str, user: User = Depends(get_current_user)) -> User:
    """
    Dependency to require specific scope.

    Args:
        required_scope: Required scope (e.g., 'cutoff.read', 'cutoff.write')
        user: Current user

    Returns:
        Current user if scope is present

    Raises:
        HTTPException: If user doesn't have required scope
    """
    if required_scope not in user.scopes:
        logger.warning(
            "scope_denied",
            user=user.username,
            required_scope=required_scope,
            user_scopes=user.scopes,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Required scope '{required_scope}' not present",
        )

    return user


# Dependency factories for common scopes
def require_read_scope(user: User = Depends(get_current_user)) -> User:
    """Require cutoff.read scope."""
    return require_scope("cutoff.read", user)


def require_write_scope(user: User = Depends(get_current_user)) -> User:
    """Require cutoff.write scope."""
    return require_scope("cutoff.write", user)


def require_admin_scope(user: User = Depends(get_current_user)) -> User:
    """Require cutoff.admin scope."""
    return require_scope("cutoff.admin", user)


# Optional authentication for development
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
) -> Optional[User]:
    """
    Optional authentication - returns None if no credentials provided.
    Useful for endpoints that support both authenticated and anonymous access.

    Args:
        credentials: Optional HTTP Authorization credentials

    Returns:
        Current user or None
    """
    if credentials is None:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
