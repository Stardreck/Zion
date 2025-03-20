from typing import Dict, Any

from src.models.final_decision import FinalDecision
from src.models.story_decision import StoryDecision


class StoryDecisionFactory:
    @staticmethod
    def create_story_decision(decision_data: Dict[str, Any]) -> StoryDecision:
        blocks_data = decision_data.get("blocks", [])
        return StoryDecision()
