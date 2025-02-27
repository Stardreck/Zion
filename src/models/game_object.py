from typing import Optional


class GameObject:
    def __init__(self, name: str, alias: str, description: str, location: str, image_path: Optional[str] = None ):
        self.name = name
        self.alias = alias
        self.description = description
        self.location = location
        self.image_path = image_path