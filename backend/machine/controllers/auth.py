import jwt
from datetime import datetime, timedelta
from machine.clients.google import GoogleOAuthClient
from machine.repositories.user import UserRepository
from core.db import Transactional
from machine.models import User
from machine.schemas.models.v1.token import TokenPair
from core.settings import Settings
from fastapi import HTTPException, status

class AuthController:
    def __init__(
        self,
        user_repository: UserRepository,
        google_outh_client: GoogleOAuthClient,
        settings: Settings
    ):
        self.user_repository = user_repository
        self.google_oauth_client = google_outh_client 
        self.settings = settings

    @Transactional()
    async def google_callback(self, authorization_code: str) -> TokenPair:
        """
        Handle OAuth callback. If the user's email does not exist in the database, create a new one.
        After that, return a token pair (access token + refresh token).

        Args:
        - authorization_code: Authorization code received from Google.

        Return:
        - TokenPair: Model instance containing the access token and refresh token.
        """
        # Step 1: Exchange authorization code for an access token from Google (Google's token is not used here)
        token_response = await self.google_oauth_client.exchange_code_for_token(authorization_code)
        access_token = token_response["access_token"]

        # Step 2: Fetch the user's information from Google
        user_info = await self.google_oauth_client.fetch_user_info(access_token)

        # Step 3: Check if the user already exists in the database by their email address
        existing_user = await self.user_repository.first(where_=[User.email_address == user_info["email"]])
        if not existing_user:
            new_user_data = {
                "email_address": user_info["email"]
            }
            existing_user = await self.user_repository.create(new_user_data, commit=True)

        access_token_jwt = self.create_access_token(
            data={"sub": str(existing_user.id)},
            expires_delta=timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        refresh_token_jwt = self.create_refresh_token(
            data={"sub": str(existing_user.id)},
            expires_delta=timedelta(minutes=self.settings.REFRESH_TOKEN_EXPIRES_MINUTES)
        )

        return TokenPair(
            access_token=access_token_jwt,
            refresh_token=refresh_token_jwt,
            expires_in=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        """
        Create the access token JWT.

        Args:
        - data (dict): The payload data to encode in the token (e.g., user email).
        - expires_delta (timedelta): The expiration time for the access token.

        Returns:
        - str: The encoded JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, data: dict, expires_delta: timedelta) -> str:
        """
        Create the refresh token JWT.

        Args:
        - data (dict): The payload data to encode in the token (e.g., user email).
        - expires_delta (timedelta): The expiration time for the refresh token.

        Returns:
        - str: The encoded JWT refresh token.
        """
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        """
        Decode the JWT token and return the payload (claims).

        Args:
        - token (str): The JWT token to decode.

        Returns:
        - dict: The decoded payload of the token.

        Raises:
        - HTTPException: If the token is invalid or expired.
        """
        try:
            # Decode the JWT token using the secret key and the algorithm specified in the settings
            decoded_token = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,  # Secret key used to sign the JWT
                algorithms=self.settings.JWT_ALGORITHM,  # Algorithm used for signing the JWT
                options={"verify_exp": True}  # Ensure the token is not expired
            )
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error decoding token: {str(e)}",
            )
