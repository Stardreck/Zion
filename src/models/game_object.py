from typing import Optional


class GameObject:
    def __init__(self, name: str, alias: str, description: str, image_path: Optional[str] = None):
        self.name = name
        self.alias = alias
        self.description = description
        self.image_path = image_path