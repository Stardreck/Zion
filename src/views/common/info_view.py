from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import pygame_gui
from pygame import Rect, Surface
from pygame_gui.elements import UIImage

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.components.ui.ui_text_box import UITextBox
from src.views.view import View

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class InfoView(View):
    def __init__(self, game: StoryGame, title: str, image: str, background_image: str, description: str,
                 confirm_text: str = "Weiter"):
        super().__init__(game.ui_manager.gui_manager)
        self.game: StoryGame = game
        self.is_running: bool = True

        ##### content #####
        self.title_text = title
        self.image_path: str = image
        self.background_image_path: str = background_image
        self.description_text: str = description
        self.confirm_button_text: str = confirm_text

        ##### UI elements #####
        self.background_image: Surface | None = None
        self.title: UILabel | None = None
        self.panel_bg: UIPanel | None = None
        self.panel: UIPanel | None = None
        self.image: UIImage | None = None
        self.description: UITextBox | None = None
        self.confirm_button: UIButton | None = None

    def __build_ui(self):
        # Load the background image
        self.background_image = pygame.image.load(self.background_image_path).convert()
        # Create title label at the top
        title_rect = Rect(0, 60, 800, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text=self.title_text,
            manager=self.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="common_info_view_title",
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
        image_surface = pygame.image.load(self.image_path)
        self.image = UIImage(
            relative_rect=Rect(20, 30, 240, 255),
            image_surface=image_surface,
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"left": "left"},
        )
        self.description = UITextBox(
            relative_rect=Rect(260, 20, 250, 255),
            html_text=self.description_text,
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"left": "left"})
        confirm_button_rect = Rect(0, -60, 500, 50)

        self.confirm_button = UIButton(
            relative_rect=confirm_button_rect,
            text=self.confirm_button_text,
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="panel_button",
        )
        self.confirm_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.kill())

    def run(self):
        """Display the menu modally and return the selected option."""
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
                    if event.key == pygame.K_RETURN:
                        self.kill()
                self.pygame_gui_ui_manager.process_events(event)
            self.pygame_gui_ui_manager.update(time_delta)
            # Draw the background image covering the window
            self.game.window.blit(self.background_image, (0, 0))
            self.pygame_gui_ui_manager.draw_ui(self.game.window)
            pygame.display.update()
        self.kill()

    def kill(self):
        self.is_running = False
        if self.title:
            self.title.kill()
        if self.panel_bg:
            self.panel_bg.kill()
        if self.panel:
            self.panel.kill()
        if self.image:
            self.image.kill()
        if self.description:
            self.description.kill()
        if self.confirm_button:
            self.confirm_button.kill()
