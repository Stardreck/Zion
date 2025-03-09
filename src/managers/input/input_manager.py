from __future__ import annotations
import pygame

from typing import List, TYPE_CHECKING, Optional

from src.managers.manager import Manager

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class InputManager(Manager):
    """
    Handles user input and delegates actions to the game logic.
    """

    def __init__(self, game: StoryGame):
        """
        Initializes the InputManager with a reference to the game instance.
        :param game: The game instance that will receive input events.
        """
        super().__init__()
        self.game = game

    def process_events(self):
        """
        Processes all incoming events and triggers corresponding game actions.
        """
        for event in pygame.event.get():
            self.game.ui_manager.gui_manager.process_events(event)
            if event.type == pygame.QUIT:
                self.game.stop()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            elif event.type == pygame.MOUSEMOTION:
                pass


    def handle_keydown(self, event: pygame.event.Event):
        if event.key == pygame.K_ESCAPE:
            self.game.stop()
        elif event.key == pygame.K_d:
            self.game.debug_manager.toggle_debug_mode()
            pass
        if self.game.ui_manager.gui_manager.get_focus_set() is None:
            self.game.handle_movement(event)
