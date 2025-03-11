from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


# Base class for mini-games
class MiniGame(ABC):
    """
    abstract base class for mini-games.
    """

    def __init__(self, game: StoryGame, background_path: str):
        self.game = game
        self.finished: bool = False
        self.success: bool = False
        self.data_directory: str = "data"
        self.background_path: str = background_path

    def load_config_file_data(self):
        path = Path(self.data_directory) / "mini_games.json"
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    @abstractmethod
    def show_start_menu(self):
        """
        show the start menu
        """
        raise NotImplementedError("show_start_menu not implemented")

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """
        Handle a single pygame event.
        :param event: The event to process.
        """
        raise NotImplementedError("handle_event not implemented")

    @abstractmethod
    def update(self, delta_time: float):
        """
        Update the mini-game state.
        :param delta_time: Time elapsed since the last update.
        """
        raise NotImplementedError("update not implemented")

    @abstractmethod
    def draw(self):
        """
        Draw the mini-game on the given surface.
        """
        raise NotImplementedError("draw not implemented")

    @abstractmethod
    def is_finished(self) -> bool:
        """
        Check if the mini-game is finished.
        :return: True if finished, False otherwise.
        """
        return self.finished

    @abstractmethod
    def get_result(self) -> bool:
        """
        Get the result of the mini-game.
        :return: True if the mini-game was won, False otherwise.
        """
        return self.success

    @abstractmethod
    def run(self):
        """
        run the mini-game.
        """
        raise NotImplementedError("run not implemented")
