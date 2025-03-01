from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

import os

import random

import pygame
import pygame_gui
from pygame import Rect

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_text_box import UITextBox
from src.models.event_card import EventCard
from src.views.view import View

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class EventView(View):
    def __init__(self, game: StoryGame, event_card: EventCard):
        """
        Initialize the EventView overlay.

        :param game: The main StoryGame instance.
        :param event_card: The EventCard object to display.
        """
        super().__init__(game.ui_manager.gui_manager)
        self.event_dismissed = False
        self.game = game
        self.event_card: EventCard = event_card

        # UI elements placeholders
        self.background_image_ui = None
        self.event_panel = None
        self.event_image_ui = None

    def __init(self):
        ##### spaceship window background #####

        # select a random spaceship window image
        spaceship_folder = "assets/images/spaceship"
        spaceship_images = [
            filename for filename in os.listdir(spaceship_folder)
            if filename.startswith("spaceship_window") and filename.endswith(".png")
        ]
        selected_bg = random.choice(spaceship_images) if spaceship_images else "spaceship_window_01.png"
        bg_path = os.path.join(spaceship_folder, selected_bg)
        bg_surface = pygame.image.load(bg_path).convert()
        bg_surface = pygame.transform.scale(bg_surface, (self.game.engine.width, self.game.engine.height))
        self.background_image_ui = pygame_gui.elements.UIImage(
            relative_rect=Rect(0, 0, self.game.engine.width, self.game.engine.height),
            image_surface=bg_surface,
            manager=self.pygame_gui_ui_manager
        )

        ##### event card #####
        # Define panel dimensions for the event card (with fixed size)
        panel_width, panel_height = 900, 600
        panel_x = (self.game.engine.width - panel_width) // 2
        panel_y = (self.game.engine.height - panel_height) // 2

        # Create a centered panel for the event card
        self.event_panel = pygame_gui.elements.UIPanel(
            relative_rect=Rect(panel_x, panel_y, panel_width, panel_height),
            manager=self.pygame_gui_ui_manager,
            object_id="panel_invisible"
        )

        # Load the event card image and scale it preserving aspect ratio with some padding (20px)
        event_img = pygame.image.load(self.event_card.image).convert_alpha()
        event_img = self.scale_image_aspect(event_img, panel_width - 150, panel_height - 150)

        # Center the scaled event image within the panel
        img_width, img_height = event_img.get_size()
        self.event_image_ui = pygame_gui.elements.UIImage(
            relative_rect=Rect(0, 0, img_width, img_height),
            image_surface=event_img,
            manager=self.pygame_gui_ui_manager,
            anchors={"center": "center"},
            container=self.event_panel
        )

        ##### event information #####
        event_title_rect = pygame.Rect(-335, 110, 250, 50)
        self.event_title = UILabel(
            relative_rect=event_title_rect,
            text=self.event_card.name,
            manager=self.pygame_gui_ui_manager,
            anchors={"right": "right", "top": "top"},
            container=self.event_panel,
            object_id="event_title"
        )
        event_description_rect = pygame.Rect(-325, 25, 300, 350)
        self.event_description = UITextBox(
            relative_rect=event_description_rect,
            html_text=self.event_card.description,
            manager=self.pygame_gui_ui_manager,
            anchors={"centery": "centery", "right": "right"},
            container=self.event_panel
        )


        ##### dismiss button #####
        button_rect = pygame.Rect(0, -75, 200, 50)
        self.close_button = UIButton(
            relative_rect=button_rect,
            container=self.event_panel,
            text="weiter",
            manager=self.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="main_menu_start_button",
        )
        self.close_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.kill())

    def run(self):
        """
        Display the event overlay until the user clicks on the button
        """
        self.__init()

        # Modal loop: wait until the user clicks to dismiss the event overlay
        clock = pygame.time.Clock()
        self.event_dismissed = False
        while not self.event_dismissed:
            time_delta = clock.tick(self.game.engine.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    self.event_dismissed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.game.debug_manager.toggle_debug_mode()
                self.pygame_gui_ui_manager.process_events(event)

            self.pygame_gui_ui_manager.update(time_delta)
            self.game.window.fill((0, 0, 0))
            self.pygame_gui_ui_manager.draw_ui(self.game.window)
            pygame.display.update()

        # Clean up the UI elements
        self.kill()

    def kill(self):
        print("kill method")
        self.event_dismissed = True
        self.event_image_ui.kill()
        self.event_panel.kill()
        self.background_image_ui.kill()

    def scale_image_aspect(self, image: pygame.Surface, max_width: int, max_height: int) -> pygame.Surface:
        """
        Scale an image while preserving its aspect ratio.

        :param image: The original pygame.Surface to scale.
        :param max_width: Maximum allowed width.
        :param max_height: Maximum allowed height.
        :return: A new scaled pygame.Surface.
        """
        orig_width, orig_height = image.get_size()
        scale_factor = min(max_width / orig_width, max_height / orig_height)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)
        return pygame.transform.smoothscale(image, (new_width, new_height))
