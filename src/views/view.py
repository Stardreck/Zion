from abc import ABC, abstractmethod

import pygame_gui


class View(ABC):
    def __init__(self, ui_manager: pygame_gui.UIManager):
        self.pygame_gui_ui_manager = ui_manager

    @abstractmethod
    def kill(self):
        pass