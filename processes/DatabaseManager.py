import os
from abc import ABC

from anki.notes import Note as AnkiNote
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, text

from ..tables import Filter, Platform, PlatformItem  # noqa: F401
from ..types.Note import Note
from ..util.config import config_get
from ..util.getters import (
    get_col,
    get_or_create_sm_memorize_deck,
    get_or_create_sm_memorize_model,
)
from .SyncManager import SyncManager

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
                    SELECT 1 FROM platform WHERE name = :name
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

    # GETTERS
    @classmethod
    def get_engine(cls):
        if not cls.db_connection:
            raise Exception(
                "Engine variable is null, should have been initialized before accessing"
            )

        return cls.db_connection

    @classmethod
    def get_platform_id_by_name(cls, platform_name: str) -> int:
        with cls.db_connection.begin() as connection:
            result = connection.execute(text("select * from platform")).fetchall()
            for row in result:
                print(row)
            result = connection.execute(
                text("""
                SELECT id FROM platform
                WHERE name = :platform_name
                """),
                {"platform_name": platform_name},
            ).fetchone()

            if result is None:
                raise ValueError(f"Platform with name '{platform_name}' not found.")

            return result[0]

    @classmethod
    def create_platform_item(cls, platform_id: int) -> int:
        with cls.db_connection.begin() as connection:
            result = connection.execute(
                text("""
                INSERT INTO platformitem (platform_id)
                VALUES (:platform_id)
                """),
                {"platform_id": platform_id},
            )
            return result.lastrowid

    # move these methods out of this class at some point

    @classmethod
    def add_note(cls, note: Note):
        col = get_col()
        model = get_or_create_sm_memorize_model()

        platform_item_id = DatabaseManager.create_platform_item(
            DatabaseManager.get_platform_id_by_name("youtube")  # magic string
        )

        ankiNote = AnkiNote(col, model)
        ankiNote["platformItemId"] = str(
            platform_item_id
        )  # store platform item id for reference
        SyncManager.sync_note(note, ankiNote)
        col.add_note(ankiNote, get_or_create_sm_memorize_deck())
