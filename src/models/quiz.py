from typing import List, Optional, Dict, Any

from src.factories.story_line_factory import StoryLineFactory
from src.models.story_line import StoryLine


class Quiz:
    """
    Model representing a quiz.

    Attributes:
        question: The quiz question text.
        answer_options: A list of possible answers.
        correct_answer: (Optional) The correct answer.
        quiz_type: The type of quiz (default: "quiz").
    """

    def __init__(self, question: str, answer_options: List[str],
                 correct_answer: Optional[str] = None, quiz_type: str = "quiz", solution: str = "", person: str = "", category: str = "", difficulty: str = "",
                 story_consequence: Dict[str, Any] | None = None):
        self.question = question
        self.answer_options = answer_options
        self.correct_answer = correct_answer
        self.quiz_type = quiz_type
        self.solution = solution
        self.person = person
        self.category = category
        self.difficulty = difficulty
        if story_consequence is not None:
            self.story_consequence = StoryLineFactory.create_story_line(story_consequence)
        else:
            self.story_consequence = None
