from pygame import Rect, Surface
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface
from pygame_gui.elements import UIImage

from src.components.ui.ui_label import UILabel


class UILargeLeftImageDescription(UILabel):
    def __init__(self, manager: UIManager, container: IContainerLikeInterface | None, text: str = "",
                 anchors=None, object_id=None):
        if anchors is None:
            anchors = {"left": "left"}
        super().__init__(relative_rect=Rect(75, 260, 100, 100), manager=manager, container=container,
                         text=text, anchors=anchors, object_id=object_id)
