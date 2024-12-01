from httpx import AsyncClient
from httpx import codes as status_codes
from typing import Optional
from core.settings import GoogleSettings
from urllib.parse import urljoin

class GoogleOAuthClient:
    """Handles interactions with Google's OAuth API using an injected httpx.AsyncClient."""

    def __init__(self, settings: GoogleSettings, httpx_client: Optional[AsyncClient] = None):
        """
        Initialize the client.

        Args:
            settings (GoogleSettings): The settings object for Google API configuration.
            httpx_client (Optional[AsyncClient]): An optional pre-configured HTTPX client.
        """
        self.settings = settings
        self.httpx_client = httpx_client

    def _get_httpx_client(self, method_client: Optional[AsyncClient]) -> AsyncClient:
        """
        Retrieve the HTTPX client to use for a method call.

        Args:
            method_client (Optional[AsyncClient]): The client passed to a specific method.

        Returns:
            AsyncClient: The HTTPX client to use.

        Raises:
            ValueError: If no client is available.
        """
        client = method_client or self.httpx_client
        if not client:
            raise ValueError("httpx_client must be provided either at class or method level.")
        return client

    @property
    def redirect_auth_url(self) -> str:
        """Property to generate the Google OAuth login URL."""
        scope_str = "%20".join(self.settings.GOOGLE_SCOPES)
        return (
            f"{self.settings.GOOGLE_AUTH_URL}?"
            f"client_id={self.settings.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={self.settings.GOOGLE_CALLBACK_URI}&"
            f"response_type=code&"
            f"scope={scope_str}"
        )

    @property
    def token_url(self) -> str:
        """Property to get the Google OAuth token URL."""
        return self.settings.GOOGLE_TOKEN_URL

    @property
    def user_info_url(self) -> str:
        """Property to get the Google user info URL."""
        return urljoin(self.settings.GOOGLE_API_BASE_URI, "oauth2/v3/userinfo")

    async def exchange_code_for_token(self, code: str, client: Optional[AsyncClient] = None) -> dict:
        """
        Exchange authorization code for access token.

        Args:
            code (str): The authorization code received from Google.
            client (Optional[AsyncClient]): Optional HTTPX client for the request.

        Returns:
            dict: The token response data.
        """
        httpx_client = self._get_httpx_client(client)
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_CALLBACK_URI,
            "grant_type": "authorization_code",
        }
        response = await httpx_client.post(self.token_url, data=data)
        response.raise_for_status()
        return response.json()

    async def fetch_user_info(self, access_token: str, client: Optional[AsyncClient] = None) -> dict:
        """
        Fetch user information using the access token.

        Args:
            access_token (str): The access token for the user.
            client (Optional[AsyncClient]): Optional HTTPX client for the request.

        Returns:
            dict: The user's information from Google.
        """
        httpx_client = self._get_httpx_client(client)
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await httpx_client.get(self.user_info_url, headers=headers)
        response.raise_for_status()
        return response.json()
