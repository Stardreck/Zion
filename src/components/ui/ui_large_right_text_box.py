from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface
from pygame_gui.elements import UITextBox


class UILargeRightTextBox(UITextBox):
    def __init__(self, manager: UIManager, container: IContainerLikeInterface | None, start_text: str = "",
                 anchors=None, object_id=None):
        if anchors is None:
            anchors = {"left": "left"}
        super().__init__(relative_rect=Rect(260, 20, 700, 320), manager=manager, container=container, anchors=anchors,
                         object_id=object_id, html_text=start_text)
