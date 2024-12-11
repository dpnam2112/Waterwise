from enum import StrEnum
from typing import Optional
from sqlalchemy import String, Integer, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base
from core.db.mixins import TimestampMixin
import uuid

class Gender(StrEnum):
    MALE = 'M'
    FEMALE = 'F'

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gender: Mapped[Optional[Gender]] = mapped_column(String, nullable=True)
    email_address: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight: Mapped[Optional[float]] = mapped_column(Integer, nullable=True)  # Nullable field
    height: Mapped[Optional[float]] = mapped_column(Integer, nullable=True)  # Nullable field
    wake_up_time: Mapped[Optional[Time]] = mapped_column(Time, nullable=True)  # Nullable field
    bed_time: Mapped[Optional[Time]] = mapped_column(Time, nullable=True)  # Nullable field
