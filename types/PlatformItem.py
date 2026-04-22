from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .Filter import Filter
from .PlatformItemFilterLink import PlatformItemFilterLink


class PlatformItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    transcript: str
    platform_id: int = Field(foreign_key="platform.id")
    filters: List[Filter] = Relationship(
        back_populates="platform_items", link_model=PlatformItemFilterLink
    )
