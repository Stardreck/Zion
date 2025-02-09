import json
from pathlib import Path
from typing import Any


class StarConfig:
    def __init__(self, config_path: str):
        self._data = self.__load_config(config_path)

        self.width: int = self._data.get("width", 1600)
        self.height: int = self._data.get("height", 720)
        self.fps: int = self._data.get("fps", 60)
        self.title: str = self._data.get("title", "")
        self.main_menu_background_image: str = self._data.get("main_menu", {}).get("background_image", "")
        self.main_menu_start_button_text: str = self._data.get("main_menu", {}).get("start_button_text", "")
        self.event_probability: float = self._data.get("event_system", {}).get("event_probability", 0)

    def __load_config(self, config_path: str) -> dict[str, Any]:
        """
        Load and parse the JSON configuration file.
        """
        config_file = Path(config_path)
        if not config_file.is_file():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        with open(config_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def validate(self) -> None:
        """
        Validate the configuration values.
        """
        if not isinstance(self.width, int) or self.width <= 0:
            raise ValueError("Invalid width in configuration")
        if not isinstance(self.height, int) or self.height <= 0:
            raise ValueError("Invalid height in configuration")
        if not isinstance(self.fps, int) or self.fps <= 0:
            raise ValueError("Invalid FPS in configuration")
        if not isinstance(self.title, str) or len(self.title) <= 0:
            raise ValueError("Invalid title in configuration")
        if not Path(self.main_menu_background_image).is_file():
            raise ValueError(f"main_menu_background_image image not found: {self.main_menu_background_image}")
        if not isinstance(self.main_menu_start_button_text, str) or len(self.main_menu_start_button_text) <= 0:
            raise ValueError("Invalid main_menu_background_image in configuration")
        if not isinstance(self.event_probability, float) or self.event_probability == 0:
            raise ValueError("Invalid event_probability in configuration")
