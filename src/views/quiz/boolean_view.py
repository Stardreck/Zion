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


class BooleanView(View):
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
        self.true_button: UIButton | None = None
        self.false_button: UIButton | None = None
        self.panel: UIPanel | None = None
        self.title: UILabel | None = None

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
            relative_rect=Rect(0, 10, 530, 460),
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="default_panel"
        )

        # Create a title label
        self.title = UILabel(
            relative_rect=Rect(0, 0, 500, 50),
            manager=self.pygame_gui_ui_manager,
            text="Aufgabe",
            container=self.panel,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="quiz_title"
        )
        # Question label (displaying the quiz question)
        self.question = UITextBox(
            relative_rect=Rect(16.5, 50, 500, 150),
            manager=self.pygame_gui_ui_manager,
            html_text=self.quiz.question,
            container=self.panel,
            anchors={"left": "left"},
            object_id="quiz_question"
        )


        self.false_button = UIButton(
            relative_rect=Rect(15, 100, 225, 225),
            text="Nein",
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"centery": "centery", "left": "left"},
            object_id="quiz_boolean_false_button"
        )
        self.false_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self.submit(False))

        self.true_button = UIButton(
            relative_rect=Rect(-240, 100, 225, 225),
            text="Ja",
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"centery": "centery", "right": "right"},
            object_id="quiz_boolean_true_button"
        )
        self.true_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self.submit(True))

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

    def submit(self, user_answer: bool) -> None:
        """
        Process the user's input and delegate it to the quiz manager.
        """
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
        if self.true_button:
            self.true_button.kill()
        if self.false_button:
            self.false_button.kill()
