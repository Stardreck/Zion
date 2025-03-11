from __future__ import annotations
from src.views.planet.base_planet_menu import BasePlanetMenu
from src.models.planet import Planet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class SpacestationMenu(BasePlanetMenu):
    def __init__(self, game: StoryGame, planet: Planet):
        title_text = planet.name
        fuel_cost = game.engine.config.game_settings_wormhole_cost
        button_texts = ("Station besuchen", f"Wurmloch betreten (-{fuel_cost} Treibstoff)")
        super().__init__(game, planet, title_text, button_texts)
