from __future__ import annotations
import pygame
import sys

from typing import TYPE_CHECKING

from src.system_check import SystemCheck

if TYPE_CHECKING:
    from src.games.story_game import StoryGame

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

    def run_system_check(self) -> bool:
        """
        check the GPIO I2C bus connection, if the connection can't be established,
        shows a message to indicate that the raspberry pi must be shutdown.
        only executed on the raspberry itself (linux OS)
        """

        system_check = SystemCheck(self)
        is_system_valid = system_check.is_system_valid()
        if not is_system_valid:
            return False

        return True

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
        if self.config.full_screen:
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
