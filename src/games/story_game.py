from typing import Dict, List

import pygame

from src.games.game import Game
from src.games.game_data import GameData
from src.managers.debug_manager import DebugManager
from src.managers.event.event_manager import EventManager
from src.managers.hud_manager import HUDManager
from src.managers.input_manager import InputManager
from src.managers.quiz_manager import QuizManager
from src.managers.story_manager import StoryManager
from src.managers.ui_manager import UIManager
from src.models.planet import Planet
from src.models.quiz import Quiz
from src.star_engine import StarEngine


class StoryGame(Game):
    def __init__(self, engine: StarEngine, data: GameData):
        super().__init__(engine, data)

        ##### Game Data #####
        self.fuel: int = 50
        self.hull: int = 50
        # Starting location
        self.player_row: int = 2
        self.player_col: int = 2
        self.current_planet = None
        self.planet_quizzes_current: Dict[str, List[Quiz]] = {
            pname: list(q_list) for pname, q_list in self.data.planet_quizzes.items()
        }

        ##### Input Manager #####
        self.input_manager: InputManager = InputManager(self)

        ##### UI Manager #####
        self.ui_manager: UIManager = UIManager(self)
        self.hud_manager = HUDManager(self)

        ##### Quiz Manager #####
        self.quiz_manager: QuizManager = QuizManager(self)

        ##### Event Manager #####
        self.event_manager: EventManager = EventManager(self, data.event_cards)

        ##### Story Manager #####
        self.story_manager: StoryManager = StoryManager(self)

        ##### Inventory Manager #####

        ##### Debug Manager #####
        self.debug_manager: DebugManager = DebugManager(self)

        ##### windows #####
        # todo change this hardcoded value to dynamic json
        img = pygame.image.load("assets/images/welcome_screen.png").convert()
        self.default_bg_full: pygame.Surface | None = pygame.transform.scale(img,
                                                                             (self.engine.width, self.engine.height))

    def handle_events(self):
        self.input_manager.process_events()

    def update(self, delta_time: float):
        self.ui_manager.gui_manager.update(delta_time)
        self.debug_manager.update(delta_time)
        self.hud_manager.update()

    def draw(self):
        self.window.blit(self.default_bg_full, (0, 0))
        self.ui_manager.gui_manager.draw_ui(window_surface=self.window)

    def handle_movement(self, event):
        move_row, move_column = 0, 0
        if event.key == pygame.K_UP:
            move_row = -1
        elif event.key == pygame.K_DOWN:
            move_row = 1
        elif event.key == pygame.K_LEFT:
            move_column = -1
        elif event.key == pygame.K_RIGHT:
            move_column = 1

        if (move_row != 0 or move_column != 0) and self.fuel > 0:
            new_row = self.player_row + move_row
            new_col = self.player_col + move_column

            self.move_player(new_row, new_col)

        elif move_row != 0 or move_column != 0:
            print("[Game Over]")

    def move_player(self, new_row: int, new_column: int):
        # change player location
        self.player_row = new_row
        self.player_col = new_column
        # movement cost
        self.fuel -= 1

        self.run_position_actions()

    def run_position_actions(self):
        self.current_planet = None
        ##### Planet #####
        # check if the position is a planet
        # loop through each planet object
        for planet in self.data.planets:
            # check if the planet coordinates matches the player ones
            if planet.row == self.player_row and planet.col == self.player_col:
                self.current_planet = planet
                # if not planet.visited:
                # self.run_planet_actions(planet)
                # self.trigger_planet_event(planet)
                break

        if not self.current_planet is None and not self.current_planet.visited:
            self.run_planet_actions(self.current_planet)
        else:
            ##### general field - show default quiz #####
            self.run_general_field_actions()

        ##### event #####
        self.event_manager.trigger_event_if_possible()

    def run_general_field_actions(self):
        self.quiz_manager.run("default")

    def run_planet_actions(self, planet: Planet):

        ##### show planet menu and await user input #####
        selected_planet_menu_option = self.story_manager.show_planet_menu(planet)

        ##### visit station clicked #####
        if selected_planet_menu_option == 1:
            selected_station_option = self.story_manager.show_planet_station_menu(planet)

            ##### solve quiz clicked #####
            if selected_station_option == 1:
                print("aufgabe lösen")

            ##### free refuel clicked #####
            if selected_station_option == 2:
                print("kostenlos tanken")

        ##### visit planet clicked #####
        if selected_planet_menu_option == 2:
            # show cutscene
            self.ui_manager.display_cutscene(planet.cutscene_media)

            # show the planet stories
            self.story_manager.show_planet_story(planet, self.data.story_segments[planet.name])

            print("Planet besuchen")
