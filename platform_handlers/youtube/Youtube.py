# 3. Specific Implementations
import json
import os
from typing import Tuple

import requests
from pydantic import BaseModel, Field, field_validator

from ...types.AnkiCard import AnkiCard
from ...types.AnkiCardModel import AnkiCardModel
from ...types.PlatformHandler import PlatformHandler
from ...types.Source import BaseSource
from ...types.SourceType import SourceType
from .sources.history import YoutubeHistorySource


class Youtube(PlatformHandler):
    sourceList: dict[SourceType, type[BaseSource]] = {
        SourceType.HISTORY: YoutubeHistorySource
    }

    def __init__(self, sources: list[SourceType] = []):
        self.sources: list[type[BaseSource]] = []
        for source in sources:
            if source not in self.sourceList:
                raise ValueError(f"Source {source} is not supported for YouTube.")
            self.sources.append(self.__class__.sourceList[source])

    def update(self):
        """
        Fetches all of the videos in a playlist specified in the config
        and updates the database accordingly.
        """

        # for each source, run the scrape method

        # list of items, e.g youtube vieos or tik tok shorts
        items: list[AnkiCardModel] = []

        for source_type, source_class in self.sourceList.items():
            items.extend(source_class(source_type).scrape())

        self.llm_process_items(items)

        # Here you would connect to your database and insert/update records
        # For demonstration, just print them:
        # for idx, title in enumerate(titles, start=1):
        # print(f"Video {idx}: {title}")
        # e.g. cursor.execute("INSERT INTO videos (title) VALUES (?)", (title,))

        # print(f"Updated database with {len(titles)} videos.")

    def llm_process_items(self, items: list[AnkiCardModel]) -> list[AnkiCard]:
        url = "https://api.deepseek.com/chat/completions"
        with open(
            "/home/owen/.local/share/Anki2/addons21/anki_memorize/prompt.txt",
            "r",
            encoding="utf-8",
        ) as f:
            system_prompt = f.read()

        API_KEY = "sk-7475c00d24be4652bf71434471a6aa77"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        examples_dir = "/home/owen/.local/share/Anki2/addons21/anki_memorize/platform_handlers/youtube/examples"
        for example_num in os.listdir(examples_dir):
            example_path = os.path.join(examples_dir, example_num)
            prompt_file = os.path.join(example_path, "prompt.txt")
            answer_file = os.path.join(example_path, "answer.txt")
            if os.path.isfile(prompt_file) and os.path.isfile(answer_file):
                with open(prompt_file, "r", encoding="utf-8") as pf:
                    prompt_text = pf.read()
                with open(answer_file, "r", encoding="utf-8") as af:
                    answer_text = af.read()
                messages.append({"role": "user", "content": prompt_text})
                messages.append({"role": "assistant", "content": answer_text})

        payload = {
            "model": "deepseek-reasoner",
            "thinking": {"type": "enabled"},
            "messages": messages,
            "response_format": {"type": "json_object"},
            "stream": False,
        }

        result: list[AnkiCard] = []
        breakpoint()
        for item in items:
            payload["messages"].append({"role": "user", "content": item.transcript})

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                # TODO: abstract this processing away and make it more generalized to support any api

                try:
                    data_str = response.json()["choices"][0]["message"]["content"]
                    raw_data = json.loads(data_str)

                    class Flashcard(BaseModel):
                        qfmt: str
                        afmt: str
                        markers: list[Tuple[str, str]]
                        score: int = Field(..., ge=1, le=10)

                        @field_validator("markers")
                        @classmethod
                        def check_markers(cls, v):
                            for start, end in v:
                                if not (":" in start and ":" in end):
                                    raise ValueError(
                                        f"Invalid time format: {start}, {end}"
                                    )
                            return v

                    class FlashcardsResponse(BaseModel):
                        flashcards: list[Flashcard]

                    data = FlashcardsResponse.model_validate(raw_data)
                    for card in data.flashcards:
                        front = card.qfmt
                        back = card.afmt
                        markers = card.markers
                        score = card.score
                        anki_card = AnkiCard(item, front, back, markers, score)
                        result.append(anki_card)

                except:
                    raise

            else:
                print(
                    f"Error processing card with title '{item.title}': {response.status_code} - {response.text}"
                )
            payload["messages"].pop()

        for card in result:
            print(card)

        return result
