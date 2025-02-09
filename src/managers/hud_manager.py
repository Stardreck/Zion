from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
import pygame
import pygame_gui
from pygame_gui.elements import UIImage

from src.components.ui.ui_panel import UIPanel
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_button import UIButton  # for other buttons
from src.enums.color import Color
from src.managers.manager import Manager

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class HUDManager(Manager):
    """
    The HUDManager creates and manages the Heads-Up Display (HUD) overlay.
    It uses pygame_gui elements to display the top bar (with fuel and hull),
    a sidebar with an inventory image, and a corner decoration.
    """
    def __init__(self, game: StoryGame):
        """
        Initialize the HUD manager.

        :param game: The StoryGame instance from which HUD data is taken.
        """
        super().__init__()
        self.game = game
        self.ui_manager: pygame_gui.UIManager = game.ui_manager.gui_manager

        # Retrieve screen dimensions from the engine.
        self.screen_width: int = self.game.engine.width
        self.screen_height: int = self.game.engine.height

        # Height for the top bar HUD.
        self.topbar_height: int = 50

        # Initialize HUD elements.
        self.__init_hud_elements()

    def __init_hud_elements(self):
        """
        Create the HUD UI elements:
          - A top bar panel with background, fuel and hull icons and labels.
          - A sidebar panel with a background image and an inventory image.
          - A corner decoration in the foreground.
        """
        # ---------------------------
        # Create the Top Bar Panel
        # ---------------------------
        self.topbar_panel: UIPanel = UIPanel(
            relative_rect=pygame.Rect(0, 0, self.screen_width, self.topbar_height),
            manager=self.ui_manager,
            anchors={"top": "top", "left": "left", "right": "right"},
            object_id="hud_topbar_panel"
        )
        # Top bar background image
        self.topbar_background: UIImage = UIImage(
            relative_rect=pygame.Rect(0, 0, self.screen_width, self.topbar_height),
            image_surface=self.__load_image("assets/interface/hud/topbar_background.png", fallback_size=(self.screen_width, self.topbar_height)),
            manager=self.ui_manager,
            container=self.topbar_panel,
            anchors={"top": "top", "left": "left", "right": "right"},
            object_id="hud_topbar_bg"
        )
        # Fuel icon (shifted further right)
        self.fuel_icon: UIImage = UIImage(
            relative_rect=pygame.Rect(150, 5, 40, 40),
            image_surface=self.__load_image("assets/icons/fuel_icon.png", fallback_size=(40, 40)),
            manager=self.ui_manager,
            container=self.topbar_panel,
            object_id="hud_fuel_icon"
        )
        # Fuel label – shows current fuel value
        self.fuel_label: UILabel = UILabel(
            relative_rect=pygame.Rect(160, 10, 100, 30),
            manager=self.ui_manager,
            text=f"{self.game.fuel}",
            container=self.topbar_panel,
            object_id="hud_fuel_label"
        )
        # Hull icon (shifted further right)
        self.hull_icon: UIImage = UIImage(
            relative_rect=pygame.Rect(320, 5, 40, 40),
            image_surface=self.__load_image("assets/icons/hull_icon.png", fallback_size=(40, 40)),
            manager=self.ui_manager,
            container=self.topbar_panel,
            object_id="hud_hull_icon"
        )
        # Hull label – shows current hull value
        self.hull_label: UILabel = UILabel(
            relative_rect=pygame.Rect(330, 10, 100, 30),
            manager=self.ui_manager,
            text=f"{self.game.hull}",
            container=self.topbar_panel,
            object_id="hud_hull_label"
        )

        # ---------------------------
        # Create the Sidebar Panel
        # ---------------------------
        self.sidebar_panel: UIPanel = UIPanel(
            relative_rect=pygame.Rect(0, self.topbar_height, 60, self.screen_height - self.topbar_height),
            manager=self.ui_manager,
            anchors={"top": "top", "bottom": "bottom", "left": "left"},
            object_id="hud_sidebar_panel"
        )
        # Sidebar background image
        self.sidebar_background: UIImage = UIImage(
            relative_rect=pygame.Rect(0, 0, 60, self.screen_height - self.topbar_height),
            image_surface=self.__load_image("assets/interface/hud/sidebar_background.png", fallback_size=(80, self.screen_height - self.topbar_height)),
            manager=self.ui_manager,
            container=self.sidebar_panel,
            anchors={"top": "top", "left": "left", "bottom": "bottom"},
            object_id="hud_sidebar_bg"
        )
        # Inventory image (displayed as a normal image, no button text)
        self.inventory_image: UIImage = UIImage(
            relative_rect=pygame.Rect(10, 40, 40, 40),
            image_surface=self.__load_image("assets/interface/inventory/inventory_icon.png", fallback_size=(60, 60)),
            manager=self.ui_manager,
            container=self.sidebar_panel,
            object_id="hud_inventory_image"
        )

        # ---------------------------
        # Create the Corner Decoration
        # ---------------------------
        # Place the decoration in the top-right corner. We set it with a high starting height so it renders on top.
        self.corner_decoration: UIImage = UIImage(
            relative_rect=pygame.Rect(0, 0, 70, 70),
            image_surface=self.__load_image("assets/interface/hud/corner_decoration.png", fallback_size=(70, 70)),
            manager=self.ui_manager,
            starting_height=10,  # ensures this element is drawn above others
            object_id="hud_corner_decoration"
        )

    def update(self):
        """
        Update the HUD with the current game data.
        This method should be called in the main game loop.
        """
        self.fuel_label.set_text(f"{self.game.fuel}")
        self.hull_label.set_text(f"{self.game.hull}")

    def __load_image(self, path: str, fallback_size: Tuple[int, int]) -> pygame.Surface:
        """
        Load an image from the given path. If loading fails, return a fallback surface
        with the given size filled with a semi-transparent dark color.

        :param path: The file path of the image asset.
        :param fallback_size: The size (width, height) for the fallback surface.
        :return: A pygame.Surface containing the loaded (or fallback) image.
        """
        try:
            image = pygame.image.load(path).convert_alpha()
            return image
        except Exception as error:
            print(f"[HUDManager] Could not load image at '{path}': {error}")
            fallback_surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
            fallback_surface.fill((0, 0, 0, 180))  # semi-transparent black
            return fallback_surface
