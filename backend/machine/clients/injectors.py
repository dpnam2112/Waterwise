# Dependency to provide GoogleOAuthClient
from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient
from core.settings import Settings, get_settings
from .google import GoogleOAuthClient


async def get_google_oauth_client(settings: Annotated[Settings, Depends(get_settings)]):
    """
    Dependency to provide a pre-configured GoogleOAuthClient.

    Args:
        settings (GoogleSettings): Injected settings object.
        httpx_client (AsyncClient): Injected HTTPX client.

    Returns:
        GoogleOAuthClient: Configured Google OAuth client.
    """
    async with AsyncClient() as httpx_client:
        yield GoogleOAuthClient(settings=settings, httpx_client=httpx_client)
