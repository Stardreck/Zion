from __future__ import annotations

import random
from typing import TYPE_CHECKING

from src.managers.manager import Manager
from src.views.inventory.inventory_view import InventoryView

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class InventoryManager(Manager):
    def __init__(self, game: StoryGame):
        super().__init__()
        self.game: StoryGame = game
        self.is_open: bool = False
        self.background_paths = self.game.engine.config.inventory_background_paths
        self.inventory_view: InventoryView | None = None

    def add_item(self):
        """
        Adds a GameObject to the inventory.
        """
        print("[InventoryManager] item added")
        pass

    def remove_item(self):
        """
        Removes a GameObject from the inventory. Returns True if successful.
        """
        print("[InventoryManager]item removed")
        pass

    def get_items(self):
        """
        Returns a list of all GameObjects in the inventory.
        """
        return []

    def find_item_by_name(self, name: str):
        """
        Finds a GameObject in the inventory by its name.
        """
        pass

    def clear_inventory(self) -> None:
        """
        Removes all items from the inventory.
        """
        print("[InventoryManager] inventory cleared")
        pass

    def open_inventory(self):
        """
        Opens the inventory menu
        """
        self.is_open = not self.is_open
        if self.is_open:
            print("[InventoryManager] inventory opened")
            self.inventory_view = InventoryView(self.game, self.__get_background_image_path(),
                                                self.game.engine.config.inventory_panel_background_path,
                                                self.game.engine.config.inventory_empty_slot_path)
            self.inventory_view.run()

    def close_inventory(self):
        """
         Close the inventory menu
        """
        self.is_open = False
        if self.inventory_view is not None:
            print("[InventoryManager] inventory closed")
            self.inventory_view.close()

    def __get_background_image_path(self) -> str:
        # select a random spaceship window image
        return random.choice(self.background_paths)
