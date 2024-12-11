from fastapi import Depends, HTTPException
from typing import Annotated
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from machine.controllers.auth import AuthController
from machine.providers.internal import InternalProvider

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

AuthControllerDep = Annotated[AuthController, Depends(InternalProvider().get_auth_controller)]

def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_controller: AuthControllerDep
) -> UUID:
    try:
        decoded_token = auth_controller.decode_token(token)
        user_id = UUID(decoded_token.get("sub"))
        return user_id
    except HTTPException as e:
        raise e
