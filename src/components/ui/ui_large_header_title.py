import pygame_gui
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface

from src.components.ui.ui_label import UILabel


class UILargeHeaderTitle(UILabel):
    def __init__(self, manager: UIManager, container: IContainerLikeInterface | None, start_text: str = "",
                 anchors=None, object_id=None):
        if anchors is None:
            anchors = {"centerx": "centerx", "top": "top"}
        if object_id is None:
            object_id = "planet_menu_title"
        super().__init__(relative_rect=Rect(0, 60, 800, 100), manager=manager, container=container, anchors=anchors,
                         object_id=object_id, text=start_text)
