from __future__ import annotations

import math
import pygame
import pygame_gui

from pygame_gui.elements import UIWindow, UIImage, UILabel
from typing import List, TYPE_CHECKING

from src.enums.color import Color

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class DebugManager:
    """
    DebugManager implements a debug view using pygame_gui elements exclusively.
    All visual components (background image, hex grid, planets, player icon, and debug text)
    are represented as UI elements placed in a dedicated UIWindow.
    """

    def __init__(self, game: StoryGame):
        """
        Initialize the DebugManager.

        :param game: The main game instance from which debug data and the UI manager are obtained.
        """
        self.game = game
        self.debug_mode = False

        # Hexagon grid configuration
        self.hex_rows = 11
        self.hex_cols = 11
        self.hex_radius = 25
        self.offset_x = 150
        self.offset_y = 200

        # Load necessary image assets (with fallbacks in case of errors)
        self.bg_solar_system = self.__load_image("assets/images/solar_system.png", fallback_size=(800, 600))
        self.hexagon_image = self.__load_image("assets/images/hexagon.png", fallback_size=(50, 50))
        self.planet_image = self.__load_image("assets/images/planet.png", fallback_size=(30, 30))
        self.fuel_planet_image = self.__load_image("assets/images/fuel_planet.png", fallback_size=(20, 20))
        self.player_image = self.__load_image("assets/images/player.png", fallback_size=(24, 24))

        # Create the main debug window using pygame_gui
        self.debug_window: UIWindow = UIWindow(
            rect=pygame.Rect(50, 50, 800, 600),
            manager=self.game.ui_manager.gui_manager,
            window_display_title="Debug View"
        )

        # Create a background UIImage (the solar system image) filling the window
        self.bg_image_ui = UIImage(
            relative_rect=pygame.Rect(0, 0, 800, 600),
            image_surface=self.bg_solar_system,
            manager=self.game.ui_manager.gui_manager,
            container=self.debug_window
        )

        # Create UI elements for the hex grid; these elements are positioned using the grid calculation.
        self.hex_ui_elements: List[UIImage] = []
        self.__create_hex_grid()

        # Create UI elements for the planets.
        # (They will be updated dynamically in update().)
        self.planet_ui_elements: List[UIImage] = []
        self.__create_planet_elements()

        # Create the player UI element.
        self.player_ui = UIImage(
            relative_rect=pygame.Rect(0, 0, self.player_image.get_width(), self.player_image.get_height()),
            image_surface=self.player_image,
            manager=self.game.ui_manager.gui_manager,
            container=self.debug_window
        )

        # Create debug text labels to show game status and debug info.
        self.debug_labels: List[UILabel] = []
        self.__create_debug_labels()

        # Hide the debug window initially.
        self.debug_window.hide()

    def toggle_debug_mode(self):
        """
        Toggle the debug mode on/off. The debug window is shown or hidden accordingly.
        """
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.debug_window.show()
        else:
            self.debug_window.hide()
        print(f"[DEBUG] Debug mode: {self.debug_mode}")

    def update(self, delta_time: float):
        """
        Update the debug UI elements based on the current game state.
        This method should be called in the main game loop.

        :param delta_time: Time elapsed since the last frame.
        """
        if not self.debug_mode:
            return

        # 1. Update planet UI elements:
        # Remove existing planet elements and recreate them so that their positions reflect the game state.
        for planet_ui in self.planet_ui_elements:
            planet_ui.kill()  # Remove from the UI manager
        self.planet_ui_elements.clear()

        # For each planet in the game data, create a new UIImage element.
        for planet in self.game.data.planets:
            cx, cy = self.__get_hex_center(planet.row, planet.col)
            if planet.is_fuel_planet:
                image = self.fuel_planet_image
            else:
                image = self.planet_image
            size = image.get_size()
            planet_rect = pygame.Rect(
                int(cx - size[0] / 2), int(cy - size[1] / 2),
                size[0], size[1]
            )
            planet_ui = UIImage(
                relative_rect=planet_rect,
                image_surface=image,
                manager=self.game.ui_manager.gui_manager,
                container=self.debug_window
            )
            self.planet_ui_elements.append(planet_ui)

        # 2. Update the player's UI element position.
        cx, cy = self.__get_hex_center(self.game.player_row, self.game.player_col)
        player_size = self.player_image.get_size()
        self.player_ui.set_relative_position(
            (int(cx - player_size[0] / 2), int(cy - player_size[1] / 2))
        )

        # 3. Update debug text information.
        # Combine different info sections into one list.
        general_info = [
            "Debug Mode [D]",
            f"Fuel: {self.game.fuel}",
            f"Hull: {self.game.hull}",
            f"Pos(r={self.game.player_row}, c={self.game.player_col})",
            f"Current Planet: {self.game.current_planet.name if self.game.current_planet else 'None'}"
        ]
        event_info = [
            "EventManager:",
            f"Error Count: {self.game.event_manager.selection_manager.error_count}"
        ]
        game_stats_info = [
            "GameStats:",
            f"Inventory Items: {len(self.game.inventory_manager.get_items())}"
        ]
        # Merge all lines (you may adjust the ordering as needed)
        debug_texts = general_info + event_info + game_stats_info

        # Update each UILabel with the corresponding debug text.
        for i, label in enumerate(self.debug_labels):
            if i < len(debug_texts):
                label.set_text(debug_texts[i])
            else:
                label.set_text("")

    def __create_hex_grid(self):
        """
        Create the hex grid UI elements.
        Each hexagon is represented by an UIImage using the hexagon asset.
        Their positions are computed using the grid settings.
        """
        # Remove any existing hexagon UI elements if they exist.
        for element in self.hex_ui_elements:
            element.kill()
        self.hex_ui_elements.clear()

        # Loop over grid rows and columns.
        for row in range(self.hex_rows):
            for col in range(self.hex_cols):
                cx, cy = self.__get_hex_center(row, col)
                hex_size = self.hexagon_image.get_size()
                hex_rect = pygame.Rect(
                    int(cx - hex_size[0] / 2), int(cy - hex_size[1] / 2),
                    hex_size[0], hex_size[1]
                )
                hex_ui = UIImage(
                    relative_rect=hex_rect,
                    image_surface=self.hexagon_image,
                    manager=self.game.ui_manager.gui_manager,
                    container=self.debug_window
                )
                self.hex_ui_elements.append(hex_ui)

    def __create_planet_elements(self):
        """
        Initially create UI elements for the planets.
        These elements will be refreshed in every update call.
        """
        self.planet_ui_elements.clear()
        for planet in self.game.data.planets:
            cx, cy = self.__get_hex_center(planet.row, planet.col)
            if planet.is_fuel_planet:
                image = self.fuel_planet_image
            else:
                image = self.planet_image
            size = image.get_size()
            planet_rect = pygame.Rect(
                int(cx - size[0] / 2), int(cy - size[1] / 2),
                size[0], size[1]
            )
            planet_ui = UIImage(
                relative_rect=planet_rect,
                image_surface=image,
                manager=self.game.ui_manager.gui_manager,
                container=self.debug_window
            )
            self.planet_ui_elements.append(planet_ui)

    def __create_debug_labels(self):
        """
        Create UILabel elements to display debug text information.
        The labels are arranged in columns within the debug window.
        """
        self.debug_labels.clear()
        label_width = 250
        label_height = 25
        padding = 5
        start_y = 10

        # For simplicity, create a fixed number of labels (10 in this example).
        # These labels will later be updated with dynamic debug information.
        for i in range(10):
            # Position labels in two or three columns (adjust as needed)
            column = i // 5  # e.g. 5 lines per column
            row = i % 5
            x = 10 + column * (label_width + padding)
            y = start_y + row * (label_height + padding)
            label = UILabel(
                relative_rect=pygame.Rect(x, y, label_width, label_height),
                text="",
                manager=self.game.ui_manager.gui_manager,
                container=self.debug_window
            )
            self.debug_labels.append(label)

    def __get_hex_center(self, row: int, col: int) -> tuple[float, float]:
        """
        Compute the center position of a hexagon cell based on its row and column.
        Uses the standard hex grid spacing formulas.

        :param row: The row index of the hexagon.
        :param col: The column index of the hexagon.
        :return: A tuple (center_x, center_y) representing the center coordinates.
        """
        vertical_spacing = self.hex_radius * 1.5
        horizontal_spacing = math.sqrt(3) * self.hex_radius
        center_x = self.offset_x + col * horizontal_spacing + (row % 2) * (horizontal_spacing / 2)
        center_y = self.offset_y + row * vertical_spacing
        return center_x, center_y

    def __load_image(self, path: str, fallback_size: tuple[int, int]) -> pygame.Surface:
        """
        Attempt to load an image from the specified path.
        If loading fails, return a fallback surface filled with black.

        :param path: The file path to the image asset.
        :param fallback_size: The size of the fallback surface.
        :return: A pygame.Surface containing the loaded image or fallback.
        """
        try:
            image = pygame.image.load(path).convert_alpha()
            return image
        except Exception as e:
            print(f"[DEBUG] ERROR: could not load image at '{path}': {e}")
            fallback = pygame.Surface(fallback_size, pygame.SRCALPHA)
            fallback.fill(Color.BLACK.value)
            return fallback
