import pygame_gui
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface
from pygame_gui.elements import UIButton


class UILargeDefaultButton(UIButton):
    def __init__(self, manager: UIManager, container: IContainerLikeInterface | None, start_text: str = "weiter",
                 anchors=None, object_id=None):
        if anchors is None:
            anchors = {"centerx": "centerx", "bottom": "bottom"}
        if object_id is None:
            object_id = "panel_button"
        super().__init__(relative_rect=Rect(0, -60, 500, 50), manager=manager, container=container, anchors=anchors,
                         object_id=object_id, text=start_text)
