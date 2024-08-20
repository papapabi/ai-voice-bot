from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.config import get_settings

X_API_KEY = APIKeyHeader(name="x-api-key", auto_error=False)
settings = get_settings()


def check_api_key(
    x_api_key: str = Security(X_API_KEY),
) -> str:
    """Validates an API key from the HTTP header.

    Args:
        x_api_key: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if x_api_key == settings.api_key:
        return x_api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
