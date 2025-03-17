from __future__ import annotations

import random
from typing import List, Tuple, Optional, TYPE_CHECKING

import pygame
import pygame_gui
from pygame import Rect

from src.mini_games.mini_game import MiniGame
from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class Bubble:
    """
    A simple bubble that appears on screen.
    """

    def __init__(self, pos: Tuple[int, int], radius: int, color: Tuple[int, int, int], lifetime: float):
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0


class BubblePopChallengeMiniGame(MiniGame):
    """
    Bubble Pop Challenge Mini-Game.
    Bubbles appear randomly and vanish after a short time.
    The player must click them to score points.
    Difficulty increases as bubbles spawn faster.
    """

    def __init__(self, game: StoryGame, background: str, game_duration: float = 30.0,
                 initial_spawn_interval: float = 1.5):
        super().__init__(game, background)
        self.game_duration: float = game_duration  # Total game time in seconds.
        # Load background and panel images.
        data = self.load_config_file_data()
        config = data.get("BubblePopChallengeMiniGame", {})
        sky_background_paths: List[str] = config.get("backgrounds", [])
        chosen_bg: str = random.choice(sky_background_paths) if sky_background_paths else background
        self.background_image: pygame.Surface = pygame.image.load(chosen_bg).convert()

        # UI elements.
        self.title: Optional[UILabel] = None
        self.background_panel: Optional[UIPanel] = None
        self.close_button: Optional[UIButton] = None
        self.score_label: Optional[UILabel] = None
        self.timer_label: Optional[UILabel] = None

        # Game variables.
        self.bubbles: List[Bubble] = []  # Active bubbles.
        self.score: int = 0
        self.spawn_timer: float = 0.0  # Timer for bubble spawning.
        self.spawn_interval: float = initial_spawn_interval  # Time between spawns.
        self.game_time: float = 0.0  # Total elapsed game time.
        self.is_running: bool = False
        self.game_finished: bool = False

        # Spawn area settings relative to the background panel.
        self.spawn_x_offset: int = 20
        self.spawn_y_offset: int = 20
        self.spawn_width: int = 1000
        self.spawn_height: int = 450
        self.spawn_area: Optional[Rect] = None  # Set in _build_ui.

    def _build_ui(self) -> None:
        """Create UI components."""
        self.background_panel = UIPanel(
            relative_rect=Rect(0, 25, 1000, 450),
            manager=self.game.ui_manager.gui_manager,
            anchors={"center": "center"},
            object_id="panel_invisible",
        )
        title_rect = Rect(0, 30, 1000, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text="Blasenjagd beginnt",
            manager=self.game.ui_manager.gui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="planet_menu_title",
        )
        score_rect = Rect(0, 80, 300, 150)
        self.score_label = UILabel(
            relative_rect=score_rect,
            text="Score: 0",
            manager=self.game.ui_manager.gui_manager,
            anchors={"left": "left", "top": "top"},
            object_id="score_text",
        )
        timer_rect = Rect(0, 30, 300, 150)
        self.timer_label = UILabel(
            relative_rect=timer_rect,
            text=f"zeit: {int(self.game_duration)}",
            manager=self.game.ui_manager.gui_manager,
            anchors={"left": "left", "top": "top"},
            object_id="score_text",
        )
        close_button_rect: Rect = Rect(0, -60, 500, 50)
        self.close_button = UIButton(
            relative_rect=close_button_rect,
            text="Aufgeben",
            manager=self.game.ui_manager.gui_manager,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="",
        )
        self.close_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.kill())

        # Set spawn area based on the background panel.
        panel_rect: Rect = self.background_panel.rect
        self.spawn_area = Rect(
            panel_rect.x + self.spawn_x_offset,
            panel_rect.y + self.spawn_y_offset,
            self.spawn_width,
            self.spawn_height,
        )

    def _spawn_bubble(self) -> None:
        """Spawn a new bubble at a random position in the spawn area."""
        if self.spawn_area is None:
            return

        # get a random spawnpoint
        x = random.randint(self.spawn_area.left, self.spawn_area.right)
        y = random.randint(self.spawn_area.top, self.spawn_area.bottom)
        pos = (x, y)

        # get a random bubble size
        radius = random.randint(20, 40)

        # color list
        available_colors: List[Tuple[int, int, int]] = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255)
        ]
        color = random.choice(available_colors)

        # Bubble lifetime decreases slightly as game time increases.
        lifetime = max(0.8, 2.0 - self.game_time * 0.05)

        # create the bubble and add it to the list
        bubble = Bubble(pos, radius, color, lifetime)
        self.bubbles.append(bubble)

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

    def _handle_mouse_button_down(self, event: pygame.event.Event) -> None:
        """Check if a bubble was clicked and remove it."""
        # get the clicked position
        mouse_pos = pygame.Vector2(event.pos)
        popped = False

        for bubble in self.bubbles[:]:
            # check if the clicked position matches a bubble location
            if (mouse_pos - bubble.pos).length() <= bubble.radius:
                self.bubbles.remove(bubble)
                self.score += 1
                popped = True
                break
        # update the score label
        if popped and self.score_label:
            self.score_label.set_text(f"Score: {self.score}")

    def update(self, delta_time: float) -> None:
        """
        Update game time, spawn bubbles, remove expired bubbles,
        and update the countdown timer.
        """
        if self.game_finished:
            return

        self.game_time += delta_time
        self.spawn_timer += delta_time

        # Update timer label.
        if self.timer_label:
            remaining = max(0, int(self.game_duration - self.game_time))
            self.timer_label.set_text(f"zeit: {remaining}")
            if remaining <= 0:
                self.game_finished = True
                self.title.set_text("Das war’s... fürs Erste")
                self.close_button.set_text("Zurück")

        # Only spawn new bubbles if game time is within duration.
        if self.game_time < self.game_duration and self.spawn_timer >= self.spawn_interval:
            self._spawn_bubble()
            self.spawn_timer = 0.0

        # Adjust spawn interval over time (minimum 0.5 seconds).
        self.spawn_interval = max(0.5, 1.5 - self.game_time * 0.05)

        # Update bubbles; remove those that exceed their lifetime.
        for bubble in self.bubbles[:]:
            bubble.age += delta_time
            if bubble.age >= bubble.lifetime:
                self.bubbles.remove(bubble)

    def draw(self) -> None:
        """Render the background, bubbles, and UI elements."""
        self.game.window.blit(self.background_image, (0, 0))
        self.game.ui_manager.gui_manager.draw_ui(self.game.window)

        for bubble in self.bubbles:
            pygame.draw.circle(
                self.game.window,
                bubble.color,
                (int(bubble.pos.x), int(bubble.pos.y)),
                bubble.radius,
            )

    def is_finished(self) -> bool:
        """Return True if the game is finished."""
        return self.finished

    def get_result(self) -> bool:
        """Return the game result (score)."""
        # currently not used
        return True

    def run(self) -> None:
        """Main game loop."""
        self._build_ui()
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
        if self.score_label:
            self.score_label.kill()
        if self.timer_label:
            self.timer_label.kill()
