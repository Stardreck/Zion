from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import pygame
import pygame_gui
from pygame import Rect, Surface
from pygame_gui.elements import UIImage

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.components.ui.ui_text_box import UITextBox
from src.views.view import View
from src.models.planet import Planet

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class BaseMiniGameMenu(View):
    def __init__(self, game: StoryGame, background_path: str, title_text: str, description_text: str, button_text: str):
        super().__init__(game.ui_manager.gui_manager)
        self.game: StoryGame = game

        # Load the background image (from star_config mini_game_system)
        self.background_image: Surface = pygame.image.load(background_path).convert()

        self.title_text: str = title_text
        self.description_text: str = description_text
        self.button_text: str = button_text

    def __build_ui(self):
        """Build the common UI elements"""
        # Create title label at the top
        title_rect = Rect(0, 60, 800, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text=self.title_text,
            manager=self.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="planet_menu_title",
        )

        # Create the background panel (transparent)
        self.panel_bg = UIPanel(
            relative_rect=Rect(0, 50, 550, 480),
            manager=self.pygame_gui_ui_manager,
            anchors={"center": "center"},
            object_id="default_panel_transparent",
        )

        # Create the inner panel
        self.panel = UIPanel(
            relative_rect=Rect(0, 10, 530, 400),
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="default_panel",
        )
        # Create the mini-game description text box
        self.description = UITextBox(
            relative_rect=Rect(260, 20, 250, 255),
            html_text=self.description_text,
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"left": "left"},
        )

        # Create a confirm button to submit the answer
        self.confirm_button = UIButton(
            relative_rect=Rect(0, -60, 500, 50),
            text=self.button_text,
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="quiz_confirm_button"
        )
        self.confirm_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self.kill())

    def run(self):
        self.__build_ui()
        clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            time_delta = clock.tick(self.game.engine.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.game.debug_manager.toggle_debug_mode()
                self.pygame_gui_ui_manager.process_events(event)
            self.pygame_gui_ui_manager.update(time_delta)
            # Draw the background image covering the window
            self.game.window.blit(self.background_image, (0, 0))
            self.pygame_gui_ui_manager.draw_ui(self.game.window)
            pygame.display.update()
        self.kill()

    def kill(self):
        """Clean up all UI elements."""
        self.is_running = False
        if self.title:
            self.title.kill()
        if self.panel:
            self.panel.kill()
        if self.panel_bg:
            self.panel_bg.kill()
        if self.description:
            self.description.kill()
