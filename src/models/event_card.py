class EventCard:
    """
    Represents an event card
    """

    def __init__(self, name: str, description: str, hull_change: int = 0, fuel_change: int = 0,
                 image: str = None, icon: str = None, event_type: str = "negative", duration: int = 0,
                 repeats: bool = False, required_conditions: dict = None, category: str = None):
        self.name = name
        self.description_template = description  # Speichern der Vorlage
        self.hull_change = hull_change
        self.fuel_change = fuel_change
        self.image = image
        self.icon = icon
        self.type = event_type
        self.duration = duration
        self.repeats = repeats
        self.required_conditions = required_conditions or {}
        self.category = category

    @property
    def description(self) -> str:
        """
        Returns a dynamically formatted description based on hull_change and fuel_change.
        Positive numbers are prefixed with a plus sign, while negative numbers retain their minus sign.

        :return: Formatted description string.
        """
        # Format hull_change: add '+' if positive, leave as is if zero or negative.
        formatted_hull_change = f"<b>+{self.hull_change} Hülle</b>" if self.hull_change > 0 else f"<b>{self.hull_change} Hülle</b>"
        # Format fuel_change similarly.
        formatted_fuel_change = f"<b>+{self.fuel_change} Treibstoff</b>" if self.fuel_change > 0 else f"<b>{self.fuel_change} Treibstoff</b>"

        return self.description_template.format(
            hull_change=formatted_hull_change,
            fuel_change=formatted_fuel_change
        )

    @property
    def formatted_html_hull_change(self):
        return f"<b>+{self.hull_change} Hülle</b>" if self.hull_change > 0 else f"<b>{self.hull_change} Hülle</b>"

    @property
    def formatted_html_fuel_change(self):
        return f"<b>+{self.fuel_change} Treibstoff</b>" if self.fuel_change > 0 else f"<b>{self.fuel_change} Treibstoff</b>"

    @property
    def formatted_text_hull_change(self):
        if self.hull_change == 0: return ""
        return f"+{self.hull_change} Hülle" if self.hull_change > 0 else f"{self.hull_change} Hülle"

    @property
    def formatted_text_fuel_change(self):
        if self.fuel_change == 0: return ""
        return f"+{self.fuel_change} Treibstoff" if self.fuel_change > 0 else f"{self.fuel_change} Treibstoff"
