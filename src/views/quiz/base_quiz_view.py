from __future__ import annotations

import random

import pygame
import pygame_gui
from pygame import Rect

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.components.ui.ui_text_box import UITextBox
from src.components.ui.ui_text_entry_line import UITextEntryLine
from src.views.view import View
from src.models.quiz import Quiz
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class BaseQuizView(View):
    """
    BaseQuizView provides the common UI for both multiple choice quizzes and tasks
    """

    def __init__(self, game: StoryGame, quiz: Quiz):
        super().__init__(game.ui_manager.gui_manager)
        self.game = game
        self.quiz = quiz
        self.is_running: bool = True

        # Load a background image
        backgrounds = self.game.engine.config.quiz_backgrounds
        chosen_image: str = random.choice(backgrounds)
        self.background_image = pygame.image.load(chosen_image).convert()

        # UI element placeholders
        self.panel_bg: UIPanel | None = None
        self.panel: UIPanel | None = None
        self.title: UILabel | None = None
        self.input_label: UILabel | None = None
        self.input_info_label: UILabel | None = None
        self.input_field: UITextEntryLine | None = None
        self.confirm_button: UIButton | None = None

    def build_ui(self) -> None:
        """
        Build the common UI elements.
        """
        # Create a centered transparent background panel
        self.panel_bg = UIPanel(
            relative_rect=Rect(0, 0, 550, 480),
            manager=self.pygame_gui_ui_manager,
            anchors={"center": "center"},
            object_id="default_panel_transparent"
        )

        # Create the inner panel for quiz content
        self.panel = UIPanel(
            relative_rect=Rect(0, 10, 530, 400),
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="default_panel"
        )

        # Create a title label
        self.title = UILabel(
            relative_rect=Rect(0, 0, 500, 50),
            manager=self.pygame_gui_ui_manager,
            text="",
            container=self.panel,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="quiz_title"
        )
        # Question label (displaying the quiz question)
        self.question = UITextBox(
            relative_rect=Rect(16.5, 50, 500, 80),
            manager=self.pygame_gui_ui_manager,
            html_text=self.quiz.question,
            container=self.panel,
            anchors={"left": "left", "top": "top"},
            object_id="quiz_question"
        )

        # Create input label for answer entry
        self.input_label = UILabel(
            relative_rect=Rect(16.5, -60, 150, 50),
            manager=self.pygame_gui_ui_manager,
            text="Antwort eingeben:",
            container=self.panel,
            anchors={"left": "left", "bottom": "bottom"},
            object_id="quiz_input_label"
        )
        # helper text
        self.input_info_label = UILabel(
            relative_rect=Rect(16.5, -40, 150, 50),
            manager=self.pygame_gui_ui_manager,
            text="",
            container=self.panel,
            anchors={"left": "left", "bottom": "bottom"},
            object_id="quiz_input_label_info"
        )

        # Create an input field for the user to enter their answer
        self.input_field = UITextEntryLine(
            relative_rect=Rect(16.5 + 150, -60, 350, 50),
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"left": "left", "bottom": "bottom"},
            object_id="quiz_input_field"
        )

        # Create a confirm button to submit the answer
        self.confirm_button = UIButton(
            relative_rect=Rect(0, -60, 500, 50),
            text="Bestätigen",
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="quiz_confirm_button"
        )
        self.confirm_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self.submit())



        # Call method for additional UI elements (specific to quiz vs. task)
        self.build_specific_ui()

    def build_specific_ui(self) -> None:
        """
        Build UI elements that are specific to the quiz type
        must be derived from children
        """
        print("[Error] build_specific_ui not implemented")
        pass

    def run(self) -> None:
        """
        Display the view in its own game loop until the user confirms their answer.
        """
        self.build_ui()
        clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            time_delta = clock.tick(self.game.engine.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    self.is_running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.game.debug_manager.toggle_debug_mode()
                self.pygame_gui_ui_manager.process_events(event)
            self.pygame_gui_ui_manager.update(time_delta)
            self.game.window.blit(self.background_image, (0, 0))
            self.pygame_gui_ui_manager.draw_ui(self.game.window)
            pygame.display.update()
        self.kill()

    def submit(self) -> None:
        """
        Process the user's input and delegate it to the quiz manager.
        """
        user_answer = self.input_field.get_text().strip()
        if not user_answer:
            return
        self.game.quiz_manager.process_submit(self.quiz, user_answer)
        self.pygame_gui_ui_manager.set_focus_set(None)
        self.is_running = False

    def kill(self) -> None:
        """
        Clean up and remove all UI elements.
        """
        self.is_running = False
        if self.panel:
            self.panel.kill()
        if self.panel_bg:
            self.panel_bg.kill()
        if self.title:
            self.title.kill()
        if self.input_label:
            self.input_label.kill()
        if self.input_info_label:
            self.input_info_label.kill()
        if self.input_field:
            self.input_field.kill()
        if self.confirm_button:
            self.confirm_button.kill()
