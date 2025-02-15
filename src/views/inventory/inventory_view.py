from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import pygame_gui
from pygame import Rect
from pygame_gui.elements import UIImage

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_panel import UIPanel
from src.views.view import View

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class InventoryView(View):
    def __init__(self, game: StoryGame, background_image_path: str, background_panel_image_path: str,
                 empty_place_path: str):
        super().__init__(game.ui_manager.gui_manager)
        self.game = game
        self.is_running: bool = True

        ##### background image #####
        self.background_image_path = background_image_path
        self.background_image = pygame.image.load(self.background_image_path).convert()

        self.panel_background = background_panel_image_path

        self.empty_slot_path = empty_place_path
        self.inventory_empty_slot = pygame.image.load(self.empty_slot_path)
        self.inventory_empty_slot = pygame.transform.scale(self.inventory_empty_slot, (100, 100))

    def __build_ui(self):
        self.inventory_panel: UIPanel = UIPanel(
            relative_rect=Rect(0, 50, 700, 480),
            manager=self.pygame_gui_ui_manager,
            anchors={"center": "center"},
            object_id="panel_invisible",
        )
        inventory_panel_background = pygame.image.load(self.panel_background).convert_alpha()
        inventory_panel_background_image = pygame.transform.scale(inventory_panel_background,
                                                                  (self.game.engine.width, self.game.engine.height))
        self.inventory_panel_background: UIImage = UIImage(
            relative_rect=Rect(0, 0, 700, 480),
            manager=self.pygame_gui_ui_manager,
            image_surface=inventory_panel_background_image,
            anchors={"center": "center"},
            object_id="inventory_panel_background",
            container=self.inventory_panel
        )

        self.close_button: UIButton = UIButton(
            relative_rect=Rect(-40, 20, 38, 38),
            text="",
            manager=self.pygame_gui_ui_manager,
            anchors={"top": "top", "right": "right"},
            object_id="default_close_button",
            container=self.inventory_panel,
        )
        self.close_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda: self.close())

    def __draw_inventory_objects(self):

        ##### grid setup #####
        slot_width = 100
        slot_height = 100
        grid_rows = 2
        grid_cols = 2
        width_spacing = 120
        height_spacing = 185


        grid_width = grid_cols * slot_width + (grid_cols - 1) * (width_spacing - slot_width)
        grid_height = grid_rows * slot_height + (grid_rows - 1) * (height_spacing - slot_height)

        # coordinates for the first object
        start_x = self.inventory_panel_background.rect.left + 240
        start_y = self.inventory_panel_background.rect.top + 125

        ##### get found objects #####
        objects = self.game.inventory_manager.get_items()

        ##### draw inventory grid #####
        for row in range(grid_rows):
            for col in range(grid_cols):
                x_pos = start_x + col * width_spacing
                y_pos = start_y + row * height_spacing
                if len(objects) != 0:
                    # todo draw found object
                    objects.pop(0)
                else:
                    # draw empty slot
                    self.game.window.blit(self.inventory_empty_slot, (x_pos, y_pos))
        pass

    def close(self):
        self.is_running = False
        self.game.inventory_manager.is_open = False

    def run(self):
        self.__build_ui()
        clock = pygame.time.Clock()
        self.is_running = True

        while self.is_running and self.game.inventory_manager.is_open:
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
            self.__draw_inventory_objects()
            pygame.display.update()
        self.kill()

    def kill(self):
        if self.inventory_panel:
            self.inventory_panel.kill()
        if self.inventory_panel_background:
            self.inventory_panel_background.kill()
        if self.close_button:
            self.close_button.kill()
