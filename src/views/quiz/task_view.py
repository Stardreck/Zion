from __future__ import annotations
from src.views.quiz.base_quiz_view import BaseQuizView
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.story_game import StoryGame

class TaskView(BaseQuizView):
    """
    TaskView displays a task where the user must input a numerical answer.
    It is similar to QuizView but does not display any multiple-choice answer options.
    """
    def build_specific_ui(self) -> None:
        """
        For task-type quizzes, no additional UI elements are required.
        """
        self.title.set_text("Aufgabe")
        self.input_info_label.set_text("(Ohne Einheiten)")
