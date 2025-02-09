from __future__ import annotations

import math
import pygame

from pygame_gui.elements import UIWindow, UIImage, UILabel
from typing import List, Optional, Tuple, TYPE_CHECKING

from src.enums.color import Color
from src.managers.manager import Manager

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class DebugManager(Manager):
    """
    Implements a debug view using pygame_gui elements exclusively.
    The UI is split into two windows:
      1. Debug Information Window – shows textual debug data.
      2. Solar System Window – displays the solar system background (scaled without stretching)
         with a hexagon grid overlay, and overlays green circles for planets and a red circle for the player.
    """

    def __init__(self, game: StoryGame):
        """
        Initialize the DebugManager.

        :param game: The main game instance which provides game data and a reference to the UI manager.
        """
        super().__init__()
        self.game = game
        self.debug_mode = False

        ##### Hexagon grid configuration #####
        self.hex_rows = 11
        self.hex_columns = 11
        self.hexagon_radius = 25
        # Offsets to position the hex grid within the solar system window
        self.hexagon_offset_x = 140
        self.hexagon_offset_y = 80

        self.__init()

        ##### Hide both windows initially #####
        self.debug_info_window.hide()
        self.solar_system_window.hide()

    def __init(self):
        ##### Create the Debug Information Window #####
        self.debug_info_window: UIWindow = UIWindow(
            rect=pygame.Rect(900, 50, 400, 300),
            manager=self.game.ui_manager.gui_manager,
            window_display_title="Debug Information"
        )
        # List to hold UILabel elements for debug text
        self.debug_info_labels: List[UILabel] = []
        self.__create_debug_info_ui()

        ##### Create the Solar System Window #####
        self.solar_system_window: UIWindow = UIWindow(
            rect=pygame.Rect(50, 50, 800, 600),
            manager=self.game.ui_manager.gui_manager,
            window_display_title="Solar System"
        )
        # Load the solar system background image (with fallback if loading fails)
        raw_solar_system_image: pygame.Surface = self.__load_image(
            "assets/images/solar_system.png", fallback_size=(800, 600)
        )
        # Scale the solar system image so that it fits within the target size without stretching
        self.solar_system_background: pygame.Surface = self.__scale_image_preserving_aspect_ratio(
            raw_solar_system_image, target_size=(800, 600)
        )
        # Create a UI element for the solar system background
        self.solar_system_background_ui = UIImage(
            relative_rect=pygame.Rect(0, 0, 800, 600),
            image_surface=self.solar_system_background,
            manager=self.game.ui_manager.gui_manager,
            container=self.solar_system_window
        )

        ##### Create the Hexagon Grid UI Elements #####
        self.hexagon_ui_elements: List[UIImage] = []
        self.__create_hex_grid_ui_elements()

        ##### Prepare UI elements for Planets and the Player #####
        # Create a surface for the green planet circle (30-pixel diameter)
        self.planet_circle_diameter = 30
        self.planet_circle_surface: pygame.Surface = self.__create_circle_surface(
            diameter=self.planet_circle_diameter, color=Color.DEBUG_PLANET.value
        )
        # This list will hold UI elements for planets (created dynamically in update)
        self.planet_ui_elements: List[UIImage] = []

        # Create a surface for the red player circle (24-pixel diameter)
        self.player_circle_diameter = 24
        self.player_circle_surface: pygame.Surface = self.__create_circle_surface(
            diameter=self.player_circle_diameter, color=Color.DEBUG_PLAYER.value
        )
        # Create the player UI element (position will be updated in update())
        self.player_ui: UIImage = UIImage(
            relative_rect=pygame.Rect(0, 0, self.player_circle_diameter, self.player_circle_diameter),
            image_surface=self.player_circle_surface,
            manager=self.game.ui_manager.gui_manager,
            container=self.solar_system_window
        )

    def toggle_debug_mode(self):
        """
        Toggle the debug mode on or off.
        When enabled, both the Debug Information and Solar System windows are shown.
        """
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.debug_info_window.show()
            self.solar_system_window.show()
        else:
            self.debug_info_window.hide()
            self.solar_system_window.hide()
        print(f"[DEBUG] Debug mode: {self.debug_mode}")

    def update(self, delta_time: float):
        """
        Update the debug UI elements to reflect the current game state.
        This method should be called each frame in the main game loop.

        :param delta_time: Time elapsed since the last frame.
        """
        if not self.debug_mode:
            return

        ##### Update Planet UI Elements #####
        # Remove previous planet UI elements.
        for planet_ui in self.planet_ui_elements:
            planet_ui.kill()  # Remove from the UI manager
        self.planet_ui_elements.clear()

        # Create a new UI element for each planet in the game.
        for planet in self.game.data.planets:
            # Compute the center position for the hex cell corresponding to the planet's row and column.
            center_x, center_y = self.__calculate_hex_center(planet.row, planet.col)
            planet_rect = pygame.Rect(
                int(center_x - self.planet_circle_diameter / 2),
                int(center_y - self.planet_circle_diameter / 2),
                self.planet_circle_diameter,
                self.planet_circle_diameter
            )
            planet_ui = UIImage(
                relative_rect=planet_rect,
                image_surface=self.planet_circle_surface,
                manager=self.game.ui_manager.gui_manager,
                container=self.solar_system_window
            )
            self.planet_ui_elements.append(planet_ui)

        ##### Update Player UI Element Position #####
        player_center_x, player_center_y = self.__calculate_hex_center(
            self.game.player_row, self.game.player_col
        )
        self.player_ui.set_relative_position((
            int(player_center_x - self.player_circle_diameter / 2),
            int(player_center_y - self.player_circle_diameter / 2)
        ))

        ##### Update Debug Information Text #####
        general_info = [
            "Debug Mode [D]",
            f"Fuel: {self.game.fuel}",
            f"Hull: {self.game.hull}",
            f"Player Position: (row={self.game.player_row}, col={self.game.player_col})",
            f"Current Planet: {self.game.current_planet.name if self.game.current_planet else 'None'}"
        ]
        event_info = [
            "Event Manager:",
        ]
        game_stats_info = [
            "Game Stats:",
        ]
        # Combine all lines of debug text
        debug_text_lines = general_info + event_info + game_stats_info

        # Update each UILabel in the Debug Information window.
        for index, label in enumerate(self.debug_info_labels):
            if index < len(debug_text_lines):
                label.set_text(debug_text_lines[index])
            else:
                label.set_text("")

    def __create_debug_info_ui(self):
        """
        Create UILabel elements inside the Debug Information window.
        These labels display debug data.
        """
        self.debug_info_labels.clear()
        label_width = 350
        label_height = 25
        padding = 5
        starting_y = 10

        # Create 10 labels arranged in (up to) two columns.
        for index in range(10):
            column_index = index // 5  # Two columns (5 labels per column)
            row_index = index % 5
            x_position = 10 + column_index * (label_width + padding)
            y_position = starting_y + row_index * (label_height + padding)
            label = UILabel(
                relative_rect=pygame.Rect(x_position, y_position, label_width, label_height),
                text="",
                manager=self.game.ui_manager.gui_manager,
                container=self.debug_info_window
            )
            self.debug_info_labels.append(label)

    def __create_hex_grid_ui_elements(self):
        """
        Create UI elements for the hexagon grid.
        Each hexagon is drawn on a generated surface and then displayed via an UIImage.
        The hex grid is placed on top of the solar system background.
        """
        # Remove any existing hexagon UI elements.
        for hexagon_ui in self.hexagon_ui_elements:
            hexagon_ui.kill()
        self.hexagon_ui_elements.clear()

        # The hexagon's diameter is twice its radius.
        hexagon_diameter = self.hexagon_radius * 2
        # Create a hexagon surface with a transparent background and a white border.
        hexagon_surface = self.__create_hexagon_surface(
            diameter=hexagon_diameter,
            border_color=Color.WHITE.value,
            fill_color=None  # No fill; just a border overlay
        )

        # Loop over each row and column in the grid.
        for grid_row in range(self.hex_rows):
            for grid_column in range(self.hex_columns):
                center_x, center_y = self.__calculate_hex_center(grid_row, grid_column)
                hexagon_rect = pygame.Rect(
                    int(center_x - self.hexagon_radius),
                    int(center_y - self.hexagon_radius),
                    hexagon_diameter,
                    hexagon_diameter
                )
                hexagon_ui = UIImage(
                    relative_rect=hexagon_rect,
                    image_surface=hexagon_surface,
                    manager=self.game.ui_manager.gui_manager,
                    container=self.solar_system_window
                )
                self.hexagon_ui_elements.append(hexagon_ui)

    def __calculate_hex_center(self, grid_row: int, grid_column: int) -> Tuple[float, float]:
        """
        Calculate the center coordinates of a hexagon cell based on its row and column in the grid.

        :param grid_row: The row index in the hex grid.
        :param grid_column: The column index in the hex grid.
        :return: A tuple (center_x, center_y) representing the center of the hex cell.
        """
        vertical_spacing = self.hexagon_radius * 1.5
        horizontal_spacing = math.sqrt(3) * self.hexagon_radius

        center_x = self.hexagon_offset_x + grid_column * horizontal_spacing
        # Offset every other row for a staggered grid layout.
        if grid_row % 2:
            center_x += horizontal_spacing / 2

        center_y = self.hexagon_offset_y + grid_row * vertical_spacing
        return center_x, center_y

    def __create_circle_surface(self, diameter: int, color: Tuple[int, int, int]) -> pygame.Surface:
        """
        Create a circular surface with a transparent background.

        :param diameter: The diameter of the circle.
        :param color: The color of the circle (RGB tuple).
        :return: A pygame.Surface containing the drawn circle.
        """
        circle_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center_position = (diameter // 2, diameter // 2)
        circle_radius = diameter // 2
        pygame.draw.circle(circle_surface, color, center_position, circle_radius)
        return circle_surface

    def __create_hexagon_surface(
            self, diameter: int, border_color: Tuple[int, int, int],
            fill_color: Optional[Tuple[int, int, int]] = None
    ) -> pygame.Surface:
        """
        Create a hexagon surface with a transparent background.
        The hexagon is drawn with a border and (optionally) a fill color.

        :param diameter: The diameter of the hexagon (distance across its bounding circle).
        :param border_color: The color of the hexagon border.
        :param fill_color: The fill color for the hexagon (if any).
        :return: A pygame.Surface containing the drawn hexagon.
        """
        hexagon_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center_point = (diameter / 2, diameter / 2)
        hexagon_radius = diameter / 2
        hexagon_points = []

        # Calculate the six points of the hexagon.
        for i in range(6):
            angle_rad = math.radians(60 * i - 30)
            point_x = center_point[0] + hexagon_radius * math.cos(angle_rad)
            point_y = center_point[1] + hexagon_radius * math.sin(angle_rad)
            hexagon_points.append((point_x, point_y))

        # Optionally fill the hexagon.
        if fill_color is not None:
            pygame.draw.polygon(hexagon_surface, fill_color, hexagon_points)
        # Draw the border of the hexagon.
        pygame.draw.polygon(hexagon_surface, border_color, hexagon_points, width=2)
        return hexagon_surface

    def __load_image(self, path: str, fallback_size: Tuple[int, int]) -> pygame.Surface:
        """
        Attempt to load an image from the specified path.
        If loading fails, return a fallback surface filled with black.

        :param path: The file path to the image asset.
        :param fallback_size: The size of the fallback surface.
        :return: A pygame.Surface with the loaded image or fallback.
        """
        try:
            image = pygame.image.load(path).convert_alpha()
            return image
        except Exception as error:
            print(f"[DEBUG] Could not load image at '{path}': {error}")
            fallback_surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
            fallback_surface.fill(Color.BLACK.value)
            return fallback_surface

    def __scale_image_preserving_aspect_ratio(
            self, image: pygame.Surface, target_size: Tuple[int, int]
    ) -> pygame.Surface:
        """
        Scale an image to fit within the target size while preserving its aspect ratio.
        The scaled image is then centered on a surface of the target size.

        :param image: The original pygame.Surface to scale.
        :param target_size: The (width, height) of the target area.
        :return: A new pygame.Surface with the scaled image centered.
        """
        target_width, target_height = target_size
        image_width, image_height = image.get_size()

        # Calculate scale factor to fit image inside target_size while preserving aspect ratio.
        scale_factor = min(target_width / image_width, target_height / image_height)
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)

        # Smoothly scale the image to the new dimensions.
        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))

        # Create a new surface with the target size and a transparent background.
        final_surface = pygame.Surface(target_size, pygame.SRCALPHA)
        final_surface.fill((0, 0, 0, 0))

        # Center the scaled image on the final surface.
        position_x = (target_width - new_width) // 2
        position_y = (target_height - new_height) // 2
        final_surface.blit(scaled_image, (position_x, position_y))

        return final_surface
