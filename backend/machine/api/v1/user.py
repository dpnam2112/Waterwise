from fastapi import APIRouter, HTTPException
import fastapi

from core.response.api_response import Ok
from machine.api.v1.deps import CurrentUserID, UserControllerDep
from machine.schemas.models.v1.user import UserBase

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=Ok[UserBase])
async def get_me(
    user_id: CurrentUserID,
    user_controller: UserControllerDep

):
    user = await user_controller.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"User is not found. id = {user_id}"
        )
    return Ok[UserBase](data=user)

@router.patch("/me")
async def update_me():
    pass
