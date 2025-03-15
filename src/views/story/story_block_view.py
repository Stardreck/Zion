from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import pygame_gui
from pygame import Rect
from pygame_gui.elements import UIImage

from src.components.ui.ui_button import UIButton
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
from src.models.story import Story
from src.models.story_block import StoryBlock
from src.models.story_line import StoryLine
from src.views.view import View
from src.models.planet import Planet

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class StoryBlockView(View):
    def __init__(self, game: StoryGame, planet: Planet, story_block: StoryBlock):
        super().__init__(game.ui_manager.gui_manager)
        self.game = game
        self.planet = planet
        self.story_block: StoryBlock = story_block
        self.active_story_line: StoryLine | None = None
        self.active_story_line_index: int = 0
        self.title_text = self.planet.name
        self.is_running: bool = True

        # Load the background image (from planet.background_image)
        self.background_image = pygame.image.load(self.planet.background_image).convert()

        # UI element placeholders
        self.title: UILabel | None = None
        self.panel_bg: UIPanel | None = None
        self.panel: UIPanel | None = None
        self.story_image = None
        self.story_image_description = None
        self.story_description = None

        self.button1 = None
        self.continue_button = None

    def __build_ui(self):
        # title
        self.title = UILargeHeaderTitle(self.pygame_gui_ui_manager, None, self.planet.name)
        # panel background
        self.panel_bg = UILargeDefaultPanelTransparentBg(self.pygame_gui_ui_manager)
        # main panel
        self.panel = UILargeDefaultPanel(self.pygame_gui_ui_manager, self.panel_bg)
        # story content, empty init
        self.story_description = UILargeRightTextBox(self.pygame_gui_ui_manager, self.panel, "")

        self.continue_button = UILargeDefaultButton(self.pygame_gui_ui_manager, self.panel_bg)
        self.continue_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self.continue_story())

    def set_next_active_story_line(self):
        # Check if there is another story line available
        if self.active_story_line_index < len(self.story_block.story_lines):
            # Set the next story line as active
            self.active_story_line = self.story_block.story_lines[self.active_story_line_index]
            self.active_story_line_index += 1  # Increment the index for the next call
        else:
            # If there are no more story lines, set the active story line to None or handle the end of the story block
            self.active_story_line = None

    def continue_story(self):
        self.set_next_active_story_line()

        if not self.active_story_line:
            self.kill()
            return

        if self.story_description:
            self.story_description.set_text(self.active_story_line.text)

        if self.story_image:
            self.story_image.kill()
        if self.story_image_description:
            self.story_image_description.kill()

        self.set_story_image(self.active_story_line)

    def set_story_image(self, story_line: StoryLine):
        portrait_path = ""
        if len(story_line.image_path) > 0:
            portrait_path = story_line.image_path
        if len(story_line.image_description) > 0:
            if story_line.image_description.lower() == "milo":
                portrait_path = self.game.engine.config.portrait_milo
            elif story_line.image_description.lower() == "lyra":
                portrait_path = self.game.engine.config.portrait_lyra
            elif story_line.image_description.lower() == "agatha":
                portrait_path = self.game.engine.config.portrait_agatha
            elif story_line.image_description.lower() == "victor":
                portrait_path = self.game.engine.config.portrait_victor
        # story image
        if len(portrait_path) > 0:
            image_surface = pygame.image.load(portrait_path).convert_alpha()
            self.story_image = UILargeLeftImage(self.pygame_gui_ui_manager, self.panel, image_surface)
            self.story_image_description = UILargeLeftImageDescription(self.pygame_gui_ui_manager, self.panel,
                                                                       story_line.image_description)

    def run(self) -> int:
        """Display the menu and return the selected option."""
        self.__build_ui()
        clock = pygame.time.Clock()
        self.is_running = True
        self.continue_story()
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
        return 1

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
