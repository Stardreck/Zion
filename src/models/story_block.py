from typing import List, Optional

from src.models.StoryOption import StoryOption
from src.models.final_decision import FinalDecision
from src.models.story_decision import StoryDecision
from src.models.story_line import StoryLine
from src.models.quiz import Quiz


class StoryBlock:
    def __init__(self, block_type: str,
                 story_lines: Optional[List[StoryLine]] = None,
                 quiz: Optional[Quiz] = None, decision: Optional[FinalDecision] = None,
                 story_decision: Optional[StoryDecision] = None,
                 story_option: Optional[StoryOption] = None):
        """
        :param block_type: "story", "quiz" oder "task"
        :param story_lines: Liste of StoryLine-Objects (with type "story")
        :param quiz: A Quiz-Object (with type "quiz" or "task")
        """
        self.block_type = block_type
        self.story_lines = story_lines or []
        self.quiz = quiz
        self.decision = decision
        self.story_decision = story_decision,
        self.story_option = story_option
