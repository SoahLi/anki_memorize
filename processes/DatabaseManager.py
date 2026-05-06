import os
from abc import ABC

from anki.notes import Note
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, text

from ..tables import Filter, Platform, PlatformItem  # noqa: F401
from ..types.AnkiCard import AnkiCard
from ..util.config import config_get
from ..util.getters import get_col, get_or_create_yt_model

USER_FOLDER = os.path.join(os.path.dirname(__file__), "..", "user_folders")
DB_PATH = os.path.join(USER_FOLDER, "database.db")


# this should be a singleton
class DatabaseManager(ABC):
    db_connection: Engine = None

    @classmethod
    def create(cls):
        if not hasattr(DatabaseManager, "_instance"):
            DatabaseManager._instance = DatabaseManager()
            cls.init_db_engine()

    @classmethod
    def seed_database(cls):
        if cls.db_connection is None:
            raise Exception(
                "Engine variable is null, should have been initialized before accessing"
            )
        with cls.db_connection.begin() as connection:
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

    @classmethod
    def init_db_engine(cls):
        global engine
        print(f"sqlite:///{DB_PATH}")
        os.makedirs(USER_FOLDER, exist_ok=True)
        cls.db_connection = create_engine(f"sqlite:///{DB_PATH}")
        print(f"engine is {cls.db_connection}")
        SQLModel.metadata.create_all(cls.db_connection)
        cls.seed_database()

    @classmethod
    def get_engine(cls):
        if not cls.db_connection:
            raise Exception(
                "Engine variable is null, should have been initialized before accessing"
            )

        return cls.db_connection

    # move these methods out of this class at some point

    def add_card(self, card: AnkiCard):
        col = get_col()
        model = get_or_create_yt_model()
        note = Note(col, model)
        col.add_note()
