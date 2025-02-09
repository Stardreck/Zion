from enum import Enum


class Color(Enum):
    """Farben als Enum für bessere Lesbarkeit."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DEBUG_PLANET = (171,205,239)
    DEBUG_PLAYER = (255, 60, 60)
