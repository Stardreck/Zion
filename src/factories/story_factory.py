from typing import Dict, Any, List

from src.factories.story_line_factory import StoryLineFactory
from src.models.story import Story
from src.models.story_line import StoryLine


class StoryFactory:
    @staticmethod
    def create_story(story_data: Dict[str, Any]) -> Story:
        story_lines_data = story_data.get("story_lines", [])
        story_lines: List[StoryLine] = []
        for story_line_data in story_lines_data:
            story_line = StoryLineFactory.create_story_line(story_line_data)
            story_lines.append(story_line)
        return Story(
            title=story_data.get("title", ""),
            story_lines=story_lines
        )
