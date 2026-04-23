from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .PlatformItem import PlatformItem
from .PlatformItemFilterLink import PlatformItemFilterLink


class Filter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    platform_items: list["PlatformItem"] = Relationship(
        back_populates="filters", link_model=PlatformItemFilterLink
    )
