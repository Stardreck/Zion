from __future__ import annotations
from typing import TYPE_CHECKING
from src.views.states.base_state_view import BaseStateView

if TYPE_CHECKING:
    from src.games.story_game import StoryGame

class GameOverView(BaseStateView):
    def __init__(self, game, backround_image_path):
        super().__init__(game, backround_image_path)
