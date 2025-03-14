from __future__ import annotations

import copy
import random

from src.managers.event.mini_game_manager import MiniGameManager
from src.managers.manager import Manager
from src.mini_games.cable_connection.cable_connection_mini_game import CableConnectionMiniGame
from src.models.event_card import EventCard
from typing import List, TYPE_CHECKING

from src.views.event.event_view import EventView
from src.views.event.events_active_view import EventsActiveView

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
        self.events_active_view: EventsActiveView | None = None
        self.game = game

        self.mini_game_manager: MiniGameManager = MiniGameManager(self.game)

        # Split events into positive and negative lists
        self.negative_events = [card for card in event_cards if card.type == "negative"]
        self.positive_events = [card for card in event_cards if card.type == "positive"]
        self.active_events: List[EventCard] = []

        # Adjustable probabilities for positive/negative events in star_config.json
        self.event_probability = self.game.engine.config.event_probability
        self.base_positive_probability = self.game.engine.config.event_base_positive_probability
        self.event_positive_probability = self.base_positive_probability
        self.change_probability_value = self.game.engine.config.change_probability_by

        self.max_error_count = self.game.engine.config.event_max_error_count
        self.error_count: int = 0

        self.is_open = False
        self.background_paths = self.game.engine.config.inventory_background_paths

    def increase_error_count(self):
        if self.error_count < self.max_error_count:
            self.error_count += 1
            self.__update_event_probabilities()

    def decrease_error_count(self):
        if self.error_count > 0:
            self.error_count -= 1
            self.__update_event_probabilities()

    def __update_event_probabilities(self) -> None:
        """
        Update the probability of triggering a positive event based on the error_count.
        As error_count increases, the chance for a positive event decreases.
        The positive probability is never allowed to drop below 0.1.
        """
        self.event_positive_probability = max(0.1,
                                              self.event_positive_probability - self.change_probability_value * self.error_count)

    def get_forced_events(self) -> List[EventCard] | []:
        events = self.negative_events + self.positive_events

        forced_events: List[EventCard] = []

        for event in events:
            if event.category == "game_over":
                # check only events with required conditions
                if event.required_conditions.items() != 0 and len(event.required_conditions) != 0:
                    # check if conditions are met
                    if self.__check_conditions(event):
                        forced_events.append(event)

        return forced_events

    def __check_conditions(self, event_card: EventCard) -> bool:
        """
        Check if the event meets the required conditions.
        :param event_card: The EventCard to check.
        :return: True if conditions are met, False otherwise.
        """
        if len(event_card.required_conditions.items()) == 0:
            return True

        for key, value in event_card.required_conditions.items():
            if key == "min_fuel" and self.game.fuel > value:
                return True
            if key == "max_fuel" and self.game.fuel <= value:
                return True
            if key == "min_hull" and self.game.hull > value:
                return True
            if key == "quiz_error_count" and self.error_count >= value:
                return True
            if key == "event_completed_negative":
                required_event = [event for event in self.negative_events if event.name == value]
                if required_event is None or len(required_event) == 0:
                    return True

        return False

    def trigger_event_if_possible(self) -> bool:
        """
        Check if an event should be triggered based on the configured probability.
        If triggered, apply event effects, display the event overlay, and then run the quiz.

        :return: True if an event was triggered, otherwise False.
        """
        # Update probabilities in case error_count has changed
        self.__update_event_probabilities()

        # Check against global event probability from the configuration
        if random.random() < self.event_probability:
            # an event should be triggered, check if a mini-game should be played
            if self.mini_game_manager.play_mini_game_if_possible():
                return True
            else:
                ##### run a random event #####
                # Decide event type (positive/negative) based on probability
                is_positive_event = random.random() < self.event_positive_probability
                if is_positive_event:
                    event_list = self.positive_events
                else:
                    event_list = self.negative_events

                # Filter events that meet the conditions
                filtered_events = [event for event in event_list if self.__check_conditions(event)]

                if not filtered_events:
                    return False

                # Select a random event from the list
                event_card: EventCard = random.choice(filtered_events)

                self.run_event(event_card)

                # remove the event card if it's only once allowed
                if event_card.once:
                    if is_positive_event:
                        self.positive_events.remove(event_card)
                    else:
                        self.negative_events.remove(event_card)

                return True
        return False

    def run_event(self, event_card: EventCard):
        print(f"[EventManager] Event triggered: {event_card.name}")
        print(f"[EventManager] Fuel change: {event_card.fuel_change}, Hull change: {event_card.hull_change}")

        # change HUD text corresponding to the card effect
        # self.game.hud_manager.fuel_label.set_text(f"{self.game.fuel} {event_card.fuel_change}")

        # Display the event view
        event_view = EventView(self.game, event_card)
        event_view.run()

        # apply effects
        self.apply_effects(event_card)

        # add event to the active event list if it's not a one time event
        if event_card.duration != 0:
            self.add_active_event(event_card)

    def run_active_events(self):
        """Runs active events, applies effects, and removes expired events."""
        for index in reversed(range(len(self.get_active_events()))):
            event = self.active_events[index]
            self.apply_effects(event)
            event.duration -= 1
            print(f"[EventManager] active event {event.name} triggered, "
                  f"effects: Fuel Change: {event.fuel_change}, Hull change: {event.hull_change} "
                  f"new duration: {event.duration}")
            if event.duration <= 0:
                self.active_events.pop(index)  # Sicheres Entfernen

    def get_active_events(self):
        return self.active_events

    def get_active_events_fuel_change(self):
        active_events = self.get_active_events()
        fuel_change = 0
        for event in active_events:
            fuel_change += event.fuel_change
        return fuel_change

    def add_active_event(self, event: EventCard):
        copied_event = copy.deepcopy(event)
        self.active_events.append(copied_event)

    def open_active_events_menu(self):
        print(f"[EventManager] Open events active menu")

        self.is_open = not self.is_open
        if self.is_open:
            self.events_active_view = EventsActiveView(self.game, self.__get_background_image_path(),
                                                       self.game.engine.config.event_panel_background_path)

            self.events_active_view.run()

    def close_active_events_menu(self):
        self.is_open = False
        if self.events_active_view is not None:
            self.events_active_view.close()

    def __get_background_image_path(self) -> str:
        # --- Background: Select a random spaceship window image ---
        return random.choice(self.background_paths)

    def apply_effects(self, event_card: EventCard):
        # Apply event effects
        self.game.fuel += event_card.fuel_change
        self.game.hull += event_card.hull_change
