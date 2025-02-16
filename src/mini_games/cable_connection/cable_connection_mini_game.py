from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, List, Tuple, Optional

import pygame
import pymunk
from pygame import Rect
from pygame_gui.elements import UIImage

from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.mini_games.mini_game import MiniGame
from src.models.mini_games.cable_connection.endpoint import Endpoint

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class CableConnectionMiniGame(MiniGame):
    """
    Cable Connection Mini-Game:
    In this mini-game, the player must connect matching colored cables on a switchboard.
    When all cables are correctly connected, the door opens (well sadly not really but the text will indicate it)
    """

    def __init__(self, game: StoryGame):
        """
        Initialize the Cable Connection mini-game.
        """
        super().__init__(game)

        ##### Initialize the physics simulation space using Pymunk #####
        self.space = pymunk.Space()
        self.space.gravity = (0, -981)  # Gravity in pixels per second^2

        ##### Initialize game state variables #####
        self.num_pairs: int = 8  # Number of cable pairs; total endpoints = num_pairs * 2
        self.endpoints: List[Endpoint] = []  # List of cable endpoints (each is a dict)
        self.connections: List[Tuple[Endpoint, Endpoint]] = []  # List of connected endpoint pairs
        self.selected_endpoint: Optional[Endpoint] = None  # Currently selected endpoint (for dragging)
        self.drag_line: Optional[
            Tuple[pymunk.Vec2d, Tuple[int, int]]] = None  # Current drag line (from selected endpoint to cursor)
        self.door_open: bool = False  # True when the door (panel) is open (win condition)
        self.is_running: bool = False  # True when the mini-game is finished

        ##### backgrounds #####
        door_paths = [
            "assets/images/spaceship/door/spaceship_door_01.png",
            "assets/images/spaceship/door/spaceship_door_02.png",
            "assets/images/spaceship/door/spaceship_door_03.png",
            "assets/images/spaceship/door/spaceship_door_04.png",
        ]
        door_path = random.choice(door_paths)
        self.background_image_surface = pygame.image.load(door_path).convert()

        panel_paths = [
            "assets/images/spaceship/panel/spaceship_panel_01.png",
            "assets/images/spaceship/panel/spaceship_panel_02.png",
            "assets/images/spaceship/panel/spaceship_panel_03.png",
            "assets/images/spaceship/panel/spaceship_panel_04.png",
        ]
        self.panel_path = random.choice(panel_paths)
        self.panel_image_surface = pygame.image.load(self.panel_path).convert()

        ##### panel options #####

        ##### UI elements #####
        self.title: UILabel | None = None
        self.panel_bg: UIPanel | None = None
        self.panel: UIPanel | None = None
        self.panel_image: UIImage | None = None

    def __build_ui(self):
        # Create the background panel (transparent)
        self.panel_bg = UIPanel(
            relative_rect=Rect(-565, 0, 550, 550),
            manager=self.game.ui_manager.gui_manager,
            anchors={"right": "right", "centery": "centery"},
            object_id="default_panel_transparent",
        )

        # Create the inner panel
        self.panel = UIPanel(
            relative_rect=Rect(0, 10, 530, 530),
            manager=self.game.ui_manager.gui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="default_panel",
        )

        self.panel_image = UIImage(
            relative_rect=Rect(10, 10, 510, 510),
            image_surface=self.panel_image_surface,
            manager=self.game.ui_manager.gui_manager,
            container=self.panel,
            anchors={"left": "left"},
        )

    def __build_endpoints(self) -> None:
        """
        Build endpoints dynamically on a grid.
        The grid is 4 columns by 4 rows. Randomly choose 2*num_pairs cells and assign pairs.
        """
        self.endpoints.clear()
        grid_cols = 4
        grid_rows = 4
        total_cells = grid_cols * grid_rows
        num_endpoints = self.num_pairs * 2
        if num_endpoints > total_cells:
            raise ValueError("Too many endpoints for the grid size (max 16 endpoints allowed)")

        # Get the rectangle of the panel_image (which is drawn in the switchboard area)
        x0, y0, width, height = self.panel_image.rect
        x0 += 150
        y0 += 90
        width = 200
        height = 300

        # Calculate cell centers
        cell_width = width / grid_cols
        cell_height = height / grid_rows
        grid_positions = [
            (x0 + col * cell_width + cell_width / 2, y0 + row * cell_height + cell_height / 2)
            for row in range(grid_rows) for col in range(grid_cols)
        ]
        # Randomly select cells for endpoints
        selected_positions = random.sample(grid_positions, num_endpoints)
        random.shuffle(selected_positions)

        # Define available colors (cycle if necessary)
        available_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                            (255, 0, 255), (0, 255, 255)]
        # For each pair, assign same color and create two endpoints
        for i in range(self.num_pairs):
            color = available_colors[i % len(available_colors)]
            pos1 = selected_positions[i]
            pos2 = selected_positions[i + self.num_pairs]
            for pos in (pos1, pos2):
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = pos
                shape = pymunk.Circle(body, 15)  # Reduced radius for tighter spacing
                shape.sensor = True
                self.space.add(body, shape)
                endpoint = Endpoint(body=body, shape=shape, color=color, connected=False, connection=None)
                self.endpoints.append(endpoint)



    def show_start_menu(self):
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Process touch/mouse events for selecting and connecting cable endpoints.

        :param event: A pygame event.
        """
        if event.type == pygame.QUIT:
            self.game.stop()
            self.is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.game.debug_manager.toggle_debug_mode()
        self.game.ui_manager.gui_manager.process_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Check if the touch is near any unconnected endpoint
            for endpoint in self.endpoints:
                if not endpoint.connected:
                    bx, by = endpoint.body.position
                    if math.hypot(pos[0] - bx, pos[1] - by) < 25:
                        self.selected_endpoint = endpoint
                        break
        elif event.type == pygame.MOUSEMOTION:
            if self.selected_endpoint:
                self.drag_line = (self.selected_endpoint.body.position, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected_endpoint:
                pos = event.pos
                target_endpoint = None
                # Look for a matching, unconnected endpoint near the release position
                for endpoint in self.endpoints:
                    if (endpoint is not self.selected_endpoint and not endpoint.connected and
                            endpoint.color == self.selected_endpoint.color):
                        bx, by = endpoint.body.position
                        if math.hypot(pos[0] - bx, pos[1] - by) < 25:
                            target_endpoint = endpoint
                            break
                if target_endpoint:
                    # Mark both endpoints as connected and record the connection
                    self.selected_endpoint.connected = True
                    target_endpoint.connected = True
                    self.selected_endpoint.connection = target_endpoint
                    target_endpoint.connection = self.selected_endpoint
                    self.connections.append((self.selected_endpoint, target_endpoint))
                # Reset selection and drag line
                self.selected_endpoint = None
                self.drag_line = None

    def update(self, delta_time: float) -> None:
        """
        Update the physics simulation and check if all cable endpoints are connected.

        :param delta_time: Time elapsed since the last frame.
        """
        self.space.step(delta_time)

    def draw(self) -> None:
        # Draw the background image covering the window
        self.game.window.blit(self.background_image_surface, (0, 0))
        self.game.ui_manager.gui_manager.draw_ui(self.game.window)

        # Draw each endpoint as a circle
        for ep in self.endpoints:
            pos = ep.body.position
            pygame.draw.circle(self.game.window, ep.color, (int(pos.x), int(pos.y)), 12)
        # Draw connection lines
        for ep1, ep2 in self.connections:
            pos1 = ep1.body.position
            pos2 = ep2.body.position
            pygame.draw.line(self.game.window, ep1.color, (int(pos1.x), int(pos1.y)), (int(pos2.x), int(pos2.y)), 8)
        # Draw drag line if dragging
        if self.drag_line and self.selected_endpoint:
            start, end = self.drag_line
            pygame.draw.line(self.game.window, self.selected_endpoint.color, (int(start.x), int(start.y)), end, 4)

    def is_finished(self) -> bool:
        return self.finished

    def get_result(self) -> bool:
        return self.door_open

    def run(self) -> None:
        self.__build_ui()
        self.__build_endpoints()
        clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:

            time_delta = clock.tick(self.game.engine.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.game.ui_manager.gui_manager.update(time_delta)
            self.draw()
            pygame.display.update()
        self.kill()

    def kill(self):
        self.is_running = False
        if self.panel:
            self.panel.kill()
        if self.panel_bg:
            self.panel_bg.kill()
        if self.panel_image:
            self.panel_image.kill()
