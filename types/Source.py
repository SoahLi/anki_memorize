# Represents a social media outlet
import json
from abc import ABC, abstractmethod


class Outlet(ABC):
    def __init__(self, name: str):
        name = name.lower()
        file_path = f"./outles/{name}.json"
        try:
            with open(file_path, "r") as f:
                build_data = json.load(f)
        except FileNotFoundError:
            raise ValueError(
                f"Outlet '{name}' not found. Please check the name and try again."
            )

        # I would like to have bear type validate the properties of data
        self.get_required_packages(build_data["packages"])

    @abstractmethod
    def get_required_packages(self, packages: list[str]):
        pass
