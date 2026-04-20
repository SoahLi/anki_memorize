import os

from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, text

from ..types import Platform, PlatformItem  # noqa: F401
from ..util.config import config_get

USER_FOLDER = os.path.join(os.path.dirname(__file__), "..", "user_folders")
DB_PATH = os.path.join(USER_FOLDER, "database.db")


# use the getter instead of importing this
engine: Engine | None = None


def seed_database():
    if engine is None:
        raise Exception(
            "Engine variable is null, should have been initialized before accessing"
        )
    with engine.begin() as connection:
        # Check if the platforms table is empty

        stmt = text("""
            INSERT INTO filter (name)
            SELECT :name
            WHERE NOT EXISTS (
                SELECT 1 FROM filter WHERE name = :name
            )
        """)

        for name in ["STEM"]:
            connection.execute(stmt, {"name": name})

        stmt = text("""
            INSERT INTO platform (name)
            SELECT :name
            WHERE NOT EXISTS (
                SELECT 1 FROM filter WHERE name = :name
            )
        """)

        platforms = config_get("platforms")
        if platforms is not None:
            for name in platforms:
                connection.execute(stmt, {"name": name})


def init_db_engine():
    global engine
    os.makedirs(USER_FOLDER, exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    print(f"engine is {engine}")
    SQLModel.metadata.create_all(engine)
    seed_database()


def get_engine():
    if not engine:
        raise Exception(
            "Engine variable is null, should have been initialized before accessing"
        )

    return engine
