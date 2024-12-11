from typing import Annotated
from uuid import UUID

from fastapi import Depends, Security

from machine.api.deps import get_current_user_id
from machine.controllers.auth import AuthController
from machine.controllers.user import UserController
from machine.providers.internal import InternalProvider


AuthControllerDep = Annotated[AuthController, Depends(InternalProvider().get_auth_controller)]
CurrentUserID = Annotated[UUID, Security(get_current_user_id)]
UserControllerDep = Annotated[UserController, Depends(InternalProvider().get_user_controller)]
