from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .PlatformItem import PlatformItem
from .PlatformItemFilterLink import PlatformItemFilterLink


class Filter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    platform_items: List["PlatformItem"] = Relationship(
        back_populates="filters", link_model=PlatformItemFilterLink
    )
