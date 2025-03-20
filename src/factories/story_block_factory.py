from typing import Dict, Any

from src.factories.final_decision_factory import FinalDecisionFactory
from src.factories.story_decision_factory import StoryDecisionFactory
from src.factories.story_option_factory import StoryOptionFactory
from src.models.StoryOption import StoryOption
from src.models.story_block import StoryBlock
from src.factories.story_line_factory import StoryLineFactory
from src.factories.quiz_factory import QuizFactory


class StoryBlockFactory:
    @staticmethod
    def create_story_block(block_data: Dict[str, Any]) -> StoryBlock | None:
        block_type = block_data.get("type")
        if block_type == "story":
            story_lines_data = block_data.get("story_lines", [])
            story_lines = [StoryLineFactory.create_story_line(sl) for sl in story_lines_data]
            return StoryBlock(block_type="story", story_lines=story_lines)
        elif block_type in ["quiz", "task", "boolean"]:
            quiz = QuizFactory.create_quiz(block_data)
            # set the quiz tipe Quiz-Typ
            quiz.quiz_type = block_type
            return StoryBlock(block_type=block_type, quiz=quiz)
        if block_type == "final_decision":
            decision = FinalDecisionFactory.create_final_decision(block_data)
            return StoryBlock(block_type=block_type, decision=decision)
        if block_type == "story_decision":
            story_decision = StoryDecisionFactory.create_story_decision(block_data)
            return StoryBlock(block_type=block_type, story_decision=story_decision)
        if block_type == "story_option":
            story_lines_data = block_data.get("story_lines", [])
            story_lines = [StoryLineFactory.create_story_line(sl) for sl in story_lines_data]
            story_option = StoryOptionFactory.create_story_option_factory(block_data)
            return StoryBlock(block_type=block_type, story_lines=story_lines, story_option=story_option)
        else:
            raise ValueError(f"Unknown Block-Type: {block_type}")
