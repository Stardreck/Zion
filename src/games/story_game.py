import random
import sys
import time
from typing import Dict, List

import pygame

from src.games.game import Game
from src.games.game_data import GameData
from src.managers.debug_manager import DebugManager
from src.managers.event.event_manager import EventManager
from src.managers.hud_manager import HUDManager
from src.managers.input.input_manager import InputManager
from src.managers.inventory_manager import InventoryManager
from src.managers.quiz_manager import QuizManager
from src.managers.statistics_manager import StatisticsManager
from src.managers.story_manager import StoryManager
from src.managers.ui_manager import UIManager
from src.models.event_card import EventCard
from src.models.planet import Planet
from src.models.quiz import Quiz
from src.models.story_line import StoryLine
from src.star_engine import StarEngine

from src.views.common.info_view import InfoView
from src.views.quiz.error_view import ErrorView
from src.views.states.game_over_view import GameOverView
from src.views.story.story_view import StoryView


class StoryGame(Game):
    """
    This is the main story game instance, responsible for the entire game logic
    """

    def __init__(self, engine: StarEngine, data: GameData):
        super().__init__(engine, data)

        ##### Game Data #####
        self.fuel: int = self.engine.config.game_settings_start_fuel
        self.hull: int = self.engine.config.game_settings_start_hull

        # start location
        self.player_row: int = self.engine.config.player_settings_start_row
        self.player_col: int = self.engine.config.player_settings_start_col
        # init planet and planet quizzes
        self.current_planet: Planet | None = None
        self.planet_quizzes_current: Dict[str, List[Quiz]] = {
            pname: list(q_list) for pname, q_list in self.data.planet_quizzes.items()
        }

        ##########################
        ##### Init Managers ######
        ##########################

        ##### Input Manager #####
        self.input_manager: InputManager = InputManager(self)
        if sys.platform.startswith("linux"):
            # only include the mcp manager on the raspberry pi, otherwise the entire game could not be executed on windows
            # as this manager depends on linux specific libraries (GPIO connection)
            from src.managers.input.mcp_input_manager import MCPInputManager, GAME_BOARD_PIN_DEFINITIONS
            self.mcp_input_manager = MCPInputManager(self, GAME_BOARD_PIN_DEFINITIONS)
            from src.managers.input.switch_input_manager import SwitchInputManager
            self.switch_input_manager = SwitchInputManager(self)
        else:
            self.mcp_input_manager = None
            self.switch_input_manager = None

        self.last_mcp_time: float = 0.0  # last time MCP/Switch-Events

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
        self.inventory_manager = InventoryManager(self)

        ##### Statistics Manager #####
        self.statistics_manager: StatisticsManager = StatisticsManager()

        ##### Debug Manager #####
        self.debug_manager: DebugManager = DebugManager(self)

        ##### windows #####
        default_backgrounds = self.engine.config.game_settings_default_backgrounds
        chosen_image: str = random.choice(default_backgrounds)
        img = pygame.image.load(chosen_image).convert()
        self.default_bg_full: pygame.Surface | None = pygame.transform.scale(img,
                                                                             (self.engine.width, self.engine.height))

        self.move_player(self.engine.config.player_settings_start_row, self.engine.config.player_settings_start_col)

    def handle_events(self):
        self.input_manager.process_events()
        current_time = time.time()
        if current_time - self.last_mcp_time >= 2.0:
            if self.mcp_input_manager:
                self.mcp_input_manager.process_events()
            if self.switch_input_manager:
                self.switch_input_manager.process_events()
            self.last_mcp_time = current_time  # reset timer

    def update(self, delta_time: float):
        self.ui_manager.gui_manager.update(delta_time)
        self.update_managers()

    def update_managers(self):
        self.hud_manager.update()
        self.debug_manager.update()

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

        if move_row != 0 or move_column != 0:
            new_row = self.player_row + move_row
            new_col = self.player_col + move_column

            self.move_player(new_row, new_col)

    def __is_game_over(self):
        if self.fuel <= 0 or self.hull <= 0:
            return True
        return False

    def move_player(self, new_row: int, new_column: int):
        # change player location
        self.player_row = new_row
        self.player_col = new_column
        # movement cost
        self.fuel -= 1
        # update hud (update fuel change)
        self.update_managers()

        if self.__is_game_over():
            return self.run_game_over()

        self.run_position_actions()

    def run_position_actions(self):

        ##### apply active event effects #####
        self.event_manager.run_active_events()

        self.current_planet = None
        ##### Planet #####
        # check if the position is a planet
        # loop through each planet object
        for planet in self.data.planets:
            # check if the planet coordinates matches the player ones
            if planet.row == self.player_row and planet.col == self.player_col:
                self.current_planet = planet
                ##### update debug view with current_planet set #####
                self.update_managers()
                # if not planet.visited:
                # self.run_planet_actions(planet)
                # self.trigger_planet_event(planet)
                break

        if not self.current_planet is None:
            self.run_planet_actions(self.current_planet)
            return
        else:
            ##### general field - show default quiz #####
            self.run_general_field_actions()

        ##### event #####

        # check for forced events
        forced_events: List[EventCard] | [] = self.event_manager.get_forced_events()
        if len(forced_events) > 0:
            for forced_event in forced_events:
                if forced_event.category == "game_over":
                    self.event_manager.run_event(forced_event)
                    self.run_game_over()
                    break

                self.event_manager.run_event(forced_event)

        self.event_manager.trigger_event_if_possible()

        ##### check if event results in game over #####
        if self.__is_game_over():
            return self.run_game_over()

    def run_general_field_actions(self):
        ##### display quiz or task #####
        self.quiz_manager.run_general_field_action()

        ##### update event system #####
        is_last_quiz_correct = self.quiz_manager.is_last_quiz_correct
        if is_last_quiz_correct:
            self.event_manager.decrease_error_count()
        else:
            self.event_manager.increase_error_count()

    def run_planet_actions(self, planet: Planet):
        ##### show story content on start planet #####
        if planet.is_start_planet:
            self.ui_manager.display_cutscene(planet.cutscene_media)
            self.story_manager.show_planet_story(planet, self.data.story_segments[planet.name])
            return
        if planet.is_end_planet:
            ##### player hasn't all items, show error message #####
            if not self.has_all_items():
                story_line = StoryLine(
                    self.engine.config.planet_menu_states_zion_not_allowed_text,
                    "", "Lyra")
                error_view = StoryView(self, planet, story_line)
                error_view.run()
                return

        if planet.is_spacestation:
            self.story_manager.show_spacestation_menu(planet)
            return

        ##### show planet menu and await user input #####
        selected_planet_menu_option = self.story_manager.show_planet_menu(planet)

        ##### visit station clicked #####
        if selected_planet_menu_option == 1:
            selected_station_option = self.story_manager.show_planet_station_menu(planet)

            ##### solve quiz clicked #####
            if selected_station_option == 1:
                print("aufgabe lösen")
                self.run_station_quiz_fuel_action(planet)

            ##### free refuel clicked #####
            if selected_station_option == 2:
                print("kostenlos tanken")
                self.run_station_free_fuel_action(planet)

        ##### visit planet clicked #####
        if selected_planet_menu_option == 2:
            # show cutscene
            self.ui_manager.display_cutscene(planet.cutscene_media)

            if planet.visited:
                story_line = StoryLine(
                    self.engine.config.planet_menu_visited,
                    "", "Victor")
                error_view = StoryView(self, planet, story_line)
                error_view.run()
            else:
                if planet.depend_on is not None:
                    depend_planet = next(
                        (p for p in self.data.planets if p.name.lower() == planet.depend_on.lower()), None
                    )

                    if depend_planet is not None and not depend_planet.visited:
                        print("depend planet not visited", depend_planet.name)
                        error_view = InfoView(self, "Falsch abgebogen", self.engine.config.portrait_victor,
                                              depend_planet.background_image,
                                              "Moment mal – wir sind hier zu früh. Wir müssen zuerst woanders hin, bevor wir hier weitermachen können.")
                        error_view.run()
                        return

                # show the planet stories
                self.story_manager.show_planet_story(planet, self.data.story_segments[planet.name])
                planet.visited = True

            print("Planet besuchen")

    def run_station_quiz_fuel_action(self, planet: Planet):
        ##### display quiz or task #####
        self.run_general_field_actions()

        is_correct = self.quiz_manager.is_last_quiz_correct
        if is_correct:
            description = f"Milos: «Ich hatte keine Zweifel daran, dass wir es schaffen, wir sind eben gut.» <b>+{self.engine.config.planet_menu_fuel_quiz_correct_amount} Treibstoff"
            self.fuel += self.engine.config.planet_menu_fuel_quiz_correct_amount
            self.hull += self.engine.config.planet_menu_fuel_quiz_correct_amount
        else:
            description = f"Milos: «Schade das war wohl nichts. Naja, immerhin haben sie uns aus Mitleid ein wenig geschenkt. Vielleicht klappt es ja beim nächsten Mal.» <b>+{self.engine.config.planet_menu_fuel_quiz_wrong_amount} Treibstoff"
            self.fuel += self.engine.config.planet_menu_fuel_quiz_wrong_amount
            self.hull += self.engine.config.planet_menu_fuel_quiz_wrong_amount

        view = InfoView(self, "Resultat", self.engine.config.portrait_milo,
                        self.engine.config.planet_menu_fuel_station_background_image_path, description,
                        "Akzeptieren")
        view.run()

    def run_station_free_fuel_action(self, planet: Planet):
        ##### display a message and add the fuel #####
        description = f"Die Minerva wird aufgetankt, mit <b>+{self.engine.config.planet_menu_fuel_free_amount} Treibstoff</b> ist sie wieder einsatzbereit."

        view = InfoView(self, "Tanken", self.engine.config.planet_menu_fuel_station_image_path,
                        self.engine.config.planet_menu_fuel_station_background_image_path, description,
                        "Akzeptieren")
        view.run()
        self.fuel += self.engine.config.planet_menu_fuel_free_amount
        self.hull += self.engine.config.planet_menu_fuel_free_amount

    def run_game_over(self):
        print("[Game Over]")
        self.hud_manager.kill_children()

        if self.fuel <= 0:
            background_image = self.engine.config.game_over_fuel_background_path
        elif self.hull <= 0:
            background_image = self.engine.config.game_over_hull_background_path
        else:
            backgrounds = self.engine.config.game_over_default_background_paths
            background_image = random.choice(backgrounds)
        game_over_view = GameOverView(self, background_image)
        game_over_view.run()

    def has_all_items(self) -> bool:
        items = self.inventory_manager.get_items()
        if len(items) == 4:
            return True
        return False

    def restart(self):
        print("[Game Restart]")
        pass
