from pygame import Rect
from pygame_gui import UIManager

from src.components.ui.ui_panel import UIPanel


class UILargeDefaultPanelTransparentBg(UIPanel):
    def __init__(self, manager: UIManager, anchors=None, object_id=None):
        if anchors is None:
            anchors = {"center": "center"}
        if object_id is None:
            object_id = "default_panel_transparent"
        super().__init__(relative_rect=Rect(0, 50, 1000, 480), manager=manager, anchors=anchors, object_id=object_id)
