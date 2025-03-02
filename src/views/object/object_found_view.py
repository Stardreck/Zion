from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
import pygame_gui
from pygame import Rect

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.models.game_object import GameObject
from src.models.planet import Planet
from src.views.view import View

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class ObjectFoundView(View):
    def __init__(self, game: StoryGame, planet: Planet):
        super().__init__(game.ui_manager.gui_manager)
        self.game = game
        self.planet = planet
        self.is_running: bool = True

        # get the obtainable object for this planet
        self.object: GameObject = next(
            (game_object for game_object in self.game.data.game_objects if
             game_object.location.lower() == planet.name.lower()), None)

        # get the object image
        self.object_image_surface = pygame.image.load(self.object.image_path).convert_alpha()

        # Load the background image (default from planet.background_image) override from object
        background_image_path = self.planet.background_image
        if self.object.background_image is not None:
            background_image_path = self.object.background_image
        self.background_image_surface = pygame.image.load(background_image_path).convert()

        self.title_text = f"{self.object.name} erhalten!"



        # UI element placeholders
        self.title: UILabel | None = None
        self.panel_bg: UIPanel | None = None
        self.panel: UIPanel | None = None
        self.story_image = None
        self.planet_description = None
        self.button1 = None
        self.continue_button = None

    def __build_ui(self):
        """Build the UI elements """
        # Create title label at the top
        title_rect = Rect(0, 60, 800, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text=self.planet.name,
            manager=self.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="planet_menu_title",
        )

        # Create a centered transparent background panel
        self.panel_bg = UIPanel(
            relative_rect=Rect(0, 50, 550, 480),
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
            text=self.title_text,
            container=self.panel,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="quiz_title"
        )

        self.object_image = pygame_gui.elements.UIImage(
            relative_rect=Rect(0, 0, 350, 350),
            image_surface=self.object_image_surface,
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"center": "center"},
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
        self.confirm_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self.kill())



    def run(self) -> int:
        """Display the menu and return the selected option."""
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
            self.game.window.blit(self.background_image_surface, (0, 0))
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
        if self.story_image:
            self.story_image.kill()
        if self.planet_description:
            self.planet_description.kill()
        if self.button1:
            self.button1.kill()
        if self.continue_button:
            self.continue_button.kill()
