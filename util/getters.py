from anki.models import ModelManager, NotetypeDict
from aqt import mw

from ..processes.init_user_db import engine


def get_col():
    if not mw or not mw.col:
        raise Exception("Anki collection not available.")
    return mw.col


def get_mm():
    if not mw or not mw.col or not mw.col.models:
        raise Exception("Anki collection or model manager not available.")
    return mw.col.models


def get_or_create_yt_model(mm: ModelManager = get_mm()) -> NotetypeDict:
    model_name = "SM_memorize"

    # Check if it already exists
    existing_model = mm.by_name(model_name)
    if existing_model:
        return existing_model

    # 1. Create a new model object
    model = mm.new(model_name)

    # 2. Add fields (The data storage)
    mm.add_field(model, mm.new_field("Front"))
    mm.add_field(model, mm.new_field("Back"))
    # mm.add_field(model, mm.new_field("Timestamp"))

    # 3. Add a Template (The visual card)
    template = mm.new_template("Card 1")
    template["qfmt"] = "{{Front}}"  # Front side HTML
    template["afmt"] = (
        # "{{FrontSide}}<hr id=answer>{{Back}}<br>Time: {{Timestamp}}"  # Back side HTML
        "{{FrontSide}}<hr id=answer>{{Back}}"  # Back side HTML
    )

    mm.add_template(model, template)

    # 4. Save the model to the collection
    mm.add(model)

    return model


def get_engine():
    if not engine:
        raise Exception(
            "Engine variable is null, should have been initialized before accessing"
        )

    return engine
