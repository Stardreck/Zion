from __future__ import annotations
from src.views.planet.base_planet_menu import BasePlanetMenu
from src.models.planet import Planet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class PlanetMenu(BasePlanetMenu):
    def __init__(self, game: StoryGame, planet: Planet):
        # Use the planet's name as title.
        title_text = planet.name
        # Button texts: first button "Station besuchen", second button "Planet besuchen"
        button_texts = ("Station besuchen", "Planet besuchen")
        super().__init__(game, planet, title_text, button_texts)
