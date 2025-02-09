import sys
from abc import ABC, abstractmethod

import pygame
from pygame import Surface

from src.games.game_data import GameData
from src.star_engine import StarEngine


class Game(ABC):
    """
    Abstract game base class
    """
    def __init__(self, engine: StarEngine, data: GameData):
        self.engine: StarEngine = engine
        self.data: GameData = data

        self.window: Surface = engine.window

        self.is_running = True


    def stop(self):
        self.is_running = False
        pygame.quit()
        sys.exit()