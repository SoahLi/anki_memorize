from anki.models import ModelManager, NotetypeDict
from aqt import mw


def get_mm():
    if not mw or not mw.col or not mw.col.models:
        raise Exception("Anki collection or model manager not available.")
    return mw.col.models


def get_or_create_yt_model(mm: ModelManager) -> NotetypeDict:
    model_name = "YouTube-to-Anki-v1"

    # Check if it already exists
    existing_model = mm.by_name(model_name)
    if existing_model:
        return existing_model

    # 1. Create a new model object
    model = mm.new(model_name)

    # 2. Add fields (The data storage)
    mm.add_field(model, mm.new_field("Front"))
    mm.add_field(model, mm.new_field("Back"))
    mm.add_field(model, mm.new_field("YouTubeURL"))  # For your searching logic
    mm.add_field(model, mm.new_field("Timestamp"))

    # 3. Add a Template (The visual card)
    template = mm.new_template("Card 1")
    template["qfmt"] = "{{Front}}<br>{{YouTubeURL}}"  # Front side HTML
    template["afmt"] = (
        "{{FrontSide}}<hr id=answer>{{Back}}<br>Time: {{Timestamp}}"  # Back side HTML
    )
    mm.add_template(model, template)

    # 4. Save the model to the collection
    mm.add(model)

    return model
