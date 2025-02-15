from typing import List

from src.models.story_block import StoryBlock


class Story:
    def __init__(self, title: str, blocks: List[StoryBlock]):
        self.title: str = title
        self.blocks: List[StoryBlock] = blocks
