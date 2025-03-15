from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import pygame_gui
from pygame import Rect
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_large_default_button import UILargeDefaultButton
from src.components.ui.ui_large_default_panel import UILargeDefaultPanel
from src.components.ui.ui_large_default_panel_transparent_bg import UILargeDefaultPanelTransparentBg
from src.components.ui.ui_large_header_title import UILargeHeaderTitle
from src.components.ui.ui_large_left_image import UILargeLeftImage
from src.components.ui.ui_large_left_image_description import UILargeLeftImageDescription
from src.components.ui.ui_large_right_text_box import UILargeRightTextBox
from src.components.ui.ui_panel import UIPanel
from src.components.ui.ui_text_box import UITextBox
from src.models.story_line import StoryLine
from src.views.view import View
from src.models.planet import Planet

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class StoryView(View):
    def __init__(self, game: StoryGame, planet: Planet, story_line: StoryLine):
        super().__init__(game.ui_manager.gui_manager)
        self.game = game
        self.planet = planet
        self.story_line: StoryLine = story_line
        self.title_text = self.planet.name
        self.is_running: bool = True
        self.selected_option: int = 0

        # Load the background image (from planet.background_image)
        self.background_image = pygame.image.load(self.planet.background_image).convert()

        # UI element placeholders
        self.title: UILabel | None = None
        self.panel_bg: UIPanel | None = None
        self.panel: UIPanel | None = None
        self.story_image = None
        self.story_description = None
        self.button1 = None
        self.continue_button = None

    def __build_ui(self):
        """Build the UI elements common to both menus."""
        # Create title label at the top
        self.title = UILargeHeaderTitle(self.pygame_gui_ui_manager, None, self.title_text)
        # title_rect = Rect(0, 60, 800, 100)
        # self.title = UILabel(
        #     relative_rect=title_rect,
        #    text=self.title_text,
        #    manager=self.pygame_gui_ui_manager,
        #    anchors={"centerx": "centerx", "top": "top"},
        #    object_id="planet_menu_title",
        # )

        # Create the background panel (transparent)
        self.panel_bg = UILargeDefaultPanelTransparentBg(self.pygame_gui_ui_manager)
        # self.panel_bg = UIPanel(
        ##     relative_rect=Rect(0, 50, 1000, 480),
        #    manager=self.pygame_gui_ui_manager,
        #    anchors={"center": "center"},
        #    object_id="default_panel_transparent",
        # )

        # Create the inner panel
        self.panel = UILargeDefaultPanel(self.pygame_gui_ui_manager, self.panel_bg)
        # self.panel = UIPanel(
        #    relative_rect=Rect(0, 10, 980, 400),
        #    manager=self.pygame_gui_ui_manager,
        #    container=self.panel_bg,
        #    anchors={"centerx": "centerx", "top": "top"},
        #    object_id="default_panel",
        # )

        # Load and display the planet image
        portrait_path = ""
        if len(self.story_line.image_path) > 0:
            portrait_path = self.story_line.image_path
        if len(self.story_line.image_description) > 0:
            if self.story_line.image_description.lower() == "milo":
                portrait_path = self.game.engine.config.portrait_milo
            elif self.story_line.image_description.lower() == "lyra":
                portrait_path = self.game.engine.config.portrait_lyra
            elif self.story_line.image_description.lower() == "agatha":
                portrait_path = self.game.engine.config.portrait_agatha
            elif self.story_line.image_description.lower() == "victor":
                portrait_path = self.game.engine.config.portrait_victor

        if len(portrait_path) > 0:
            image_surface = pygame.image.load(portrait_path).convert_alpha()
            self.story_image = UILargeLeftImage(self.pygame_gui_ui_manager, self.panel, image_surface)
        # self.story_image = pygame_gui.elements.UIImage(
        ##     relative_rect=Rect(20, 30, 240, 255),
        #    image_surface=image_surface,
        #    manager=self.pygame_gui_ui_manager,
        #    container=self.panel,
        #    anchors={"left": "left"},
        # )
        self.story_image_description = UILargeLeftImageDescription(self.pygame_gui_ui_manager, self.panel,
                                                                   self.story_line.image_description)
        ##self.story_image_description = UILabel(
        #   relative_rect=Rect(75, 260, 100, 100),
        #   manager=self.pygame_gui_ui_manager,
        #    text=self.story_line.image_description,
        #    container=self.panel,
        #    anchors={"left": "left"},
        # )
        # Create the story text box
        self.story_description = UILargeRightTextBox(self.pygame_gui_ui_manager, self.panel, self.story_line.text)
        # self.story_description = UITextBox(
        #     relative_rect=Rect(260, 20, 700, 320),
        #    html_text=self.story_line.text,
        #    manager=self.pygame_gui_ui_manager,
        #    container=self.panel,
        #    anchors={"left": "left"},
        # )

        # Create the continue button
        self.continue_button = UILargeDefaultButton(self.pygame_gui_ui_manager, self.panel_bg)
        self.continue_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self._set_option(2))

        # continue_button_rect = Rect(0, -60, 500, 50)
        #
        #     self.continue_button = UIButton(
        #      relative_rect=continue_button_rect,
        #      text="weiter",
        #      manager=self.pygame_gui_ui_manager,
        #      container=self.panel_bg,
        #      anchors={"centerx": "centerx", "bottom": "bottom"},
        #     object_id="panel_button",
        #  )
        self.continue_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self._set_option(2))

    def _set_option(self, option: int):
        """Set the selected option and exit the menu."""
        self.selected_option = option
        self.kill()

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
        if self.story_image:
            self.story_image.kill()
        if self.story_description:
            self.story_description.kill()
        if self.button1:
            self.button1.kill()
        if self.continue_button:
            self.continue_button.kill()
