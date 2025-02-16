import random

import pygame

from src.mini_games.mini_game import MiniGame


class TestMiniGame01(MiniGame):
    """
    Asteroid Dodge Mini-Game.
    The player controls a spaceship and must dodge falling asteroids.
    The mini-game lasts for a fixed duration.
    Surviving until the end is considered a win.
    """

    def is_finished(self) -> bool:
        pass

    def get_result(self) -> bool:
        pass

    def __init__(self, game, duration: float = 30.0):
        super().__init__(game)
        # Duration of the mini-game in seconds
        self.duration = duration
        self.elapsed_time = 0.0
        # Define the player's spaceship rectangle
        self.player_rect = pygame.Rect(0, 0, 50, 50)
        self.player_rect.center = (game.engine.width // 2, game.engine.height - 75)
        self.player_speed = 300  # Pixels per second
        # List to hold asteroid rectangles
        self.asteroids = []
        self.asteroid_speed = 200  # Speed at which asteroids fall (pixels per second)
        self.asteroid_spawn_timer = 0.0
        self.asteroid_spawn_interval = 1.0  # Spawn an asteroid every 1 second

    def start(self):
        """
        Initialize the mini-game state.
        """
        self.elapsed_time = 0.0
        self.asteroids.clear()
        self.finished = False
        self.success = False

    def update(self, delta_time: float):
        """
        Update the mini-game state, including moving asteroids and checking for collisions.
        :param delta_time: Time elapsed since the last update.
        """
        self.elapsed_time += delta_time

        # End the game if the duration is reached
        if self.elapsed_time >= self.duration:
            self.finished = True
            self.success = True
            return

        # Spawn new asteroids at defined intervals
        self.asteroid_spawn_timer += delta_time
        if self.asteroid_spawn_timer >= self.asteroid_spawn_interval:
            self.asteroid_spawn_timer -= self.asteroid_spawn_interval
            self.spawn_asteroid()

        # Move each asteroid downward
        for asteroid in self.asteroids:
            asteroid.y += int(self.asteroid_speed * delta_time)

        # Remove asteroids that have moved off-screen
        self.asteroids = [a for a in self.asteroids if a.y < self.game.engine.height]

        # Check for collisions between the spaceship and asteroids
        for asteroid in self.asteroids:
            if self.player_rect.colliderect(asteroid):
                self.finished = True
                self.success = False
                break

    def handle_event(self, event: pygame.event.Event):
        """
        Handle player input to move the spaceship.
        :param event: A pygame event.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player_rect.x -= int(self.player_speed * 0.1)
            elif event.key == pygame.K_RIGHT:
                self.player_rect.x += int(self.player_speed * 0.1)
            elif event.key == pygame.K_UP:
                self.player_rect.y -= int(self.player_speed * 0.1)
            elif event.key == pygame.K_DOWN:
                self.player_rect.y += int(self.player_speed * 0.1)

        # Ensure the spaceship stays within screen bounds
        self.player_rect.clamp_ip(pygame.Rect(0, 0, self.game.engine.width, self.game.engine.height))

    def draw(self, surface: pygame.Surface):
        """
        Render the mini-game elements.
        :param surface: The surface to draw on.
        """
        # Clear the screen with black
        surface.fill((0, 0, 0))
        # Draw the player's spaceship as a blue rectangle
        pygame.draw.rect(surface, (0, 0, 255), self.player_rect)
        # Draw each asteroid as a red ellipse
        for asteroid in self.asteroids:
            pygame.draw.ellipse(surface, (255, 0, 0), asteroid)
        # Display the remaining time
        font = pygame.font.SysFont(None, 36)
        time_left = max(0, int(self.duration - self.elapsed_time))
        time_text = font.render(f"Time Left: {time_left}", True, (255, 255, 255))
        surface.blit(time_text, (10, 10))

    def spawn_asteroid(self):
        """
        Spawn a new asteroid at a random x position at the top of the screen.
        """
        asteroid_width = random.randint(20, 50)
        asteroid_height = asteroid_width  # Asteroids are roughly circular
        x_position = random.randint(0, self.game.engine.width - asteroid_width)
        asteroid_rect = pygame.Rect(x_position, -asteroid_height, asteroid_width, asteroid_height)
        self.asteroids.append(asteroid_rect)
