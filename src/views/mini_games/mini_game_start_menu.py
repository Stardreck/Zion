from __future__ import annotations

from src.views.mini_games.base_mini_game_menu import BaseMiniGameMenu
from src.models.planet import Planet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class MiniGameStartMenu(BaseMiniGameMenu):
    def __init__(self, game: StoryGame, background_path: str, title_text: str, description_text: str, button_text: str):
        super().__init__(game, background_path, title_text, description_text, button_text)
