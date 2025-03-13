from __future__ import annotations
from typing import List, TYPE_CHECKING, Tuple
from gpiozero import Button
from src.managers.manager import Manager

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class SwitchInputManager(Manager):
    def __init__(self, game: StoryGame):
        super().__init__()
        self.game = game
        self.button = Button(26)
        self.is_button_pressed = False

    def process_events(self):
        print("SwitchInputManager.process_events()")
        if self.button.is_pressed:
            print("switch active")
            self.is_button_pressed = True
        else:
            print("switch inactive")
            self.is_button_pressed = False
