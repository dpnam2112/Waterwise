from typing import Optional
from uuid import UUID
from core.controller import BaseController
from machine.models import User
from machine.repositories import UserRepository


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model_class=User, repository=user_repository)
        self.user_repository = user_repository

    async def get(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.first(where_=[User.id == user_id])
