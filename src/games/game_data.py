import json
from pathlib import Path
from typing import List, Dict

from src.factories.event_factory import EventFactory
from src.factories.game_object_factory import GameObjectFactory
from src.factories.planet_factory import PlanetFactory
from src.factories.quiz_factory import QuizFactory
from src.factories.story_factory import StoryFactory
from src.models.event_card import EventCard
from src.models.game_object import GameObject
from src.models.planet import Planet
from src.models.quiz import Quiz
from src.models.story import Story
from src.star_config import StarConfig


class GameData:
    """
    this class stores all game data like events, planets and so on (located in data)
    the json data are mapped according to the corresponding models
    """

    def __init__(self, config: StarConfig, data_directory: str = "data"):
        self.planet_quizzes: Dict[str, List[Quiz]] = self.load_quizzes(Path(data_directory) / "quizzes.json")
        self.game_objects: List[GameObject] = self.load_game_objects(Path(data_directory) / "game_objects.json")
        self.story_segments: dict[str, Story] = self.load_stories(Path(data_directory) / "stories.json")
        self.event_cards: List[EventCard] = self.load_events(Path(data_directory) / "events.json")
        self.planets: List[Planet] = self.load_planets(Path(data_directory) / "planets.json")

    def load_quizzes(self, path: Path) -> Dict[str, List[Quiz]]:
        with open(path, "r", encoding="utf-8") as file:
            quizzes_data = json.load(file)
        quizzes: Dict[str, List[Quiz]] = {}
        for planet_name, quiz_list in quizzes_data.items():
            quizzes[planet_name] = [QuizFactory.create_quiz(quiz) for quiz in quiz_list]
        return quizzes

    def load_game_objects(self, path: Path) -> List[GameObject]:
        with open(path, "r", encoding="utf-8") as file:
            game_object_data = json.load(file)
        return [GameObjectFactory.create_game_object(object) for object in game_object_data]

    def load_stories(self, path: Path) -> dict[str, Story]:
        with open(path, "r", encoding="utf-8") as file:
            story_data = json.load(file)
        return {planet: StoryFactory.create_story(data) for planet, data in story_data.items()}

    def load_events(self, path: Path) -> List[EventCard]:
        with open(path, "r", encoding="utf-8") as file:
            event_data = json.load(file)
        return [EventFactory.create_event(event) for event in event_data]

    def load_planets(self, path: Path) -> List[Planet]:
        with open(path, "r", encoding="utf-8") as file:
            planet_data = json.load(file)
        return [PlanetFactory.create_planet(planet) for planet in planet_data]
