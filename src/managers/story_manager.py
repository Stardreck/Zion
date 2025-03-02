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
        # iterate over the story and or quiz / task blocks

        current_quiz_count = 0
        total_quiz_count = len([block for block in story.blocks if block.block_type in {"quiz", "task", "boolean"}])

        for block in story.blocks:
            if block.block_type == "story":
                for story_line in block.story_lines:
                    story_view = StoryView(self.game, planet, story_line)
                    story_view.run()

            has_quizzes: bool = block.block_type in ["quiz", "task", "boolean"]
            ##### run quiz loop #####
            if has_quizzes:
                current_quiz_count += 1
                is_correct = False
                attempts = 1
                while is_correct is False:
                    match block.block_type:
                        case "quiz":
                            self.game.quiz_manager.run_quiz(block.quiz)
                        case "task":
                            self.game.quiz_manager.run_task(block.quiz)
                        case "boolean":
                            self.game.quiz_manager.run_boolean(block.quiz)
                    ##### update statistics #####
                    is_correct = self.game.quiz_manager.is_last_quiz_correct
                    self.game.statistics_manager.record_quiz_task_result(block.quiz, is_correct)

                    ##### if user failed, show consequence story line  #####
                    if not is_correct and block.quiz.story_consequence is not None:
                        print(f"[Story Quiz] failed attempt: {attempts}")
                        # if user failed X attempts, it's game over -> defined in star_config
                        if attempts == self.game.engine.config.game_over_story_quiz_max_attempts:
                            return self.game.run_game_over()
                        # show consequence story line
                        consequence_view = StoryView(self.game, planet, block.quiz.story_consequence)
                        consequence_view.run()

                        attempts += 1

                if total_quiz_count == current_quiz_count:
                    print(f"[Story Quiz] object gained")
