from __future__ import annotations  # Uncomment if not already present
import pymunk
from typing import Optional

class Endpoint:
    def __init__(self, body: pymunk.Body, shape: pymunk.Circle, color, connected: bool, connection: Optional[Endpoint] = None):
        self.body: pymunk.Body = body
        self.shape: pymunk.Circle = shape
        self.color:  tuple[int, int, int] = color
        self.connected: bool = connected
        self.connection: Endpoint | None = connection
