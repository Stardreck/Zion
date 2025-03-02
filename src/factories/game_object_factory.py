from typing import Dict, Any

from src.models.game_object import GameObject


class GameObjectFactory:
    @staticmethod
    def create_game_object(game_object_data: Dict[str, Any]) -> GameObject:
        return GameObject(
            name=game_object_data["name"],
            alias=game_object_data["alias"],
            description=game_object_data["description"],
            location=game_object_data["location"],
            image_path=game_object_data.get("image_path", None),
            background_image=game_object_data.get("background_image", None)
        )
