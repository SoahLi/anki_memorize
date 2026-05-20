from abc import ABC

from anki.notes import Note as AnkiNote

from custom_types.Note import Note


class SyncManager(ABC):
    @classmethod
    def sync_note(cls, note: Note, ankiNote: AnkiNote):
        ankiNote["Front"] = note.front
        ankiNote["Back"] = note.back
        ankiNote["url"] = note.url
        ankiNote["thumbnail"] = str(note.thumbnail)
        ankiNote["platformItemId"] = str(note.id)
        ankiNote["platformName"] = note.platform
        # ankiNote[# or, if were not using our own databa] = note.databa
        # ankiNote["platformId"] = note.platformId
        # ankiNote["filters"] = note.filters
        ankiNote["title"] = note.title
        # ankiNote["video_snippet"] = note.video_snippet
        # ankiNote["filters"] = note.filters

    # mm.add_field(model, mm.new_field("Timestamp"))
