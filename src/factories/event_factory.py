from typing import Dict, Any

from src.models.event_card import EventCard


class EventFactory:
    @staticmethod
    def create_event(event_data: Dict[str, Any]) -> EventCard:
        return EventCard(
            name=event_data["name"],
            description=event_data["description"],
            hull_change=event_data.get("hull_change", 0),
            fuel_change=event_data.get("fuel_change", 0),
            image=event_data.get("image"),
            icon=event_data.get("icon"),
            event_type=event_data.get("type", "negative"),
            duration=event_data.get("duration", 0),
            repeats=event_data.get("repeats", False),
            once=event_data.get("once", False),
            required_conditions=event_data.get("required_conditions", {}),
            category=event_data.get("category", "general")
        )
