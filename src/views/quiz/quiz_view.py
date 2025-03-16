from __future__ import annotations
import pygame_gui
from pygame import Rect
from src.views.quiz.base_quiz_view import BaseQuizView


class QuizView(BaseQuizView):
    """
    QuizView displays a multiple-choice quiz.
    It inherits common UI elements from BaseQuizView and adds a multiple-choice answer list.
    """

    def build_specific_ui(self) -> None:
        """
        Build UI elements specific to a multiple-choice quiz.
        This includes displaying a list of answer options.
        """
        if self.quiz.answer_options:
            answers_html = "<br/>".join(
                [f"<b>{idx + 1})</b> {answer}<br/>" for idx, answer in enumerate(self.quiz.answer_options)]
            )
        else:
            answers_html = "No answers provided."
        # Create a UITextBox to display the answer options
        self.answer_list = pygame_gui.elements.UITextBox(
            relative_rect=Rect(16.5, 180, 600, 250),
            manager=self.pygame_gui_ui_manager,
            html_text=answers_html,
            container=self.panel,
            anchors={"left": "left", "top": "top"},
            object_id="quiz_answer_list"
        )
        self.title.set_text("Quiz-Frage")
        self.input_info_label.set_text("(1,2,3,4)")
