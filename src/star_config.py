import json
from pathlib import Path
from typing import Any, List


class StarConfig:
    def __init__(self, config_path: str):
        self._data = self.__load_config(config_path)

        self.width: int = self._data.get("width", 1600)
        self.height: int = self._data.get("height", 720)
        self.fps: int = self._data.get("fps", 60)
        self.title: str = self._data.get("title", "")

        ##### main menu #####
        self.main_menu_background_image: str = self._data.get("main_menu", {}).get("background_image", "")
        self.main_menu_start_button_text: str = self._data.get("main_menu", {}).get("start_button_text", "")

        ##### planet menu #####
        self.planet_menu_fuel_station_background_image_path: str = self._data.get("planet_menu", {}).get("fuel_station", {}).get("background", "")
        self.planet_menu_fuel_station_image_path: str = self._data.get("planet_menu", {}).get("fuel_station", {}).get("image", "")
        self.planet_menu_fuel_free_amount: int = self._data.get("planet_menu", {}).get("fuel_station", {}).get("fuel_free_amount", 0)
        self.planet_menu_fuel_quiz_correct_amount: int = self._data.get("planet_menu", {}).get("fuel_station", {}).get("fuel_quiz_correct_amount", 0)
        self.planet_menu_fuel_quiz_wrong_amount: int = self._data.get("planet_menu", {}).get("fuel_station", {}).get("fuel_quiz_wrong_amount", 0)

        ##### event system #####
        self.event_probability: float = self._data.get("event_system", {}).get("event_probability", 0)
        self.event_base_positive_probability: float = self._data.get("event_system", {}).get("base_positive_probability", 0)
        self.event_max_error_count: float = self._data.get("event_system", {}).get("max_error_count", 0)
        self.change_probability_by: float = self._data.get("event_system", {}).get("change_probability_by", 0)
        self.event_panel_background_path: str = self._data.get("event_system", {}).get("panel_background", "")
        self.event_panel_background_path: str = self._data.get("event_system", {}).get("panel_background", "")

        ##### quiz system #####
        self.quiz_tolerance: float = self._data.get("quiz_system", {}).get("tolerance", 0)
        self.quiz_tolerance: float = self._data.get("quiz_system", {}).get("tolerance", 0)

        ##### inventory system #####
        self.inventory_background_paths: List[str] = self._data.get("inventory_system", {}).get("backgrounds", [])
        self.inventory_panel_background_path: str = self._data.get("inventory_system", {}).get("panel_background", "")
        self.inventory_empty_slot_path: str = self._data.get("inventory_system", {}).get("empty_slot", "")

        ##### game-over system #####
        self.game_over_story_quiz_max_attempts: int = self._data.get("game_over_system", {}).get("story_quiz_max_attempts", 5)





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
