from typing import List, Optional


class StoryLine:
    def __init__(self, text: str, image_path: str | None = None, image_description: str | None = None):
        self.text = text
        self.image_path = image_path
        self.image_description = image_description
