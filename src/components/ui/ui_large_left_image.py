from pygame import Rect, Surface
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface
from pygame_gui.elements import UIImage


class UILargeLeftImage(UIImage):
    def __init__(self, manager: UIManager, container: IContainerLikeInterface | None, surface: Surface,
                 anchors=None, object_id=None):
        if anchors is None:
            anchors = {"left": "left"}
        super().__init__(relative_rect=Rect(20, 30, 240, 255), manager=manager, container=container,
                         image_surface=surface, anchors=anchors, object_id=object_id)
