from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
import pygame_gui

from src.enums.color import Color
from src.managers.manager import Manager
from src.plugins.video_player import VideoPlayer

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class UIManager(Manager):
    """
    Manages UI elements such as HUDs, Overlays
    """

    def __init__(self, game: StoryGame):
        """
        Initialize the UIManager with a reference to the game instance.
        """
        super().__init__()
        self.game: StoryGame = game
        self.gui_manager: pygame_gui.UIManager = self.game.engine.pygame_gui_ui_manager

    def display_cutscene(self, media_path: str) -> None:
        """
        Display a cutscene image or video and wait for user input to continue.
        :param media_path: Path to the cutscene media (image or video).
        """
        if media_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            player = VideoPlayer(self.game.window)
            player.set_video(media_path)
            player.play()
        else:
            waiting = True
            clock = pygame.time.Clock()

            try:
                image = pygame.image.load(media_path).convert()
                image = pygame.transform.scale(image, self.game.window.get_size())
            except Exception as e:
                print(f"[UIManager] Cutscene could not be loaded {media_path}: {e}")
                image = pygame.Surface(self.game.window.get_size())
                image.fill(Color.BLACK.value)

            while waiting and self.game.is_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game.stop()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game.stop()
                            return
                        else:
                            waiting = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False

                self.game.draw()
                self.game.window.blit(image, (0, 0))
                pygame.display.flip()
                clock.tick(60)
