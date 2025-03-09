from __future__ import annotations
import pygame
import sys

from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.games.story_game import StoryGame

from pygame import Surface
from pygame_gui import UIManager
from src.star_config import StarConfig
from src.views.main_menu import MainMenu


class StarEngine:
    def __init__(self, config: StarConfig):
        """
        Initialize the game engine, set up pygame, and load resources.
        """
        self.config: StarConfig = config
        self.__initialize_pygame()
        self.__setup_display()
        self.pygame_gui_ui_manager: UIManager = UIManager((self.width, self.height), 'theme/theme.json')
        self.pygame_gui_ui_manager.get_theme().get_font_dictionary().preload_font(16, "noto_sans", True, False, True,
                                                                                  True)
        self.main_menu: MainMenu = MainMenu(self.pygame_gui_ui_manager, self.config)

    def show_main_menu(self) -> int:
        """
        Display the main menu and return the selected option.
        :return: Selected option as an int
        0 = Quit
        1 = StoryGame
        """
        return self.main_menu.run(self.window, self.clock, self.fps)

    def run(self, game: StoryGame) -> None:
        """
        Main game loop that handles events, updates, and rendering.
        :param game: The active game instance.
        """
        while self.is_running and game.is_running:
            delta_time = self.clock.tick(self.fps) / 1000.0
            game.handle_events()
            game.update(delta_time)
            game.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    ##### private methods #####
    def __initialize_pygame(self):
        """
        Initialize pygame and set up general settings.
        """
        pygame.init()
        self.width = self.config.width
        self.height = self.config.height
        self.fps = self.config.fps
        self.is_running = True

    def __setup_display(self):
        """
        Set up the display, window title, and clock.
        """
        self.title = self.config.title
        self.window = pygame.display.set_mode((self.width, self.height))
        # self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
