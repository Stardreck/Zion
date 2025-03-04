from __future__ import annotations
from typing import TYPE_CHECKING, List
import pygame
import pygame_gui
from pygame import Rect
from pygame_gui.elements import UIImage

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.components.ui.ui_text_box import UITextBox
from src.views.view import View

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class EventsActiveView(View):
    def __init__(self, game: StoryGame, background_image_path: str, background_panel_image_path: str):
        super().__init__(game.ui_manager.gui_manager)
        self.event_item_panels: List[UIPanel] = []
        self.game = game
        self.is_running: bool = True

        ##### background image #####
        self.background_image_path = background_image_path
        self.background_image = pygame.image.load(self.background_image_path).convert()

        self.panel_background = background_panel_image_path

    def __build_ui(self):
        self.events_panel: UIPanel = UIPanel(
            relative_rect=Rect(0, 25, 1300, 600),
            manager=self.pygame_gui_ui_manager,
            anchors={"center": "center"},
            object_id="panel_invisible",
            starting_height=9998
        )

        events_panel_background = pygame.image.load(self.panel_background).convert_alpha()
        events_panel_background_image = pygame.transform.scale(events_panel_background,
                                                               (self.game.engine.width, self.game.engine.height))
        self.events_panel_background: UIImage = UIImage(
            relative_rect=Rect(0, 0, 1300, 600),
            manager=self.pygame_gui_ui_manager,
            image_surface=events_panel_background_image,
            anchors={"center": "center"},
            object_id="inventory_panel_background",
            container=self.events_panel,
            starting_height=9998
        )
        self.title: UITextBox = UITextBox(
            relative_rect=Rect(125, -10, 500, 80),
            html_text="aktive ereignisse",
            manager=self.pygame_gui_ui_manager,
            object_id="events_active_title",
            starting_height=9999,
            container=self.events_panel,
            anchors={"centerx": "centerx", "top": "top"},
        )
        event_icon = pygame.image.load("assets/icons/event_icon_original.png").convert_alpha()
        self.event_icon: UIImage = UIImage(
            container=self.events_panel,
            relative_rect=Rect(-175, 3, 64, 64),
            image_surface=event_icon,
            starting_height=9999,
            anchors={"centerx": "centerx", "top": "top"},
        )

        self.close_button: UIButton = UIButton(
            relative_rect=Rect(-40, 25, 38, 38),
            text="",
            manager=self.pygame_gui_ui_manager,
            anchors={"top": "top", "right": "right"},
            object_id="default_close_button",
            container=self.events_panel,
            starting_height=9998
        )
        self.close_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.close())

        self.__draw_events_active_objects()

    def __draw_events_active_objects(self):

        event_cards = self.game.event_manager.active_events

        # grid settings
        columns = 2
        rows = 3
        cell_width = 600
        cell_height = 160
        start_x = 25
        start_y = 80
        spacing_x = 50
        spacing_y = 10

        row = 1 // columns
        col = 1 % columns
        x = start_x + col * (cell_width + spacing_x)
        y = start_y + row * (cell_height + spacing_y)



        for i, event_card in enumerate(event_cards[:6]):  # Maximal 6 Events anzeigen
            row = i // columns
            col = i % columns

            # Koordinaten für das Panel berechnen
            x = start_x + col * (cell_width + spacing_x)
            y = start_y + row * (cell_height + spacing_y)

            event_panel = UIPanel(
                relative_rect=Rect(x, y, cell_width, cell_height),
                manager=self.pygame_gui_ui_manager,
                container=self.events_panel,
                object_id="default_panel_transparent",
                starting_height=9999
            )

            event_icon_surface = pygame.image.load(event_card.icon).convert_alpha()
            event_icon = UIImage(
                relative_rect=Rect(10, 10, 100, 100),
                image_surface=event_icon_surface,
                manager=self.pygame_gui_ui_manager,
                starting_height=9999,
                container=event_panel,
            )
            event_title = UILabel(
                relative_rect=Rect(118, -30, 425, 100),
                manager=self.pygame_gui_ui_manager,
                text=event_card.name,

                object_id="event_title",
                container=event_panel,
            )
            event_description = UITextBox(
                relative_rect= pygame.Rect(110, 25, 480, 100),
                html_text=event_card.description,
                manager=self.pygame_gui_ui_manager,
                container=event_panel
            )
            duration_id = ""
            effect_id = ""
            if event_card.type == "negative":
                duration_id = "event_duration_text_negative"
                effect_id = "event_effect_text_negative"
            else:
                duration_id = "event_duration_text_positive"
                effect_id = "event_effect_text_positive"


            event_duration = UILabel(
                relative_rect=Rect(10, 90, 150, 100),
                manager=self.pygame_gui_ui_manager,
                text="Noch 2 Runden",
                object_id=duration_id,
                container=event_panel,
            )
            event_effect = UILabel(
                relative_rect=Rect(cell_width - 165, 90, 150, 100),
                manager=self.pygame_gui_ui_manager,
                text="-10 Treibstoff, -5 Hülle",
                object_id=effect_id,
                container=event_panel,
            )


            self.event_item_panels.append(event_panel)

    def close(self):
        self.is_running = False
        self.game.event_manager.is_open = False
        self.kill()

    def run(self):
        self.__build_ui()
        clock = pygame.time.Clock()
        self.is_running = True

        while self.is_running and self.game.event_manager.is_open:
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

    def kill(self):
        if self.events_panel:
            self.events_panel.kill()
        if self.events_panel_background:
            self.events_panel_background.kill()
        if self.close_button:
            self.close_button.kill()
        if self.event_item_panels:
            for panel in self.event_item_panels:
                panel.kill()
        if self.event_icon:
            self.event_icon.kill()
