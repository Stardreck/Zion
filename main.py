from src.games.game_data import GameData
from src.games.story_game import StoryGame
from src.plugins.video_player import VideoPlayer
from src.star_config import StarConfig
from src.star_engine import StarEngine


def main():
    ##### init Config #####
    config = StarConfig("data/star_config.json")
    config.validate()

    ##### intro video #####
    player = VideoPlayer(None)
    player.enable_standalone(config.width, config.height, config.title)
    player.set_video("assets/videos/intro_video.mp4")
    player.play()

    ##### init game engine #####
    engine = StarEngine(config)

    ##### show main menu #####
    result = engine.show_main_menu()
    if result == 0:
        return
    if result == 1:
        pass
        #data = GameData()
        #game = StoryGame(engine, data)
        #engine.run(game)


def debug():
    config = StarConfig("data/star_config.json")
    engine = StarEngine(config)
    data = GameData(config)
    game = StoryGame(engine, data)
    engine.run(game)


# entry point
if __name__ == "__main__":
    debug()
