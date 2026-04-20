import os

from sqlmodel import SQLModel, create_engine

from ..types import Platform, PlatformItem  # noqa: F401

USER_FOLDER = os.path.join(os.path.dirname(__file__), "..", "user_folders")
DB_PATH = os.path.join(USER_FOLDER, "database.db")

engine = None


def init_db_engine():
    global engine
    os.makedirs(USER_FOLDER, exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    SQLModel.metadata.create_all(engine)
