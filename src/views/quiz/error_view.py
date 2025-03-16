from __future__ import annotations
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


class ErrorView(View):
    def __init__(self, game: StoryGame, quiz: Quiz):
        super().__init__(game.ui_manager.gui_manager)
        self.game = game
        self.quiz = quiz
        self.is_running: bool = True

        # Load a common background image (using the main menu background image)
        self.background_image = pygame.image.load("assets/images/spaceship/classroom/spaceship_classroom_01.png").convert()

        # title
        self.title_text = "Nachhilfeunterricht"

        # UI element placeholders


    def build_ui(self) -> None:

        title_rect = Rect(0, 60, 800, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text=self.title_text,
            manager=self.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="quiz_classroom_title",
        )

        # Create a centered transparent background panel
        self.panel_bg = UIPanel(
            relative_rect=Rect(540, 160, 500, 260),
            manager=self.pygame_gui_ui_manager,
            object_id="default_panel_transparent"
        )

        # Create the inner panel for quiz content
        self.panel = UIPanel(
            relative_rect=Rect(0, 10, 480, 180),
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="default_panel"
        )
        self.explanation = UITextBox(
            relative_rect=Rect(0,0, 470, 180),
            manager=self.pygame_gui_ui_manager,
            html_text=self.quiz.solution,
            container=self.panel,
            anchors={"left": "left"},
        )
        # Create a confirm button to submit the answer
        self.confirm_button = UIButton(
            relative_rect=Rect(0, -60, 480, 50),
            text="Weiter",
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="quiz_confirm_button"
        )

        self.confirm_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self.kill())


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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.kill()
                self.pygame_gui_ui_manager.process_events(event)
            self.pygame_gui_ui_manager.update(time_delta)
            self.game.window.blit(self.background_image, (0, 0))
            self.pygame_gui_ui_manager.draw_ui(self.game.window)
            pygame.display.update()
        self.kill()


    def kill(self) -> None:
        self.pygame_gui_ui_manager.set_focus_set(None)
        self.is_running = False
        if self.panel_bg:
            self.panel_bg.kill()
        if self.title:
            self.title.kill()
        if self.panel:
            self.panel.kill()
        if self.explanation:
            self.explanation.kill()
        if self.confirm_button:
            self.confirm_button.kill()