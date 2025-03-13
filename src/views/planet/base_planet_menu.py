from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import pygame
import pygame_gui
from pygame import Rect
from pygame_gui.elements import UIImage

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.components.ui.ui_text_box import UITextBox
from src.views.view import View
from src.models.planet import Planet

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class BasePlanetMenu(View):
    """
    Base class for planet-related menus.

    Parameters:
      - game: The StoryGame instance.
      - planet: The Planet to display.
      - title_text: The title text to display (can be the planet name or a custom title).
      - button_texts: A tuple with the texts for the two buttons.
    """

    def __init__(self, game: StoryGame, planet: Planet, title_text: str, button_texts: Tuple[str, str]):
        super().__init__(game.ui_manager.gui_manager)
        self.game = game
        self.planet = planet
        self.title_text = title_text
        self.button_texts = button_texts
        self.is_running: bool = True
        self.selected_option: int = 0

        # Load the background image (from planet.background_image)
        self.background_image = pygame.image.load(self.planet.background_image).convert()

        ##### UI elements #####
        self.title: UILabel | None = None
        self.panel_bg: UIPanel | None = None
        self.panel: UIPanel | None = None
        self.planet_image: UIImage | None = None
        self.planet_description = None
        self.button1: UIButton | None = None
        self.button2: UIButton | None = None
        self.show_button_1 = True
        self.show_button_2 = True

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
            relative_rect=Rect(0, 10, 530, 333),
            manager=self.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="default_panel",
        )

        # Load and display the planet image
        image_surface = pygame.image.load(self.planet.planet_image).convert()
        self.planet_image = pygame_gui.elements.UIImage(
            relative_rect=Rect(20, 30, 240, 240),
            image_surface=image_surface,
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"left": "left"},
        )

        # Create the planet description text box
        self.planet_description = UITextBox(
            relative_rect=Rect(260, 20, 250, 255),
            html_text=self.planet.description,
            manager=self.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"left": "left"},
        )

        if self.show_button_1:
            # Create the first button
            button1_rect = Rect(0, -125, 500, 50)
            self.button1 = UIButton(
                relative_rect=button1_rect,
                text=self.button_texts[0],
                manager=self.pygame_gui_ui_manager,
                container=self.panel_bg,
                anchors={"centerx": "centerx", "bottom": "bottom"},
                object_id="panel_button",
            )
            self.button1.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self._set_option(1))

        if self.show_button_2:
            # Create the second button
            button2_rect = Rect(0, -60, 500, 50)
            self.button2 = UIButton(
                relative_rect=button2_rect,
                text=self.button_texts[1],
                manager=self.pygame_gui_ui_manager,
                container=self.panel_bg,
                anchors={"centerx": "centerx", "bottom": "bottom"},
                object_id="panel_button",
            )
            self.button2.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self._set_option(2))

    def _set_option(self, option: int):
        """Set the selected option and exit the menu."""
        self.selected_option = option
        self.kill()

    def run(self) -> int:
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
                self.pygame_gui_ui_manager.process_events(event)
            self.pygame_gui_ui_manager.update(time_delta)
            # Draw the background image covering the window
            self.game.window.blit(self.background_image, (0, 0))
            self.pygame_gui_ui_manager.draw_ui(self.game.window)
            pygame.display.update()
        self.kill()
        return self.selected_option

    def kill(self):
        """Clean up all UI elements."""
        self.is_running = False
        if self.title:
            self.title.kill()
        if self.panel:
            self.panel.kill()
        if self.panel_bg:
            self.panel_bg.kill()
        if self.planet_image:
            self.planet_image.kill()
        if self.planet_description:
            self.planet_description.kill()
        if self.button1:
            self.button1.kill()
        if self.button2:
            self.button2.kill()
