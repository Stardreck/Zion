from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface

from src.components.ui.ui_panel import UIPanel


class UILargeDefaultPanel(UIPanel):
    def __init__(self, manager: UIManager, container: IContainerLikeInterface | None, anchors=None, object_id=None):
        if anchors is None:
            anchors = {"centerx": "centerx", "top": "top"}
        if object_id is None:
            object_id = "default_panel"
        super().__init__(relative_rect=Rect(0, 10, 980, 400), manager=manager, container=container, anchors=anchors,
                         object_id=object_id)
