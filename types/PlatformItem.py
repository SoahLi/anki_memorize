from typing import List

from sqlalchemy.util import NoneType
from sqlmodel import Field, SQLModel

from .Filter import Filter


class PlatformItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    transcript: str
    platform_id: int = Field(foreign_key="platform.id")
    filters: List[Filter] = Field(default=NoneType)
