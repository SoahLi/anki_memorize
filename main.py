from anki.models import ModelManager, NotetypeDict
from aqt import gui_hooks, mw
from util.decorators import require_vars
import json
from util.getters import get_mm

from aqt import mw


def test():
    if not mw or not mw.col or not mw.col.db:
        print("bruh")
        return

    cards = mw.col.db.all("select * from notes limit 1113")

    for card in cards:
        print(card)

    for model in mw.col.models.all():
        print(json.dumps(model, indent=4))


def main():
    gui_hooks.main_window_did_init.append(test)
