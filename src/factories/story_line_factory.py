from typing import Dict, Any
from src.models.story_line import StoryLine


class StoryLineFactory:
    @staticmethod
    def create_story_line(story_line_data: Dict[str, Any]) -> StoryLine:
        return StoryLine(
            text=story_line_data.get("text", ""),
            image_path=story_line_data.get("image", ""),
            image_description=story_line_data.get("image_description", ""),
        )
