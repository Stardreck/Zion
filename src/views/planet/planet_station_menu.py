from __future__ import annotations
from src.views.planet.base_planet_menu import BasePlanetMenu
from src.models.planet import Planet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class PlanetStationMenu(BasePlanetMenu):
    def __init__(self, game: StoryGame, planet: Planet):
        title_text = "Handelsstation"
        button_texts = ("Aufgabe lösen", "Kostenlos tanken")
        super().__init__(game, planet, title_text, button_texts)
