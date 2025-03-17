from __future__ import annotations
from src.views.planet.base_planet_menu import BasePlanetMenu
from src.models.planet import Planet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class PlanetMenu(BasePlanetMenu):
    def __init__(self, game: StoryGame, planet: Planet):
        title_text = planet.name
        button_texts = ("Station besuchen", "Planet besuchen")
        show_button_1 = True
        show_button_2 = True
        if planet.is_fuel_planet:
            show_button_2 = False
        super().__init__(game, planet, title_text, button_texts, show_button_1, show_button_2)
