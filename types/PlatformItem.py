from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class PlatformItemFilterLink(SQLModel, table=True):
    platform_item_id: Optional[int] = Field(
        default=None, foreign_key="platformitem.id", primary_key=True
    )
    filter_id: Optional[int] = Field(
        default=None, foreign_key="filter.id", primary_key=True
    )


class Filter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    platform_items: List["PlatformItem"] = Relationship(
        back_populates="filters", link_model=PlatformItemFilterLink
    )


class PlatformItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    transcript: str
    platform_id: int = Field(foreign_key="platform.id")
    filters: List[Filter] = Relationship(
        back_populates="platform_items", link_model=PlatformItemFilterLink
    )
