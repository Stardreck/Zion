from typing import Dict, Any, List

from src.factories.story_block_factory import StoryBlockFactory
from src.factories.story_line_factory import StoryLineFactory
from src.models.story import Story
from src.models.story_line import StoryLine


class StoryFactory:
    @staticmethod
    def create_story(story_data: Dict[str, Any]) -> Story:
        blocks_data = story_data.get("blocks", [])
        blocks = [StoryBlockFactory.create_story_block(block) for block in blocks_data]
        return Story(
            title=story_data.get("title", ""),
            blocks=blocks
        )
