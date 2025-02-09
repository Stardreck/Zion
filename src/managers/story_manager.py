from __future__ import annotations

from typing import TYPE_CHECKING

from src.managers.manager import Manager
from src.models.planet import Planet
from src.models.story import Story
from src.views.planet.planet_menu import PlanetMenu
from src.views.planet.planet_station_menu import PlanetStationMenu
from src.views.story.story_view import StoryView

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class StoryManager(Manager):
    def __init__(self, game: StoryGame):
        super().__init__()
        self.game: StoryGame = game

    def show_planet_menu(self, planet: Planet):
        planet_menu = PlanetMenu(self.game, planet)

        return planet_menu.run()

    def show_planet_station_menu(self, planet: Planet):
        planet_station_menu = PlanetStationMenu(self.game, planet)

        return planet_station_menu.run()

    def show_planet_story(self, planet: Planet, story: Story):
        for story_line in story.story_lines:
            story_view = StoryView(self.game, planet, story_line)
            story_view.run()
