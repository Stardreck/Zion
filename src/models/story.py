from typing import List, Optional

from src.models.story_line import StoryLine


class Story:
    def __init__(self, title: str, story_lines: List[StoryLine]):
        self.title: str = title
        self.story_lines: List[StoryLine] = story_lines
