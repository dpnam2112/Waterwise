from typing import Optional
from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str  # The access token issued by the OAuth provider
    refresh_token: str  # The refresh token used to obtain a new access token
    token_type: str = "bearer"  # Default to "bearer" as per OAuth 2.0 spec
    expires_in: Optional[int] = 3600  # The lifespan of the access token in seconds (optional, can be included in the response)
