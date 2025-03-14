import sys

import pygame

from src.games.game_data import GameData
from src.games.story_game import StoryGame
from src.mini_games.cable_connection.cable_connection_mini_game import CableConnectionMiniGame
from src.mini_games.test_mini_game_01 import TestMiniGame01
from src.plugins.video_player import VideoPlayer
from src.star_config import StarConfig
from src.star_engine import StarEngine


def main():
    ##### init Config #####
    config = StarConfig("data/star_config.json")

    ##### init game engine #####
    engine = StarEngine(config)

    ##### run system check #####
    #if sys.platform.startswith("linux"):
    #    is_system_valid = engine.run_system_check()
    #    if not is_system_valid:
    #        sys.exit()

    ##### intro video #####
    player = VideoPlayer(None)
    player.enable_standalone(config.width, config.height, config.title, config.full_screen)
    player.set_video("assets/videos/intro.mp4")
    player.play()

    ##### show main menu #####
    result = engine.show_main_menu()
    if result == 0:
        # game closed
        return
    if result == 1:
        # start story game
        data = GameData(config)
        game = StoryGame(engine, data)
        engine.run(game)


def debug():
    config = StarConfig("data/star_config.json")
    engine = StarEngine(config)
    data = GameData(config)
    game = StoryGame(engine, data)
    engine.run(game)


def test_mini_game_01():
    config = StarConfig("data/star_config.json")
    engine = StarEngine(config)
    data = GameData(config)
    game = StoryGame(engine, data)

    mini_game = TestMiniGame01(game)
    clock = pygame.time.Clock()
    while not mini_game.is_finished():
        delta_time = clock.tick(game.engine.fps) / 1000.0
        for event in pygame.event.get():
            mini_game.handle_event(event)
        mini_game.update(delta_time)
        mini_game.draw(game.window)
        pygame.display.flip()
    if mini_game.get_result():
        print("Mini-game won!")
    else:
        print("Mini-game lost!")


def test_mini_game_cable_connection1():
    config = StarConfig("data/star_config.json")
    engine = StarEngine(config)
    data = GameData(config)
    game = StoryGame(engine, data)

    mini_game = CableConnectionMiniGame(game)
    mini_game.run()

    result = mini_game.get_result()
    print("Result:", result)


# entry point
if __name__ == "__main__":
    debug()
