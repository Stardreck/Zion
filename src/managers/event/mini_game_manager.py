from __future__ import annotations
import random
from src.managers.manager import Manager
from src.mini_games.asteroid_dodge.asteroid_dodge_mini_game import AsteroidDodgeMiniGame
from src.mini_games.cable_connection.cable_connection_mini_game import CableConnectionMiniGame
from typing import List, TYPE_CHECKING
from src.views.mini_games.mini_game_start_menu import MiniGameStartMenu

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class MiniGameManager(Manager):
    def __init__(self, game: StoryGame):
        super().__init__()
        self.game: StoryGame = game
        # Adjustable probabilities in star_config.json
        self.mini_game_probability: float = self.game.engine.config.mini_game_probability
        self.menu_backgrounds: List[str] = self.game.engine.config.mini_game_menu_backgrounds

    def play_mini_game_if_possible(self):
        if not self.__should_game_be_played():
            # don't play a mini-game this round
            return False

        ##### run a random mini-game #####

        # cable connection mini-game
        result = self.__play_cable_connection_mini_game()
        # asteroid doge mini-game
        # result = self.__play_asteroid_dodge_mini_game()

    def __play_cable_connection_mini_game(self) -> bool:
        background = self.__get_background_image_path()
        # todo define mini game title and description
        title_text = "Minispiel"
        description_text = "Grossartig. IRIS hat ein Software-Update gemacht, und jetzt ist die Tür verriegelt. Wir müssen die richtigen Kabel verbinden, um die Sperre zu umgehen"
        button_text = "starten"

        mini_game_start_menu = MiniGameStartMenu(self.game, background, title_text, description_text, button_text)
        mini_game_start_menu.run()

        num_pairs = random.choice([4, 6, 8])
        mini_game = CableConnectionMiniGame(self.game, background, num_pairs)
        mini_game.run()
        result = mini_game.get_result()
        return result

    def __play_asteroid_dodge_mini_game(self) -> bool:
        background = self.__get_background_image_path()
        # todo define mini game title and description
        title_text = "Minispiel"
        description_text = "oha"
        button_text = "starten"

        mini_game_start_menu = MiniGameStartMenu(self.game, background, title_text, description_text, button_text)
        mini_game_start_menu.run()

        mini_game_start_menu = AsteroidDodgeMiniGame(self.game, background)
        mini_game_start_menu.run()

        num_pairs = random.choice([4, 6, 8])
        mini_game = CableConnectionMiniGame(self.game, background, num_pairs)
        mini_game.run()
        result = mini_game.get_result()
        return result

    def __should_game_be_played(self):
        if random.random() < self.mini_game_probability:
            return True
        return False

    def __get_background_image_path(self) -> str:
        # select a random spaceship window image
        return random.choice(self.menu_backgrounds)
