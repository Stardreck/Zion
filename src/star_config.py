import json
from pathlib import Path
from typing import Any, List


class StarConfig:
    """
    This is the main configuration file (star_config.json in data)
    """

    def __init__(self, config_path: str):
        self._data = self.__load_config(config_path)

        self.title: str = self._data.get("title", "")

        ##### engine settings #####
        self.width: int = self._data.get("engine", {}).get("width", 1600)
        self.height: int = self._data.get("engine", {}).get("height", 720)
        self.fps: int = self._data.get("engine", {}).get("fps", 60)
        self.full_screen: bool = self._data.get("engine", {}).get("full_screen", False)
        self.system_check_backgrounds: List[str] = self._data.get("engine", {}).get("system_check_backgrounds", [])


        ##### main menu #####
        self.main_menu_background_image: str = self._data.get("main_menu", {}).get("background_image", "")
        self.main_menu_start_button_text: str = self._data.get("main_menu", {}).get("start_button_text", "")

        ##### game settings #####
        self.game_settings_start_fuel: int = self._data.get("game_settings", {}).get("start_fuel", 0)
        self.game_settings_start_hull: int = self._data.get("game_settings", {}).get("start_hull", 0)
        self.game_settings_default_backgrounds: [] = self._data.get("game_settings", {}).get("default_backgrounds", [])
        self.game_settings_wormhole_cost: int = self._data.get("game_settings", {}).get("wormhole_cost", 10)

        ##### portraits #####
        self.portrait_milo = self._data.get("portraits", {}).get("milo", 0)
        self.portrait_lyra = self._data.get("portraits", {}).get("lyra", 0)
        self.portrait_agatha = self._data.get("portraits", {}).get("agatha", 0)
        self.portrait_victor = self._data.get("portraits", {}).get("victor", 0)

        ##### player settings #####
        self.player_settings_start_row: int = self._data.get("player_settings", {}).get("player_start_row", 0)
        self.player_settings_start_col: int = self._data.get("player_settings", {}).get("player_start_col", 0)

        ##### planet menu #####
        self.planet_menu_fuel_station_background_image_paths: List[str] = self._data.get("planet_menu", {}).get("fuel_station",                                                                                                         {}).get(
            "backgrounds", [])
        self.planet_menu_fuel_station_image_path: str = self._data.get("planet_menu", {}).get("fuel_station", {}).get(
            "image", "")
        self.planet_menu_fuel_free_amount: int = self._data.get("planet_menu", {}).get("fuel_station", {}).get(
            "fuel_free_amount", 0)
        self.planet_menu_fuel_quiz_correct_amount: int = self._data.get("planet_menu", {}).get("fuel_station", {}).get(
            "fuel_quiz_correct_amount", 0)
        self.planet_menu_fuel_quiz_wrong_amount: int = self._data.get("planet_menu", {}).get("fuel_station", {}).get(
            "fuel_quiz_wrong_amount", 0)
        self.planet_menu_states_zion_not_allowed_text: str = self._data.get("planet_menu", {}).get("states",{}).get(
            "zion_not_allowed", "")
        self.planet_menu_visited: str = self._data.get("planet_menu", {}).get("states",{}).get(
            "visited", "")

        ##### event system #####
        self.event_probability: float = self._data.get("event_system", {}).get("event_probability", 0)
        self.event_base_positive_probability: float = self._data.get("event_system", {}).get(
            "base_positive_probability", 0)
        self.event_max_error_count: float = self._data.get("event_system", {}).get("max_error_count", 0)
        self.change_probability_by: float = self._data.get("event_system", {}).get("change_probability_by", 0)
        self.event_panel_background_path: str = self._data.get("event_system", {}).get("panel_background", "")
        self.event_panel_background_path: str = self._data.get("event_system", {}).get("panel_background", "")

        ##### mini-game system #####
        self.mini_game_probability: float = self._data.get("mini_game_system", {}).get("mini_game_probability", 0)
        self.mini_game_menu_backgrounds: List[str] = self._data.get("mini_game_system", {}).get("menu_backgrounds", [])

        ##### quiz system #####
        self.quiz_tolerance: float = self._data.get("quiz_system", {}).get("tolerance", 0)
        self.quiz_tolerance: float = self._data.get("quiz_system", {}).get("tolerance", 0)
        self.quiz_backgrounds: [] = self._data.get("quiz_system", {}).get("backgrounds", [])

        ##### inventory system #####
        self.inventory_background_paths: List[str] = self._data.get("inventory_system", {}).get("backgrounds", [])
        self.inventory_panel_background_path: str = self._data.get("inventory_system", {}).get("panel_background", "")
        self.inventory_empty_slot_path: str = self._data.get("inventory_system", {}).get("empty_slot", "")

        ##### game-over system #####
        self.game_over_story_quiz_max_attempts: int = self._data.get("game_over_system", {}).get(
            "story_quiz_max_attempts", 5)
        self.game_over_fuel_background_path: str = self._data.get("game_over_system", {}).get(
            "game_over_fuel_background", "")
        self.game_over_hull_background_path: str = self._data.get("game_over_system", {}).get(
            "game_over_hull_background", "")
        self.game_over_default_background_paths: List[str] = self._data.get("game_over_system", {}).get(
            "game_over_default_backgrounds", [])
        self.game_over_reject_background_paths: List[str] = self._data.get("game_over_system", {}).get(
            "game_over_reject_backgrounds", [])
        self.game_over_terraform_backgrounds_paths: List[str] = self._data.get("game_over_system", {}).get(
            "game_over_terraform_backgrounds", [])

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
