from __future__ import annotations
from src.views.planet.base_planet_menu import BasePlanetMenu
from src.models.planet import Planet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class SpacestationMenu(BasePlanetMenu):
    def __init__(self, game: StoryGame, planet: Planet):

        fuel_cost = game.engine.config.game_settings_wormhole_cost
        if game.has_all_items():
            title_text = planet.name
            button_texts = ("", f"Wurmloch betreten (-{fuel_cost} Treibstoff)")
        else:
            title_text = "zugang verweigert"
            button_texts = ("verlassen", "")

        super().__init__(game, planet, title_text, button_texts)

        if game.has_all_items():
            self.show_button_1 = False
        else:
            self.show_button_2 = False
