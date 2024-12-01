from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from machine.clients.google import GoogleOAuthClient
from machine.clients.injectors import get_google_oauth_client
from core.response import Ok

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


@router.get("/callback")
async def google_callback(
    code: str, oauth_client: GoogleOAuthClient = Depends(get_google_oauth_client)
):
    """
    Handles the OAuth callback from Google.

    Args:
        code (str): Authorization code from Google.
        oauth_client (GoogleOAuthClient): The injected OAuth client.

    Returns:
        dict: User info retrieved from Google.
    """
    token_data = await oauth_client.exchange_code_for_token(code=code)
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token not found in response")
    user_info = await oauth_client.fetch_user_info(access_token=access_token)
    return {"user": user_info}
