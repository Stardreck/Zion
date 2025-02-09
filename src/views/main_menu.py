import pygame
import pygame_gui
from pygame import Clock, Surface
from pygame_gui.elements import UIButton

from src.components.ui.ui_label import UILabel
from src.star_config import StarConfig
from src.views.view import View


class MainMenu(View):
    def __init__(self, pygame_gui_ui_manager: pygame_gui.UIManager, config: StarConfig):
        super().__init__(pygame_gui_ui_manager)
        self.is_running = True
        self.start_story_game = False

        self.text: UILabel | None = None
        self.config: StarConfig = config

        self.background_image = pygame.image.load(self.config.main_menu_background_image).convert()

    def __build_ui(self):

        title_rect = pygame.Rect(0, 50, 500, 250)
        self.title = UILabel(
            relative_rect=title_rect,
            text=self.config.title,
            manager=self.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="main_menu_title",
        )

        button_rect = pygame.Rect(0, 0, 200, 50)
        self.start_button = UIButton(
            relative_rect=button_rect,
            text=self.config.main_menu_start_button_text,
            manager=self.pygame_gui_ui_manager,
            anchors={"center": "center"},
            object_id="main_menu_start_button",
        )
        self.start_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.start())

    def kill(self):
        self.title.kill()
        self.start_button.kill()

    def start(self):
        self.start_story_game = True

    def run(self, surface: Surface, clock: Clock, fps: int) -> int:
        self.__build_ui()
        while self.is_running:
            time_delta = clock.tick(fps) / 1000.0  # limit to 60 FPS (defined in star_config)
            if (self.start_story_game):
                return 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return 0
                self.pygame_gui_ui_manager.process_events(event)
            # pass events to the UI elements
            self.pygame_gui_ui_manager.update(time_delta)

            # draw the background
            surface.blit(self.background_image, (0, 0))  # draw the background

            # draw the UI elements
            self.pygame_gui_ui_manager.draw_ui(surface)
            # update the UI
            pygame.display.update()
