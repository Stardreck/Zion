from __future__ import annotations
import random
from src.managers.manager import Manager
from src.mini_games.asteroid_dodge.asteroid_dodge_mini_game import AsteroidDodgeMiniGame
from src.mini_games.bubble_pop_challenge.bubble_pop_challenge_mini_game import BubblePopChallengeMiniGame
from src.mini_games.cable_connection.cable_connection_mini_game import CableConnectionMiniGame
from typing import List, TYPE_CHECKING

from src.mini_games.magical_orbs_connection.magical_orbs_connection import MagicalOrbsConnectionMiniGame
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
            # Don't play a mini-game this round.
            return False

        ##### Run a random mini-game #####
        mini_game_options = [
            self.__play_bubble_pop_challenge_mini_game
            #self.__play_cable_connection_mini_game,
            #self.__play_magical_orbs_connection_mini_game
        ]
        mini_game_choice = random.choice(mini_game_options)
        result = mini_game_choice()
        return result

    def __play_cable_connection_mini_game(self) -> bool:
        background = self.__get_background_image_path()

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

    def __play_magical_orbs_connection_mini_game(self) -> bool:
        background = self.__get_background_image_path()

        title_text = "Minispiel"
        description_text = "Lyra schlief tief, ihr Atem ruhig und gleichmässig. Doch in ihrem Geist entfaltete sich eine andere Welt – ein Traum, seltsam und doch vertraut.<br/>Sie schwebte in einem endlosen Raum aus schimmerndem Licht. Farben tanzten um sie herum, sanfte Wellen aus Blau, Violett und Gold. Vor ihr schwebten mehrere leuchtende Kugeln, pulsierend wie kleine Sterne.<br/>Eine flüsternde Stimme, fern und schwer zu greifen, hallte durch ihren Traum: «Verbinde sie…»"
        button_text = "starten"

        mini_game_start_menu = MiniGameStartMenu(self.game, background, title_text, description_text, button_text)
        mini_game_start_menu.run()

        num_pairs = random.choice([6, 8, 10])
        mini_game = MagicalOrbsConnectionMiniGame(self.game, background, num_pairs)
        mini_game.run()

        result = mini_game.get_result()
        return result

    def __play_bubble_pop_challenge_mini_game(self):
        background = self.__get_background_image_path()
        title_text = "Minispiel"
        description_text = "Agatha behauptet steif und fest, dass ihre Reflexe unschlagbar sind – doch nach dem letzten Training tuscheln die anderen bereits hinter ihrem Rücken. Das kann sie natürlich nicht auf sich sitzen lassen! Also wird sie ihnen zeigen, wie schnell sie reagieren kann. Blasen tauchen überall auf, und sie bringt sie einer nach der anderen zum Platzen. Am Ende wird keiner mehr an ihrer Treffsicherheit zweifeln."
        button_text = "starten"

        mini_game_start_menu = MiniGameStartMenu(self.game, background, title_text, description_text, button_text)
        mini_game_start_menu.run()

        mini_game = BubblePopChallengeMiniGame(self.game, background)
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
