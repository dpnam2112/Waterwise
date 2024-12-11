from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import time
from machine.models.user import Gender

class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[Gender]
    email_address: EmailStr
    age: Optional[int]
    weight: Optional[float] = None
    height: Optional[float] = None
    wake_up_time: Optional[time] = None
    bed_time: Optional[time] = None

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Gender] = None
    email_address: Optional[EmailStr] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    wake_up_time: Optional[time] = None
    bed_time: Optional[time] = None
