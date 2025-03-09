from __future__ import annotations

import math
import random
from typing import List, Tuple, Optional, TYPE_CHECKING

import pygame
import pygame_gui
import pymunk
from pygame import Rect
from pygame_gui.elements import UIImage

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.mini_games.mini_game import MiniGame
from src.models.mini_games.cable_connection.endpoint import Endpoint

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class CableConnectionMiniGame(MiniGame):
    """
    Cable Connection Mini-Game:
    The player can connect endpoints regardless of color.
    However, the game is only won (door_open = True) if all connections are correct,
    meaning that the connected endpoints share the same color.
    Clicking on a connected endpoint will remove its connection.
    """

    def __init__(self, game: StoryGame, num_pairs: int = 8):
        super().__init__(game)
        self.space: pymunk.Space = pymunk.Space()
        self.space.gravity = (0, -981)  # Gravity in pixels per second^2

        self.num_pairs: int = num_pairs  # Total cable pairs (max 8 - 16 endpoints)
        # Now each connection is stored as a tuple: (endpoint1, endpoint2, is_correct)
        self.connections: List[Tuple[Endpoint, Endpoint, bool]] = []
        self.endpoints: List[Endpoint] = []
        self.selected_endpoint: Optional[Endpoint] = None
        self.drag_line: Optional[Tuple[pymunk.Vec2d, Tuple[int, int]]] = None
        self.door_open: bool = False
        self.is_running: bool = False

        # Instance variables for grid settings (instead of global/class-level constants)
        self.grid_columns: int = 4
        self.grid_rows: int = 4
        self.endpoint_connection_threshold: int = 25  # Pixel distance to consider an endpoint "selected"
        self.endpoint_draw_radius: int = 12
        self.connection_line_width: int = 8
        self.drag_line_width: int = 4

        # Instance variables for switchboard area relative to the panel image
        self.switchboard_x_offset: int = 150
        self.switchboard_y_offset: int = 90
        self.switchboard_width: int = 200
        self.switchboard_height: int = 300

        data = self.load_config_file_data()
        config = data.get("CableConnectionMiniGame", {})
        # Load images
        door_image_paths: List[str] = config.get("backgrounds")
        panel_image_paths: List[str] = config.get("panel_images")
        chosen_door_image: str = random.choice(door_image_paths)
        self.background_image: pygame.Surface = pygame.image.load(chosen_door_image).convert()
        chosen_panel_image: str = random.choice(panel_image_paths)
        self.panel_image_surface: pygame.Surface = pygame.image.load(chosen_panel_image).convert()

        # UI elements
        self.title: Optional[UILabel] = None
        self.background_panel: Optional[UIPanel] = None
        self.inner_panel: Optional[UIPanel] = None
        self.panel_image: Optional[UIImage] = None
        self.close_button: Optional[UIButton] = None  # Button to exit or close the mini-game

    def _build_ui(self) -> None:
        """Construct the UI components for the mini-game."""
        self.background_panel = UIPanel(
            relative_rect=Rect(-565, 0, 550, 550),
            manager=self.game.ui_manager.gui_manager,
            anchors={"right": "right", "centery": "centery"},
            object_id="default_panel_transparent",
        )
        title_rect = Rect(0, 60, 800, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text="geschlossen",
            manager=self.game.ui_manager.gui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="planet_menu_title",
        )
        self.inner_panel = UIPanel(
            relative_rect=Rect(0, 10, 530, 530),
            manager=self.game.ui_manager.gui_manager,
            container=self.background_panel,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="default_panel",
        )
        self.panel_image = UIImage(
            relative_rect=Rect(10, 10, 510, 510),
            image_surface=self.panel_image_surface,
            manager=self.game.ui_manager.gui_manager,
            container=self.inner_panel,
            anchors={"left": "left"},
        )
        close_button_rect: Rect = Rect(0, -60, 500, 50)
        self.close_button = UIButton(
            relative_rect=close_button_rect,
            text="Aufgeben",
            manager=self.game.ui_manager.gui_manager,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="",
        )
        # Bind the button press event to terminate the mini-game.
        self.close_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.kill())

    def _build_endpoints(self) -> None:
        """Generate cable endpoints within a defined grid area on the switchboard."""
        self.endpoints.clear()
        total_grid_cells: int = self.grid_columns * self.grid_rows
        total_endpoints: int = self.num_pairs * 2
        if total_endpoints > total_grid_cells:
            raise ValueError("Too many endpoints for the grid size (max 16 endpoints allowed)")

        # Determine the switchboard area relative to the panel image.
        panel_rect: Rect = self.panel_image.rect
        switchboard_origin_x: int = panel_rect.x + self.switchboard_x_offset
        switchboard_origin_y: int = panel_rect.y + self.switchboard_y_offset
        board_width: int = self.switchboard_width
        board_height: int = self.switchboard_height

        # Calculate center positions for grid cells within the switchboard area.
        cell_width: float = board_width / self.grid_columns
        cell_height: float = board_height / self.grid_rows
        grid_cell_centers: List[Tuple[float, float]] = [
            (
                switchboard_origin_x + col * cell_width + cell_width / 2,
                switchboard_origin_y + row * cell_height + cell_height / 2,
            )
            for row in range(self.grid_rows)
            for col in range(self.grid_columns)
        ]

        # Randomly select grid cell centers for placing endpoints and shuffle their order.
        selected_positions: List[Tuple[float, float]] = random.sample(grid_cell_centers, total_endpoints)
        random.shuffle(selected_positions)

        # Define available colors; if there are more pairs than colors, colors will be reused.
        available_colors: List[Tuple[int, int, int]] = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255),
        ]
        # Loop over each cable pair:
        # For each pair, select one color (the correct color) and assign two distinct grid positions (from the shuffled list).
        for pair_index in range(self.num_pairs):
            color: Tuple[int, int, int] = available_colors[pair_index % len(available_colors)]
            first_endpoint_pos: Tuple[float, float] = selected_positions[pair_index]
            second_endpoint_pos: Tuple[float, float] = selected_positions[pair_index + self.num_pairs]
            for position in (first_endpoint_pos, second_endpoint_pos):
                static_body: pymunk.Body = pymunk.Body(body_type=pymunk.Body.STATIC)
                static_body.position = position
                circle_shape: pymunk.Circle = pymunk.Circle(static_body, 15)
                circle_shape.sensor = True
                self.space.add(static_body, circle_shape)
                endpoint: Endpoint = Endpoint(
                    body=static_body,
                    shape=circle_shape,
                    color=color,  # This is the correct color for the connection.
                    connected=False,
                    connection=None,
                )
                self.endpoints.append(endpoint)

    def show_start_menu(self) -> None:
        """Display the start menu (not implemented)."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process input events."""
        if event.type == pygame.QUIT:
            self.game.stop()
            self.is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            self.game.debug_manager.toggle_debug_mode()

        self.game.ui_manager.gui_manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_button_down(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_button_up(event)

    def _handle_mouse_button_down(self, event: pygame.event.Event) -> None:
        """
        Handle mouse button down events.
        - If the click is within a threshold distance (using math.hypot) of an endpoint:
          - If the endpoint is already connected, remove its connection.
          - Otherwise, select the endpoint for initiating a new connection.
        math.hypot calculates the Euclidean distance between two points.
        """
        mouse_position: Tuple[int, int] = event.pos
        for endpoint in self.endpoints:
            endpoint_position = endpoint.body.position
            distance: float = math.hypot(
                mouse_position[0] - endpoint_position.x,
                mouse_position[1] - endpoint_position.y
            )
            if distance < self.endpoint_connection_threshold:
                if endpoint.connected:
                    self._remove_connection(endpoint)
                else:
                    self.selected_endpoint = endpoint
                break

    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Update the drag line as the mouse moves, showing a visual connection from the selected endpoint to the cursor."""
        if self.selected_endpoint:
            self.drag_line = (self.selected_endpoint.body.position, event.pos)

    def _handle_mouse_button_up(self, event: pygame.event.Event) -> None:
        """
        Handle mouse button release events.
        When the mouse button is released:
        - Check if the release position is close enough to an unconnected endpoint.
        - If so, establish a connection between the selected endpoint and the target endpoint,
          regardless of color.
        - Determine if the connection is correct by comparing endpoint colors.
        - After connecting, verify the win condition.
        math.hypot is used here to compute the distance between the release point and potential endpoints.
        """
        if not self.selected_endpoint:
            return

        mouse_position: Tuple[int, int] = event.pos
        target_endpoint: Optional[Endpoint] = None
        for endpoint in self.endpoints:
            if endpoint is not self.selected_endpoint and not endpoint.connected:
                endpoint_position = endpoint.body.position
                if math.hypot(
                        mouse_position[0] - endpoint_position.x,
                        mouse_position[1] - endpoint_position.y
                ) < self.endpoint_connection_threshold:
                    target_endpoint = endpoint
                    break

        if target_endpoint:
            # Allow connection even if colors do not match.
            self.selected_endpoint.connected = True
            target_endpoint.connected = True
            self.selected_endpoint.connection = target_endpoint
            target_endpoint.connection = self.selected_endpoint
            # Determine if the connection is correct (i.e., both endpoints have the same color)
            is_correct: bool = self.selected_endpoint.color == target_endpoint.color
            self.connections.append((self.selected_endpoint, target_endpoint, is_correct))
            self._check_win_condition()

        self.selected_endpoint = None
        self.drag_line = None

    def _remove_connection(self, endpoint: Endpoint) -> None:
        """
        Remove the connection associated with the given endpoint.
        Resets both endpoints involved in the connection and updates the win condition.
        """
        partner_endpoint = endpoint.connection
        if partner_endpoint:
            # Remove the connection tuple from the connections list
            for conn in self.connections:
                if endpoint in (conn[0], conn[1]):
                    self.connections.remove(conn)
                    break
            # Reset connection state for both endpoints
            endpoint.connected = False
            endpoint.connection = None
            partner_endpoint.connected = False
            partner_endpoint.connection = None
            self._check_win_condition()

    def _check_win_condition(self) -> None:
        """
        Check if all cable pairs are correctly connected.
        The game is won (door_open = True) only if:
          - All endpoints are connected (number of connections equals the number of pairs), and
          - Every connection is correct (i.e. endpoints share the same color).
        If the win condition is met, print "open" to the console and update the close button text.
        """
        if len(self.connections) == self.num_pairs and all(conn[2] for conn in self.connections):
            if not self.door_open:
                self.door_open = True
                print("open")
                self.title.set_text("geöffnet")
                self.close_button.set_text("Zurück")
        else:
            self.door_open = False
            self.title.set_text("geschlossen")
            self.close_button.set_text("Aufgeben")

    def update(self, delta_time: float) -> None:
        """Advance the physics simulation."""
        self.space.step(delta_time)

    def draw(self) -> None:
        """Render the game elements on the window."""
        self.game.window.blit(self.background_image, (0, 0))
        self.game.ui_manager.gui_manager.draw_ui(self.game.window)

        # Draw each endpoint as a circle
        for endpoint in self.endpoints:
            position = endpoint.body.position
            pygame.draw.circle(
                self.game.window,
                endpoint.color,
                (int(position.x), int(position.y)),
                self.endpoint_draw_radius,
            )

        # Draw lines connecting endpoints that have been connected.
        # The connection tuple now contains a third element indicating correctness.
        for first_endpoint, second_endpoint, _ in self.connections:
            pos1 = first_endpoint.body.position
            pos2 = second_endpoint.body.position
            pygame.draw.line(
                self.game.window,
                first_endpoint.color,
                (int(pos1.x), int(pos1.y)),
                (int(pos2.x), int(pos2.y)),
                self.connection_line_width,
            )

        # Draw the current drag line if a connection is in progress.
        if self.drag_line and self.selected_endpoint:
            start_position, current_mouse_position = self.drag_line
            pygame.draw.line(
                self.game.window,
                self.selected_endpoint.color,
                (int(start_position.x), int(start_position.y)),
                current_mouse_position,
                self.drag_line_width,
            )

    def is_finished(self) -> bool:
        """Return True if the mini-game is finished."""
        return self.finished

    def get_result(self) -> bool:
        """Return the result of the mini-game (door open state)."""
        return self.door_open

    def run(self) -> None:
        """Main loop for the mini-game."""
        self._build_ui()
        self._build_endpoints()
        clock: pygame.time.Clock = pygame.time.Clock()
        self.is_running = True

        while self.is_running:
            time_elapsed: float = clock.tick(self.game.engine.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.game.ui_manager.gui_manager.update(time_elapsed)
            self.draw()
            pygame.display.update()

        self.kill()

    def kill(self) -> None:
        """Clean up UI components and terminate the mini-game."""
        self.is_running = False
        if self.title:
            self.title.kill()
        if self.inner_panel:
            self.inner_panel.kill()
        if self.background_panel:
            self.background_panel.kill()
        if self.panel_image:
            self.panel_image.kill()
        if self.close_button:
            self.close_button.kill()
