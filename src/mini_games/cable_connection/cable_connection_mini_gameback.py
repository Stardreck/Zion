from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

import pygame
import pymunk

from src.mini_games.mini_game import MiniGame

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class CableConnectionMiniGame(MiniGame):
    """
    Cable Connection Mini-Game:
    In this mini-game, the player must connect matching colored cables on a switchboard.
    When all cables are correctly connected, the door (panel) opens.
    """

    def start(self):
        pass

    def __init__(self, game: StoryGame):
        """
        Initialize the Cable Connection mini-game.

        :param game: The main StoryGame instance.
        """
        # Initialize the base mini-game class
        super().__init__(game)

        # Initialize the physics simulation space using Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, -981)  # Gravity in pixels per second^2

        # Initialize game state variables
        self.endpoints = []  # List of cable endpoints (each is a dict)
        self.connections = []  # List of connected endpoint pairs
        self.selected_endpoint = None  # Currently selected endpoint (for dragging)
        self.drag_line = None  # Current drag line (from selected endpoint to cursor)
        self.door_open = False  # True when the door (panel) is open (win condition)
        self.finished = False  # True when the mini-game is finished

        # Define the switchboard (panel) area as a square on the right side of the screen
        panel_size = 250  # The square's width and height
        margin_right = 50  # Margin from the right edge
        window_width = self.game.window.get_width()
        window_height = self.game.window.get_height()
        self.board_rect = pygame.Rect(
            window_width - panel_size - margin_right,
            (window_height - panel_size) // 2,
            panel_size,
            panel_size
        )

        door_images = [
            "assets/images/spaceship/door/spaceship_door_01.png",
        ]
        background_path = random.choice(door_images)
        self.background_image = pygame.image.load(background_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, self.game.window.get_size())
        # Choose a random panel background image from available options
        panel_images = [
            "assets/images/spaceship/panel/spaceship_panel_01.png",
            "assets/images/spaceship/panel/spaceship_panel_02.png"
        ]
        panel_path = random.choice(panel_images)
        self.panel_image = pygame.image.load(panel_path).convert()
        self.panel_image = pygame.transform.scale(self.panel_image, self.game.window.get_size())

        # Set up the font for drawing text (e.g. door status)
        self.font = pygame.font.SysFont(None, 36)

        # Initialize cable endpoints based on the board_rect
        self.__init_endpoints()

    def __init_endpoints(self) -> None:
        """
        Initialize cable endpoints with fixed positions and matching colors inside the switchboard area.
        """
        # Calculate positions relative to the board_rect
        x0, y0, width, height = self.board_rect
        endpoint_positions = [
            (x0 + width * 0.25, y0 + height * 0.25),
            (x0 + width * 0.75, y0 + height * 0.25),
            (x0 + width * 0.25, y0 + height * 0.75),
            (x0 + width * 0.75, y0 + height * 0.75)
        ]
        # Two red endpoints and two green endpoints
        endpoint_colors = [(255, 0, 0), (255, 0, 0), (0, 255, 0), (0, 255, 0)]
        for pos, color in zip(endpoint_positions, endpoint_colors):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Circle(body, 20)
            shape.sensor = True  # Sensor: does not affect physical collisions
            self.space.add(body, shape)
            self.endpoints.append({
                'body': body,
                'shape': shape,
                'color': color,
                'connected': False,
                'connection': None
            })

    def update(self, delta_time: float) -> None:
        """
        Update the physics simulation and check if all cable endpoints are connected.

        :param delta_time: Time elapsed since the last frame.
        """
        self.space.step(delta_time)
        # If all endpoints are connected, mark the door as open and finish the game.
        if all(ep['connected'] for ep in self.endpoints):
            self.door_open = True
            self.finished = True

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Process touch/mouse events for selecting and connecting cable endpoints.

        :param event: A pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Check if the touch is near any unconnected endpoint
            for ep in self.endpoints:
                if not ep['connected']:
                    bx, by = ep['body'].position
                    if math.hypot(pos[0] - bx, pos[1] - by) < 25:
                        self.selected_endpoint = ep
                        break
        elif event.type == pygame.MOUSEMOTION:
            if self.selected_endpoint:
                self.drag_line = (self.selected_endpoint['body'].position, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected_endpoint:
                pos = event.pos
                target_endpoint = None
                # Look for a matching, unconnected endpoint near the release position
                for ep in self.endpoints:
                    if (ep is not self.selected_endpoint and not ep['connected'] and
                            ep['color'] == self.selected_endpoint['color']):
                        bx, by = ep['body'].position
                        if math.hypot(pos[0] - bx, pos[1] - by) < 25:
                            target_endpoint = ep
                            break
                if target_endpoint:
                    # Mark both endpoints as connected and record the connection
                    self.selected_endpoint['connected'] = True
                    target_endpoint['connected'] = True
                    self.selected_endpoint['connection'] = target_endpoint
                    target_endpoint['connection'] = self.selected_endpoint
                    self.connections.append((self.selected_endpoint, target_endpoint))
                # Reset selection and drag line
                self.selected_endpoint = None
                self.drag_line = None

    def draw(self) -> None:
        """
        Draw the mini-game elements, including background, switchboard area, cable endpoints,
        connection lines, drag line, and door status text.
        """
        # Draw the full-screen background image
        self.game.window.blit(self.background_image, (0, 0))
        # Draw the switchboard area as a square on the right side
        pygame.draw.rect(self.game.window, (60, 60, 60), self.board_rect)
        self.game.window.blit(self.panel_image, self.board_rect)
        # Draw each cable endpoint as a circle
        for ep in self.endpoints:
            pos = ep['body'].position
            pygame.draw.circle(self.game.window, ep['color'], (int(pos.x), int(pos.y)), 20)
        # Draw connection lines between connected endpoints
        for ep1, ep2 in self.connections:
            pos1 = ep1['body'].position
            pos2 = ep2['body'].position
            pygame.draw.line(
                self.game.window,
                ep1['color'],
                (int(pos1.x), int(pos1.y)),
                (int(pos2.x), int(pos2.y)),
                8
            )
        # Draw the drag line if a cable is being dragged
        if self.drag_line and self.selected_endpoint:
            start, end = self.drag_line
            pygame.draw.line(
                self.game.window,
                self.selected_endpoint['color'],
                (int(start.x), int(start.y)),
                end,
                4
            )
        # Render door status text at the bottom center of the screen
        status_text = "Door Open!" if self.door_open else "Door Closed"
        text_surface = self.font.render(status_text, True, (255, 255, 255))
        text_x = self.game.window.get_width() // 2 - text_surface.get_width() // 2
        text_y = self.game.window.get_height() - 50
        self.game.window.blit(text_surface, (text_x, text_y))

    def is_finished(self) -> bool:
        """
        Return True if the mini-game is finished.

        :return: True if finished; otherwise, False.
        """
        return self.finished

    def get_result(self) -> bool:
        """
        Return the result of the mini-game (True if the door is open).

        :return: True if win; otherwise, False.
        """
        return self.door_open

    def run(self) -> None:
        """
        Run the mini-game loop until the mini-game is finished.
        """
        clock = pygame.time.Clock()
        running = True
        while running:
            delta_time = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.game.stop()
                self.handle_event(event)
            self.update(delta_time)
            self.draw()
            pygame.display.flip()
            if self.is_finished():
                running = False
