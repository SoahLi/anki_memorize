from typing import Optional

from anki.decks import DeckId
from anki.models import ModelManager, NotetypeDict
from aqt import mw


def get_mw():
    if not mw:
        raise Exception("Anki main window not available.")
    return mw


def get_col():
    if not mw or not mw.col:
        raise Exception("Anki collection not available.")
    return mw.col


def get_mm():
    if not mw or not mw.col or not mw.col.models:
        raise Exception("Anki collection or model manager not available.")
    return mw.col.models


def get_or_create_sm_memorize_model(mm: Optional[ModelManager] = None) -> NotetypeDict:
    if mm is None:
        mm = get_mm()

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
    mm.add_field(model, mm.new_field("url"))
    mm.add_field(model, mm.new_field("thumbnail"))
    # For now, this is associated with the id of the youtube video, not the record in the custom database
    mm.add_field(model, mm.new_field("platformItemId"))
    # this would have been stored in the internal database
    mm.add_field(model, mm.new_field("platformName"))
    # I would prefer if this was filters (plural) but fields are only strings
    mm.add_field(model, mm.new_field("filter"))

    mm.add_field(model, mm.new_field("title"))
    mm.add_field(model, mm.new_field("video_snippet"))
    mm.add_field(model, mm.new_field("filters"))

    # mm.add_field(model, mm.new_field("Timestamp"))

    # 3. Add a Template (The visual card)
    template = mm.new_template("Card 1")
    template["qfmt"] = """
    <div style="display: flex; align-items: center; justify-content: center; height: 200px;">
      <div style="flex: 1; display: flex; align-items: center; justify-content: center; border-right: 1px solid #ccc; height: 100%;">
        <span style="font-size: 1.5em;">{{Front}}</span>
      </div>
      <div style="flex: 1; display: flex; align-items: center; justify-content: center; height: 100%;">
        <img src="{{thumbnail}}" alt="thumbnail" style="max-width: 100%; max-height: 180px; display: block; margin: auto;" />
      </div>
    </div>
    """
    template["afmt"] = (
        # "{{FrontSide}}<hr id=answer>{{Back}}<br>Time: {{Timestamp}}"  # Back side HTML
        "{{FrontSide}}<hr id=answer>{{Back}}"  # Back side HTML
    )

    mm.add_template(model, template)

    # 4. Save the model to the collection
    mm.add(model)

    return model


def get_or_create_sm_memorize_deck() -> DeckId:
    col = get_col()
    deck_name = "SM_memorize"
    # Check if the deck already exists
    existing_deck_id = col.decks.id_for_name(deck_name)
    if existing_deck_id:
        return existing_deck_id
    # Create a new deck
    new_deck_id = col.decks.id(deck_name)
    if not new_deck_id:
        raise Exception("Failed to create or retrieve the deck ID.")
    return new_deck_id
