from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from machine.api.v1.deps import AuthControllerDep
from machine.clients.google import GoogleOAuthClient
from machine.clients.injectors import get_google_oauth_client
from core.response import Ok
from machine.schemas.models.v1.token import TokenPair

router = APIRouter(prefix="/google", tags=["auth"])

@router.get("/login", response_model=Ok[str])
async def google_login(
    oauth_client: Annotated[GoogleOAuthClient, Depends(get_google_oauth_client)]
):
    """
    Redirects the user to Google's OAuth login page.

    Args:
        oauth_client (GoogleOAuthClient): The injected OAuth client.

    Returns:
        RedirectResponse: Redirects to Google's OAuth login page.
    """
    return Ok(data=oauth_client.redirect_auth_url)


@router.get("/callback", response_model=TokenPair)
async def google_callback(
    code: str,
    auth_controller: AuthControllerDep
):
    """
    Handles the OAuth callback from Google.

    Args:
        code (str): Authorization code from Google.
        oauth_client (GoogleOAuthClient): The injected OAuth client.

    Returns:
        dict: User info retrieved from Google.
    """
    return await auth_controller.google_callback(code)
