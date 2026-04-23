from typing import Optional

from sqlmodel import Field, SQLModel


class PlatformItemFilterLink(SQLModel, table=True):
    platform_item_id: Optional[int] = Field(
        default=None, foreign_key="platformitem.id", primary_key=True
    )
    filter_id: Optional[int] = Field(
        default=None, foreign_key="filter.id", primary_key=True
    )
