from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import pygame_gui
from pygame import Rect

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.views.view import View

if TYPE_CHECKING:
    from src.games.story_game import StoryGame
    

class BaseStateView(View):
    def __init__(self, game: StoryGame, backround_image_path: str):
        super().__init__(game.ui_manager.gui_manager)
        self.game: StoryGame = game
        self.is_running: bool = True
        self.title_text = "game over!"
        
        # Load the background image
        self.background_image = pygame.image.load(backround_image_path).convert()
        
    
    def __build_ui(self):
        # Create title label at the top
        title_rect = Rect(0, 60, 800, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text=self.title_text,
            manager=self.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="planet_menu_title",
        )
        
        # Create the first button
        confirm_button = Rect(0, -125, 500, 50)
        self.confirm_button = UIButton(
            relative_rect=confirm_button,
            text="neustart",
            manager=self.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="panel_button",
        )
        self.confirm_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self._restart())
        
        pass


        
    def run(self):
        self.__build_ui()
        clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            time_delta = clock.tick(self.game.engine.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.game.debug_manager.toggle_debug_mode()
                        
                self.pygame_gui_ui_manager.process_events(event)
            self.pygame_gui_ui_manager.update(time_delta)
            # Draw the background image covering the window
            self.game.window.blit(self.background_image, (0, 0))
            self.pygame_gui_ui_manager.draw_ui(self.game.window)
            pygame.display.update()
        self.kill()

    
    def _restart(self):
        self.is_running = False
        self.game.restart()
    
    def kill(self):
        self.confirm_button.kill()
        
        
        
        