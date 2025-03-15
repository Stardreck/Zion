from __future__ import annotations

import random
import pygame
import pygame_gui
from pygame import Rect
from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.mini_games.mini_game import MiniGame


class AsteroidDodgeMiniGame(MiniGame):
    """
    Asteroid Dodge Mini-Game:
    The player controls a spaceship and must dodge falling asteroids.
    The mini-game lasts for a fixed duration; surviving until the end is a win.
    """

    def __init__(self, game, background_path: str, duration: float = 30.0):
        """
        Initialize the Asteroid Dodge mini-game.

        :param game: The main game instance.
        :param background_path: Path to the background image.
        :param duration: Game duration in seconds.
        """
        super().__init__(game, background_path)
        # Load the background image
        self.background_image: pygame.Surface = pygame.image.load(background_path).convert()
        # Game duration and timer variables
        self.duration: float = duration
        self.elapsed_time: float = 0.0
        self.finished: bool = False
        self.success: bool = False
        self.is_running: bool = False

        # Spaceship properties
        self.player_rect: pygame.Rect = pygame.Rect(0, 0, 50, 50)
        self.player_rect.center = (game.engine.width // 2, game.engine.height - 75)
        self.player_speed: int = 300  # pixels per second

        # Asteroid properties
        self.asteroids: list[pygame.Rect] = []
        self.asteroid_speed: int = 200  # falling speed in pixels per second
        self.asteroid_spawn_timer: float = 0.0
        self.asteroid_spawn_interval: float = 1.0  # seconds between spawns

        # UI elements (initialized in _build_ui)
        self.background_panel: UIPanel | None = None
        self.title: UILabel | None = None
        self.close_button: UIButton | None = None

    def _build_ui(self) -> None:
        """Construct the UI components for the mini-game."""
        self.background_panel = UIPanel(
            relative_rect=Rect(-150, 0, 300, 100),
            manager=self.game.ui_manager.gui_manager,
            anchors={"top": "top", "centerx": "centerx"},
            object_id="default_panel_transparent",
        )
        self.title = UILabel(
            relative_rect=Rect(0, 10, 300, 50),
            text="Asteroid Dodge",
            manager=self.game.ui_manager.gui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="game_title",
        )
        self.close_button = UIButton(
            relative_rect=Rect(0, -40, 200, 50),
            text="Quit",
            manager=self.game.ui_manager.gui_manager,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="quit_button",
        )
        # Bind the close button to terminate the mini-game.
        self.close_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.kill())

    def show_start_menu(self) -> None:
        """Display the start menu for the mini-game (implementation can be added if needed)."""
        pass

    def start(self) -> None:
        """Initialize or reset the mini-game state."""
        self.elapsed_time = 0.0
        self.asteroids.clear()
        self.finished = False
        self.success = False
        # Reset spaceship position to the center-bottom of the screen.
        self.player_rect.center = (self.game.engine.width // 2, self.game.engine.height - 75)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Process input events.
        - Handle quit events.
        - Process key presses for spaceship movement.
        - Forward events to the UI manager.
        """
        if event.type == pygame.QUIT:
            self.game.stop()
            self.is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            self.game.debug_manager.toggle_debug_mode()

        self.game.ui_manager.gui_manager.process_events(event)

        if event.type == pygame.KEYDOWN:
            # Move the spaceship based on arrow key presses.
            if event.key == pygame.K_LEFT:
                self.player_rect.x -= int(self.player_speed * 0.1)
            elif event.key == pygame.K_RIGHT:
                self.player_rect.x += int(self.player_speed * 0.1)
            elif event.key == pygame.K_UP:
                self.player_rect.y -= int(self.player_speed * 0.1)
            elif event.key == pygame.K_DOWN:
                self.player_rect.y += int(self.player_speed * 0.1)

            # Keep the spaceship within the screen boundaries.
            self.player_rect.clamp_ip(Rect(0, 0, self.game.engine.width, self.game.engine.height))

    def update(self, delta_time: float) -> None:
        """
        Update the mini-game state.
        - Increase elapsed time.
        - Spawn new asteroids at regular intervals.
        - Move asteroids downward.
        - Remove asteroids that have moved off-screen.
        - Check for collisions between the spaceship and asteroids.
        """
        self.elapsed_time += delta_time

        # End the game when the duration is reached.
        if self.elapsed_time >= self.duration:
            self.finished = True
            self.success = True
            return

        # Spawn asteroids at defined intervals.
        self.asteroid_spawn_timer += delta_time
        if self.asteroid_spawn_timer >= self.asteroid_spawn_interval:
            self.asteroid_spawn_timer -= self.asteroid_spawn_interval
            self.spawn_asteroid()

        # Update asteroid positions.
        for asteroid in self.asteroids:
            asteroid.y += int(self.asteroid_speed * delta_time)

        # Remove asteroids that have left the screen.
        self.asteroids = [
            asteroid for asteroid in self.asteroids if asteroid.y < self.game.engine.height
        ]

        # Check for collisions between the spaceship and asteroids.
        for asteroid in self.asteroids:
            if self.player_rect.colliderect(asteroid):
                self.finished = True
                self.success = False
                break

    def draw(self) -> None:
        """
        Render the mini-game elements.
        - Draw the background.
        - Draw UI components.
        - Draw the spaceship and asteroids.
        - Display the remaining time.
        """
        # Draw the background image.
        self.game.window.blit(self.background_image, (0, 0))
        # Render UI elements.
        self.game.ui_manager.gui_manager.draw_ui(self.game.window)

        # Draw the player's spaceship as a blue rectangle.
        pygame.draw.rect(self.game.window, (0, 0, 255), self.player_rect)
        # Draw each asteroid as a red ellipse.
        for asteroid in self.asteroids:
            pygame.draw.ellipse(self.game.window, (255, 0, 0), asteroid)
        # Display the remaining time.
        font = pygame.font.SysFont(None, 36)
        time_left = max(0, int(self.duration - self.elapsed_time))
        time_text = font.render(f"Zeit übrig: {time_left}", True, (255, 255, 255))
        self.game.window.blit(time_text, (150, 50))

    def spawn_asteroid(self) -> None:
        """
        Spawn a new asteroid at a random x position at the top of the screen.
        Asteroids are represented as rectangles with equal width and height.
        """
        asteroid_width = random.randint(20, 50)
        asteroid_height = asteroid_width  # Approximate circular shape.
        x_position = random.randint(0, self.game.engine.width - asteroid_width)
        asteroid_rect = pygame.Rect(x_position, -asteroid_height, asteroid_width, asteroid_height)
        self.asteroids.append(asteroid_rect)

    def is_finished(self) -> bool:
        """Return True if the mini-game is finished."""
        return self.finished

    def get_result(self) -> bool:
        """Return True if the player survived the mini-game (win), otherwise False."""
        return self.success

    def run(self) -> None:
        """
        Main loop for the mini-game.
        - Build UI components.
        - Initialize game state.
        - Process events, update the game state, and render graphics.
        - Exit the loop when the mini-game is finished.
        """
        self._build_ui()
        self.start()
        clock: pygame.time.Clock = pygame.time.Clock()
        self.is_running = True

        while self.is_running:
            delta_time: float = clock.tick(self.game.engine.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.game.ui_manager.gui_manager.update(delta_time)
            self.update(delta_time)
            self.draw()
            pygame.display.update()

        self.kill()

    def kill(self) -> None:
        """Clean up UI components and terminate the mini-game."""
        self.is_running = False
        if self.title:
            self.title.kill()
        if self.background_panel:
            self.background_panel.kill()
        if self.close_button:
            self.close_button.kill()
