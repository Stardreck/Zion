from __future__ import annotations

import random
from src.managers.manager import Manager
from src.models.event_card import EventCard
from typing import List, TYPE_CHECKING

from src.views.event.event_view import EventView

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class EventManager(Manager):
    def __init__(self, game: StoryGame, event_cards: List[EventCard]):
        """
        Initialize the EventManager.

        :param game: The main StoryGame instance.
        :param event_cards: List of EventCard objects loaded from JSON.
        """
        super().__init__()
        self.game = game
        # Split events into positive and negative lists
        self.negative_events = [card for card in event_cards if card.type == "negative"]
        self.positive_events = [card for card in event_cards if card.type == "positive"]

        # Adjustable probabilities for positive/negative events
        self.event_probability = self.game.engine.config.event_probability
        self.event_positive_probability = 0.5
        self.event_negative_probability = 0.5

    def trigger_event_if_possible(self) -> bool:
        """
        Check if an event should be triggered based on the configured probability.
        If triggered, apply event effects, display the event overlay, and then run the quiz.

        :return: True if an event was triggered, otherwise False.
        """
        # Check against global event probability from the configuration
        if random.random() < self.event_probability:
            # Decide event type (positive/negative) based on probability
            event_list = self.positive_events if random.random() < self.event_positive_probability else self.negative_events

            if not event_list:
                return False

            # Select a random event from the list
            event_card = random.choice(event_list)

            # apply effects
            self.apply_effects(event_card)

            # Debug output
            print(f"[EventManager] Event triggered: {event_card.name}")
            print(f"[EventManager] Description: {event_card.description}")
            print(f"[EventManager] Fuel change: {event_card.fuel_change}, Hull change: {event_card.hull_change}")

            # Display the event view
            event_view = EventView(self.game, event_card)
            event_view.run()
            return True
        return False

    def apply_effects(self, event_card: EventCard):
        # Apply event effects
        self.game.fuel += event_card.fuel_change
        self.game.hull += event_card.hull_change
