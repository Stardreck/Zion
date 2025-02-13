from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from src.managers.manager import Manager

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class InventoryManager(Manager):
    def __init__(self, game: StoryGame):
        super().__init__()
        self.game: StoryGame = game

    def add_item(self):
        """
        Adds a GameObject to the inventory.
        """
        pass

    def remove_item(self):
        """
        Removes a GameObject from the inventory. Returns True if successful.
        """
        pass

    def get_items(self):
        """
        Returns a list of all GameObjects in the inventory.
        """
        pass

    def find_item_by_name(self, name: str):
        """
        Finds a GameObject in the inventory by its name.
        """
        pass

    def clear_inventory(self) -> None:
        """
        Removes all items from the inventory.
        """
        print("[InventoryManager] inventory cleared.")
        pass

