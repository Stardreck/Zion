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
from src.models.mini_games.cable_connection.endpoint import Endpoint  # Reusing Endpoint as a Magical Orb

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class MagicalOrbsConnectionMiniGame(MiniGame):
    """
    Connect Magical Orbs Mini-Game.
    Orbs drift in a sky area.
    Connect orbs with the same color.
    Orbs are drawn with a radial gradient and flicker.
    """

    def __init__(self, game: StoryGame, background: str, num_pairs: int = 8):
        super().__init__(game, background)
        # Create a physics space with no gravity.
        self.space: pymunk.Space = pymunk.Space()
        self.space.gravity = (0, 0)

        self.num_pairs: int = num_pairs  # Total orb pairs (max 32 pairs = 64 orbs).
        # Each connection is a tuple: (orb1, orb2, is_correct).
        self.connections: List[Tuple[Endpoint, Endpoint, bool]] = []
        self.stars: List[Endpoint] = []  # List of Magical Orbs.
        self.selected_star: Optional[Endpoint] = None
        self.drag_line: Optional[Tuple[pymunk.Vec2d, Tuple[int, int]]] = None
        self.convergence_completed: bool = False
        self.is_running: bool = False

        # Grid settings for orb placement.
        self.grid_columns: int = 8  # Allows up to 64 cells.
        self.grid_rows: int = 8
        self.star_connection_threshold: int = 25  # Pixel distance for orb selection.
        self.star_draw_radius: int = 12
        self.connection_line_width: int = 8
        self.drag_line_width: int = 4

        # Sky area settings relative to the panel.
        self.sky_x_offset: int = 20
        self.sky_y_offset: int = 20
        self.sky_width: int = 900
        self.sky_height: int = 350
        self.sky_rect: Optional[Rect] = None  # Set during orb creation.

        data = self.load_config_file_data()
        config = data.get("MagicalOrbsConnectionMiniGame", {})
        # Load a night sky background and a panel image.
        sky_background_paths: List[str] = config.get("backgrounds", [])
        panel_image_paths: List[str] = config.get("panel_images", [])
        chosen_sky_background: str = random.choice(sky_background_paths) if sky_background_paths else background
        self.background_image: pygame.Surface = pygame.image.load(chosen_sky_background).convert()
        chosen_panel_image: str = random.choice(panel_image_paths) if panel_image_paths else background
        self.panel_image_surface: pygame.Surface = pygame.image.load(chosen_panel_image).convert()

        # UI elements.
        self.title: Optional[UILabel] = None
        self.background_panel: Optional[UIPanel] = None
        self.close_button: Optional[UIButton] = None  # Button to exit the mini-game.

    def _build_ui(self) -> None:
        """Create UI components."""
        self.background_panel = UIPanel(
            relative_rect=Rect(0, 25, 1000, 450),
            manager=self.game.ui_manager.gui_manager,
            anchors={"center": "center"},
            object_id="panel_invisible",
        )
        title_rect = Rect(0, 60, 800, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text="Gefangen im Traum",
            manager=self.game.ui_manager.gui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="planet_menu_title",
        )
        close_button_rect: Rect = Rect(0, -60, 500, 50)
        self.close_button = UIButton(
            relative_rect=close_button_rect,
            text="Aufgeben",
            manager=self.game.ui_manager.gui_manager,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="",
        )
        # Bind button to exit the game.
        self.close_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.kill())

    def _build_stars(self) -> None:
        """Generate moving Magical Orbs in a grid area."""
        self.stars.clear()
        total_grid_cells: int = self.grid_columns * self.grid_rows
        total_stars: int = self.num_pairs * 2
        if total_stars > total_grid_cells:
            raise ValueError("Too many orbs for the grid size (max 64 orbs allowed)")

        # Set the sky area based on the background panel.
        panel_rect: Rect = self.background_panel.rect
        sky_origin_x: int = panel_rect.x + self.sky_x_offset
        sky_origin_y: int = panel_rect.y + self.sky_y_offset
        board_width: int = self.sky_width
        board_height: int = self.sky_height
        self.sky_rect = Rect(sky_origin_x, sky_origin_y, board_width, board_height)

        # Compute center positions for grid cells.
        cell_width: float = board_width / self.grid_columns
        cell_height: float = board_height / self.grid_rows
        grid_cell_centers: List[Tuple[float, float]] = [
            (
                sky_origin_x + col * cell_width + cell_width / 2,
                sky_origin_y + row * cell_height + cell_height / 2,
            )
            for row in range(self.grid_rows)
            for col in range(self.grid_columns)
        ]

        # Randomly select grid cell centers and shuffle.
        selected_positions: List[Tuple[float, float]] = random.sample(grid_cell_centers, total_stars)
        random.shuffle(selected_positions)

        # Define colors for orb groups.
        available_colors: List[Tuple[int, int, int]] = [
            (255, 255, 255),  # White
            (255, 215, 0),  # Gold
            (173, 216, 230),  # Light Blue
            (255, 182, 193),  # Light Pink
            (144, 238, 144),  # Light Green
            (221, 160, 221),  # Plum
            (255, 165, 0),  # Orange
            (240, 128, 128),  # Light Coral
            (147, 112, 219),  # Medium Purple
            (64, 224, 208),  # Turquoise
            (240, 230, 140),  # Khaki
            (135, 206, 235),  # Sky Blue
            (218, 112, 214),  # Orchid
            (250, 128, 114),  # Salmon
            (219, 112, 147),  # Pale Violet Red
            (255, 160, 122),  # Light Salmon
        ]
        # Create two orbs per pair.
        for pair_index in range(self.num_pairs):
            color: Tuple[int, int, int] = available_colors[pair_index % len(available_colors)]
            first_orb_pos: Tuple[float, float] = selected_positions[pair_index]
            second_orb_pos: Tuple[float, float] = selected_positions[pair_index + self.num_pairs]
            for position in (first_orb_pos, second_orb_pos):
                # Create a kinematic body for constant velocity.
                body: pymunk.Body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
                body.position = position
                body.velocity = pymunk.Vec2d(
                    random.uniform(-30, 30),
                    random.uniform(-30, 30)
                )
                circle_shape: pymunk.Circle = pymunk.Circle(body, 15)
                circle_shape.sensor = True
                self.space.add(body, circle_shape)
                orb: Endpoint = Endpoint(
                    body=body,
                    shape=circle_shape,
                    color=color,  # Orb group color.
                    connected=False,
                    connection=None,
                )
                # Add flicker properties.
                orb.intensity = random.uniform(0.8, 1.2)
                orb.intensity_direction = random.choice([-1, 1])
                orb.intensity_speed = random.uniform(0.2, 0.5)
                self.stars.append(orb)

    def _draw_star(self, star: Endpoint) -> None:
        """Draw a Magical Orb with a radial gradient."""
        pos = star.body.position
        radius = self.star_draw_radius
        star_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        steps = radius
        for i in range(steps, 0, -1):
            alpha = int(255 * (i / steps) ** 2 * star.intensity)
            alpha = max(0, min(alpha, 255))
            pygame.draw.circle(
                star_surface,
                (star.color[0], star.color[1], star.color[2], alpha),
                (radius, radius),
                i,
            )
        self.game.window.blit(star_surface, (int(pos.x) - radius, int(pos.y) - radius))

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
        If click is near an orb:
        Remove connection if orb is connected.
        Else, select the orb.
        """
        mouse_position: Tuple[int, int] = event.pos
        for star in self.stars:
            star_position = star.body.position
            distance: float = math.hypot(
                mouse_position[0] - star_position.x,
                mouse_position[1] - star_position.y
            )
            if distance < self.star_connection_threshold:
                if star.connected:
                    self._remove_connection(star)
                else:
                    self.selected_star = star
                break

    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Update the drag line while the mouse moves."""
        if self.selected_star:
            self.drag_line = (self.selected_star.body.position, event.pos)

    def _handle_mouse_button_up(self, event: pygame.event.Event) -> None:
        """
        On mouse release:
        Connect selected orb to a nearby unconnected orb.
        Check if the connection is correct.
        """
        if not self.selected_star:
            return

        mouse_position: Tuple[int, int] = event.pos
        target_star: Optional[Endpoint] = None
        for star in self.stars:
            if star is not self.selected_star and not star.connected:
                star_position = star.body.position
                if math.hypot(
                        mouse_position[0] - star_position.x,
                        mouse_position[1] - star_position.y
                ) < self.star_connection_threshold:
                    target_star = star
                    break

        if target_star:
            self.selected_star.connected = True
            target_star.connected = True
            self.selected_star.connection = target_star
            target_star.connection = self.selected_star
            is_correct: bool = self.selected_star.color == target_star.color
            self.connections.append((self.selected_star, target_star, is_correct))
            self._check_win_condition()

        self.selected_star = None
        self.drag_line = None

    def _remove_connection(self, star: Endpoint) -> None:
        """
        Remove the orb connection.
        Reset both orbs.
        """
        partner_star = star.connection
        if partner_star:
            for conn in self.connections:
                if star in (conn[0], conn[1]):
                    self.connections.remove(conn)
                    break
            star.connected = False
            star.connection = None
            partner_star.connected = False
            partner_star.connection = None
            self._check_win_condition()

    def _check_win_condition(self) -> None:
        """
        Check if all orb pairs are connected correctly.
        """
        if len(self.connections) == self.num_pairs and all(conn[2] for conn in self.connections):
            if not self.convergence_completed:
                self.convergence_completed = True
                self.title.set_text("Das Licht ruft!")
                self.close_button.set_text("Zurück")
        else:
            self.convergence_completed = False
            self.title.set_text("Gefangen im Traum")
            self.close_button.set_text("Aufgeben")

    def update(self, delta_time: float) -> None:
        """
        Step physics simulation.
        Update orb positions and flickering effect.
        """
        self.space.step(delta_time)
        if self.sky_rect:
            for star in self.stars:
                pos = star.body.position
                vel = star.body.velocity
                if pos.x < self.sky_rect.left and vel.x < 0:
                    star.body.velocity = pymunk.Vec2d(-vel.x, vel.y)
                elif pos.x > self.sky_rect.right and vel.x > 0:
                    star.body.velocity = pymunk.Vec2d(-vel.x, vel.y)
                if pos.y < self.sky_rect.top and vel.y < 0:
                    star.body.velocity = pymunk.Vec2d(vel.x, -vel.y)
                elif pos.y > self.sky_rect.bottom and vel.y > 0:
                    star.body.velocity = pymunk.Vec2d(vel.x, -vel.y)

        for star in self.stars:
            star.intensity += star.intensity_direction * star.intensity_speed * delta_time
            if star.intensity > 1.2:
                star.intensity = 1.2
                star.intensity_direction = -abs(star.intensity_direction)
            elif star.intensity < 0.8:
                star.intensity = 0.8
                star.intensity_direction = abs(star.intensity_direction)

    def draw(self) -> None:
        """Render the game elements."""
        self.game.window.blit(self.background_image, (0, 0))
        self.game.ui_manager.gui_manager.draw_ui(self.game.window)

        for star in self.stars:
            self._draw_star(star)

        for first_star, second_star, _ in self.connections:
            pos1 = first_star.body.position
            pos2 = second_star.body.position
            pygame.draw.line(
                self.game.window,
                first_star.color,
                (int(pos1.x), int(pos1.y)),
                (int(pos2.x), int(pos2.y)),
                self.connection_line_width,
            )

        if self.drag_line and self.selected_star:
            start_position, current_mouse_position = self.drag_line
            pygame.draw.line(
                self.game.window,
                self.selected_star.color,
                (int(start_position.x), int(start_position.y)),
                current_mouse_position,
                self.drag_line_width,
            )

    def is_finished(self) -> bool:
        """Return True if the game is finished."""
        return self.finished

    def get_result(self) -> bool:
        """Return the game result."""
        return self.convergence_completed

    def run(self) -> None:
        """Main game loop."""
        self._build_ui()
        self._build_stars()
        clock: pygame.time.Clock = pygame.time.Clock()
        self.is_running = True

        while self.is_running:
            time_elapsed: float = clock.tick(self.game.engine.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.game.ui_manager.gui_manager.update(time_elapsed)
            self.update(time_elapsed)
            self.draw()
            pygame.display.update()

        self.kill()

    def kill(self) -> None:
        """Clean up UI components and exit the game."""
        self.is_running = False
        if self.title:
            self.title.kill()
        if self.background_panel:
            self.background_panel.kill()
        if self.close_button:
            self.close_button.kill()
