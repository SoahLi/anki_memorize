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
from ...util.config import config_get_source_types_for_platform
from .sources.history import YoutubeHistorySource

SourceList = dict[SourceType, type[BaseSource]]


class Youtube(PlatformHandler):
    sourceList: SourceList = {SourceType.HISTORY: YoutubeHistorySource}

    def __init__(self):
        super().__init__("youtube")
        # breakpoint()
        requested_sources = config_get_source_types_for_platform(self.name)
        self.sources: SourceList = {}
        for source in requested_sources or []:
            if source not in self.sourceList:
                raise ValueError(f"Source {source} is not supported for YouTube.")
            # Append the key and value to self.sources
            self.sources[source] = self.__class__.sourceList[source]

    def update(self):
        """
        1. For each source type, run the scrape method to get a list of items (e.g. YouTube videos or TikTok shorts).
        2. For each item, send the transcript to the LLM and get back a set of flash cards
        """

        items: list[AnkiCardModel] = []

        for source_type, source_class in self.sources.items():
            # breakpoint()
            items.extend(source_class(source_type).scrape())

        self.llm_process_items(items)

    def llm_process_items(self, items: list[AnkiCardModel]) -> list[AnkiCard]:
        url = "https://api.deepseek.com/chat/completions"
        
        # Get the add-on root directory dynamically
        addon_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        prompt_path = os.path.join(addon_dir, "prompt.txt")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()

        # TODO: make this a config variable
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

        # Get examples directory relative to this file
        examples_to_inject_dir = os.path.join(
            os.path.dirname(__file__), "examples"
        )
        for i in os.listdir(examples_to_inject_dir):
            # breakpoint()
            example_number_path = os.path.join(examples_to_inject_dir, i)
            prompt_file = os.path.join(example_number_path, "prompt.txt")
            answer_file = os.path.join(example_number_path, "answer.txt")

            if os.path.isfile(prompt_file) and os.path.isfile(answer_file):
                with open(prompt_file, "r", encoding="utf-8") as pf:
                    prompt_text = pf.read()
                with open(answer_file, "r", encoding="utf-8") as af:
                    answer_text = af.read()
                messages.append({"role": "user", "content": prompt_text})
                messages.append({"role": "assistant", "content": answer_text})

        # TODO: abstract this processing away and make it more generalized to support any api
        # TODO: make this async. In fact, make all different platforms async
        payload = {
            "model": "deepseek-reasoner",
            "thinking": {"type": "enabled"},
            "messages": messages,
            "response_format": {"type": "json_object"},
            "stream": False,
        }

        result: list[AnkiCard] = []
        for item in items:
            payload["messages"].append({"role": "user", "content": item.transcript})

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                # TODO: abstract this processing away and make it more generalized to support any api
                # TODO: make this async. In fact, make all different platforms async

                try:
                    # breakpoint()
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
                    raise RuntimeError(
                        f"Error processing response for card with title '{item.title}': {response.text}"
                    )

            else:
                print(
                    f"Error processing card with title '{item.title}': {response.status_code} - {response.text}"
                )
            payload["messages"].pop()

        for card in result:
            print(card)

        return result
