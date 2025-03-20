from typing import Dict, Any

from src.models.StoryOption import StoryOption
from src.models.final_decision import FinalDecision


class StoryOptionFactory:
    @staticmethod
    def create_story_option_factory(data: Dict[str, Any]) -> StoryOption:
        option = data.get("option", [])
        return StoryOption(option)
