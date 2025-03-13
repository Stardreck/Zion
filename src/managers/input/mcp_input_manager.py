from __future__ import annotations
from typing import List, TYPE_CHECKING, Tuple

import sys
from smbus2 import SMBus
from colorama import Fore, Style, init

from src.managers.manager import Manager

if TYPE_CHECKING:
    from src.games.story_game import StoryGame

# Initialize colorama for colored console output.
init(autoreset=True)

##### MCP Register Definitions #####
IODIRA = 0x00
IODIRB = 0x01
GPPUA = 0x0C
GPPUB = 0x0D

##### GPIO registers #####
GPIOA = 0x12
GPIOB = 0x13

##### Game Board Pin Definitions #####
# Each dictionary defines a pin on the game board. Registers GPIOA/B and MCP addresses are used.
GAME_BOARD_PIN_DEFINITIONS = [
    # MCP1
    {"row": 0, "col": 0, "mask": 0x01, "pinName": "A0", "register": GPIOA, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 1, "mask": 0x02, "pinName": "A1", "register": GPIOA, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 2, "mask": 0x04, "pinName": "A2", "register": GPIOA, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 3, "mask": 0x08, "pinName": "A3", "register": GPIOA, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 4, "mask": 0x10, "pinName": "A4", "register": GPIOA, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 5, "mask": 0x20, "pinName": "A5", "register": GPIOA, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 6, "mask": 0x40, "pinName": "A6", "register": GPIOA, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 7, "mask": 0x80, "pinName": "A7", "register": GPIOA, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 8, "mask": 0x01, "pinName": "B0", "register": GPIOB, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 0, "col": 9, "mask": 0x02, "pinName": "B1", "register": GPIOB, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 1, "col": 0, "mask": 0x04, "pinName": "B2", "register": GPIOB, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 1, "col": 1, "mask": 0x08, "pinName": "B3", "register": GPIOB, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 1, "col": 2, "mask": 0x10, "pinName": "B4", "register": GPIOB, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 1, "col": 3, "mask": 0x20, "pinName": "B5", "register": GPIOB, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 1, "col": 4, "mask": 0x40, "pinName": "B6", "register": GPIOB, "mcpAddress": 0x20, "mcpName": "MCP1"},
    {"row": 1, "col": 5, "mask": 0x80, "pinName": "B7", "register": GPIOB, "mcpAddress": 0x20, "mcpName": "MCP1"},

    # MCP2
    {"row": 1, "col": 6, "mask": 0x01, "pinName": "A0", "register": GPIOA, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 1, "col": 7, "mask": 0x02, "pinName": "A1", "register": GPIOA, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 1, "col": 8, "mask": 0x04, "pinName": "A2", "register": GPIOA, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 1, "col": 9, "mask": 0x08, "pinName": "A3", "register": GPIOA, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 1, "col": 10, "mask": 0x10, "pinName": "A4", "register": GPIOA, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 0, "mask": 0x20, "pinName": "A5", "register": GPIOA, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 1, "mask": 0x40, "pinName": "A6", "register": GPIOA, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 2, "mask": 0x80, "pinName": "A7", "register": GPIOA, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 3, "mask": 0x01, "pinName": "B0", "register": GPIOB, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 4, "mask": 0x02, "pinName": "B1", "register": GPIOB, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 5, "mask": 0x04, "pinName": "B2", "register": GPIOB, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 6, "mask": 0x08, "pinName": "B3", "register": GPIOB, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 7, "mask": 0x10, "pinName": "B4", "register": GPIOB, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 8, "mask": 0x20, "pinName": "B5", "register": GPIOB, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 9, "mask": 0x40, "pinName": "B6", "register": GPIOB, "mcpAddress": 0x21, "mcpName": "MCP2"},
    {"row": 2, "col": 10, "mask": 0x80, "pinName": "B7", "register": GPIOB, "mcpAddress": 0x21, "mcpName": "MCP2"},

    # MCP3
    {"row": 3, "col": 0, "mask": 0x01, "pinName": "A0", "register": GPIOA, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 1, "mask": 0x02, "pinName": "A1", "register": GPIOA, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 2, "mask": 0x04, "pinName": "A2", "register": GPIOA, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 3, "mask": 0x08, "pinName": "A3", "register": GPIOA, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 4, "mask": 0x10, "pinName": "A4", "register": GPIOA, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 5, "mask": 0x20, "pinName": "A5", "register": GPIOA, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 6, "mask": 0x40, "pinName": "A6", "register": GPIOA, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 7, "mask": 0x80, "pinName": "A7", "register": GPIOA, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 8, "mask": 0x01, "pinName": "B0", "register": GPIOB, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 9, "mask": 0x02, "pinName": "B1", "register": GPIOB, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 3, "col": 10, "mask": 0x04, "pinName": "B2", "register": GPIOB, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 4, "col": 0, "mask": 0x08, "pinName": "B3", "register": GPIOB, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 4, "col": 1, "mask": 0x10, "pinName": "B4", "register": GPIOB, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 4, "col": 2, "mask": 0x20, "pinName": "B5", "register": GPIOB, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 4, "col": 3, "mask": 0x40, "pinName": "B6", "register": GPIOB, "mcpAddress": 0x22, "mcpName": "MCP3"},
    {"row": 4, "col": 4, "mask": 0x80, "pinName": "B7", "register": GPIOB, "mcpAddress": 0x22, "mcpName": "MCP3"},

    # MCP4
    {"row": 4, "col": 6, "mask": 0x01, "pinName": "A0", "register": GPIOA, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 4, "col": 7, "mask": 0x02, "pinName": "A1", "register": GPIOA, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 4, "col": 8, "mask": 0x04, "pinName": "A2", "register": GPIOA, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 4, "col": 9, "mask": 0x08, "pinName": "A3", "register": GPIOA, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 4, "col": 10, "mask": 0x10, "pinName": "A4", "register": GPIOA, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 5, "col": 0, "mask": 0x20, "pinName": "A5", "register": GPIOA, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 5, "col": 1, "mask": 0x40, "pinName": "A6", "register": GPIOA, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 5, "col": 2, "mask": 0x80, "pinName": "A7", "register": GPIOA, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 5, "col": 3, "mask": 0x01, "pinName": "B0", "register": GPIOB, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 5, "col": 8, "mask": 0x02, "pinName": "B1", "register": GPIOB, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 5, "col": 9, "mask": 0x04, "pinName": "B2", "register": GPIOB, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 5, "col": 10, "mask": 0x08, "pinName": "B3", "register": GPIOB, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 6, "col": 0, "mask": 0x10, "pinName": "B4", "register": GPIOB, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 6, "col": 1, "mask": 0x20, "pinName": "B5", "register": GPIOB, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 6, "col": 2, "mask": 0x40, "pinName": "B6", "register": GPIOB, "mcpAddress": 0x23, "mcpName": "MCP4"},
    {"row": 6, "col": 3, "mask": 0x80, "pinName": "B7", "register": GPIOB, "mcpAddress": 0x23, "mcpName": "MCP4"},

    # MCP5
    {"row": 6, "col": 7, "mask": 0x01, "pinName": "A0", "register": GPIOA, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 6, "col": 8, "mask": 0x02, "pinName": "A1", "register": GPIOA, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 6, "col": 9, "mask": 0x04, "pinName": "A2", "register": GPIOA, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 6, "col": 10, "mask": 0x08, "pinName": "A3", "register": GPIOA, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 7, "col": 0, "mask": 0x10, "pinName": "A4", "register": GPIOA, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 7, "col": 1, "mask": 0x20, "pinName": "A5", "register": GPIOA, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 7, "col": 2, "mask": 0x40, "pinName": "A6", "register": GPIOA, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 7, "col": 3, "mask": 0x80, "pinName": "A7", "register": GPIOA, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 7, "col": 8, "mask": 0x01, "pinName": "B0", "register": GPIOB, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 7, "col": 9, "mask": 0x02, "pinName": "B1", "register": GPIOB, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 7, "col": 10, "mask": 0x04, "pinName": "B2", "register": GPIOB, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 8, "col": 0, "mask": 0x08, "pinName": "B3", "register": GPIOB, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 8, "col": 1, "mask": 0x10, "pinName": "B4", "register": GPIOB, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 8, "col": 2, "mask": 0x20, "pinName": "B5", "register": GPIOB, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 8, "col": 3, "mask": 0x40, "pinName": "B6", "register": GPIOB, "mcpAddress": 0x24, "mcpName": "MCP5"},
    {"row": 8, "col": 4, "mask": 0x80, "pinName": "B7", "register": GPIOB, "mcpAddress": 0x24, "mcpName": "MCP5"},

    # MCP6
    {"row": 8, "col": 6, "mask": 0x01, "pinName": "A0", "register": GPIOA, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 8, "col": 7, "mask": 0x02, "pinName": "A1", "register": GPIOA, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 8, "col": 8, "mask": 0x04, "pinName": "A2", "register": GPIOA, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 8, "col": 9, "mask": 0x08, "pinName": "A3", "register": GPIOA, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 8, "col": 10, "mask": 0x10, "pinName": "A4", "register": GPIOA, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 0, "mask": 0x20, "pinName": "A5", "register": GPIOA, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 1, "mask": 0x40, "pinName": "A6", "register": GPIOA, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 2, "mask": 0x80, "pinName": "A7", "register": GPIOA, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 3, "mask": 0x01, "pinName": "B0", "register": GPIOB, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 4, "mask": 0x02, "pinName": "B1", "register": GPIOB, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 5, "mask": 0x04, "pinName": "B2", "register": GPIOB, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 6, "mask": 0x08, "pinName": "B3", "register": GPIOB, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 7, "mask": 0x10, "pinName": "B4", "register": GPIOB, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 8, "mask": 0x20, "pinName": "B5", "register": GPIOB, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 9, "mask": 0x40, "pinName": "B6", "register": GPIOB, "mcpAddress": 0x25, "mcpName": "MCP6"},
    {"row": 9, "col": 10, "mask": 0x80, "pinName": "B7", "register": GPIOB, "mcpAddress": 0x25, "mcpName": "MCP6"},

    # MCP7
    {"row": 10, "col": 0, "mask": 0x01, "pinName": "A0", "register": GPIOA, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 1, "mask": 0x02, "pinName": "A1", "register": GPIOA, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 2, "mask": 0x04, "pinName": "A2", "register": GPIOA, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 3, "mask": 0x08, "pinName": "A3", "register": GPIOA, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 4, "mask": 0x10, "pinName": "A4", "register": GPIOA, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 5, "mask": 0x20, "pinName": "A5", "register": GPIOA, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 6, "mask": 0x40, "pinName": "A6", "register": GPIOA, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 7, "mask": 0x80, "pinName": "A7", "register": GPIOA, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 8, "mask": 0x01, "pinName": "B0", "register": GPIOB, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 9, "mask": 0x02, "pinName": "B1", "register": GPIOB, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 10, "col": 10, "mask": 0x04, "pinName": "B2", "register": GPIOB, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 11, "col": 0, "mask": 0x08, "pinName": "B3", "register": GPIOB, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 11, "col": 1, "mask": 0x10, "pinName": "B4", "register": GPIOB, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 11, "col": 2, "mask": 0x20, "pinName": "B5", "register": GPIOB, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 11, "col": 3, "mask": 0x40, "pinName": "B6", "register": GPIOB, "mcpAddress": 0x26, "mcpName": "MCP7"},
    {"row": 11, "col": 4, "mask": 0x80, "pinName": "B7", "register": GPIOB, "mcpAddress": 0x26, "mcpName": "MCP7"},

    # MCP8
    {"row": 11, "col": 5, "mask": 0x01, "pinName": "A0", "register": GPIOA, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 11, "col": 6, "mask": 0x02, "pinName": "A1", "register": GPIOA, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 11, "col": 7, "mask": 0x04, "pinName": "A2", "register": GPIOA, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 11, "col": 8, "mask": 0x08, "pinName": "A3", "register": GPIOA, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 11, "col": 9, "mask": 0x10, "pinName": "A4", "register": GPIOA, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 11, "col": 10, "mask": 0x20, "pinName": "A5", "register": GPIOA, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 0, "mask": 0x40, "pinName": "A6", "register": GPIOA, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 1, "mask": 0x80, "pinName": "A7", "register": GPIOA, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 2, "mask": 0x01, "pinName": "B0", "register": GPIOB, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 3, "mask": 0x02, "pinName": "B1", "register": GPIOB, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 4, "mask": 0x04, "pinName": "B2", "register": GPIOB, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 5, "mask": 0x08, "pinName": "B3", "register": GPIOB, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 6, "mask": 0x10, "pinName": "B4", "register": GPIOB, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 7, "mask": 0x20, "pinName": "B5", "register": GPIOB, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 12, "col": 8, "mask": 0x40, "pinName": "B6", "register": GPIOB, "mcpAddress": 0x27, "mcpName": "MCP8"},
    {"row": 11, "col": 9, "mask": 0x80, "pinName": "B7", "register": GPIOB, "mcpAddress": 0x27, "mcpName": "MCP8"},
]


class I2CPin:
    """
    Represents a single I2C pin based on its configuration definition
    """

    def __init__(self, pin_definition: dict) -> None:
        self.row: int = pin_definition["row"]
        self.col: int = pin_definition["col"]
        self.mask: int = pin_definition["mask"]
        self.pin_name: str = pin_definition["pinName"]
        self.register: int = pin_definition["register"]
        self.mcp_address: int = pin_definition["mcpAddress"]
        self.mcp_name: str = pin_definition["mcpName"]

    def get_unique_key(self) -> str:
        """Generate a unique key for the pin."""
        return f"{self.mcp_name}_{self.row}_{self.col}_{self.pin_name}"

    def read_state(self, bus: SMBus) -> str:
        """
        Read the state of the pin using the I2C bus.
        Returns "LOW" if the bit value is 0 (Reed switch closed), otherwise "HIGH".
        """
        try:
            register_value = bus.read_byte_data(self.mcp_address, self.register)
            return "LOW" if (register_value & self.mask) == 0 else "HIGH"
        except Exception:
            return "ERR"

    def __str__(self) -> str:
        """Return a string representation of the I2C pin."""
        return f"[{self.mcp_name}] {self.pin_name} ({self.row}, {self.col})"


class I2CPinMonitor:
    """
    Monitors a list of I2C pins for state changes.
    It records the last state of each pin and returns any changes.
    """

    def __init__(self, pin_definitions: List[dict]) -> None:
        self.pins: List[I2CPin] = [I2CPin(defn) for defn in pin_definitions]
        self.last_states: dict[str, str] = {}

    def initialize_devices(self, bus: SMBus) -> None:
        """
        Initialize all MCP devices by configuring their registers
        and capturing the initial state of all pins.
        """
        unique_addresses = {pin.mcp_address for pin in self.pins}
        for address in unique_addresses:
            try:
                # Set all Port A and Port B pins as inputs and enable pull-ups
                bus.write_byte_data(address, IODIRA, 0xFF)
                bus.write_byte_data(address, IODIRB, 0xFF)
                bus.write_byte_data(address, GPPUA, 0xFF)
                bus.write_byte_data(address, GPPUB, 0xFF)
                print(f"{Fore.CYAN}Initialized MCP @ 0x{address:02X}")
            except Exception as error:
                print(f"{Fore.RED}Failed to initialize MCP @ 0x{address:02X}: {error}")

        # Capture initial states for all pins.
        print(f"\n{Style.BRIGHT}Initial States:")
        print(f"{'MCP':<10} {'Row':<3} {'Col':<3} {'Pin':<6} {'State':<8}")
        print("-" * 40)
        for pin in self.pins:
            key = pin.get_unique_key()
            state = pin.read_state(bus)
            self.last_states[key] = state
            state_color = Fore.GREEN if state == "LOW" else Fore.RED
            print(f"{str(pin):<10} {pin.row:<3} {pin.col:<3} {pin.pin_name:<6} {state_color}{state:<8}{Style.RESET_ALL}")
        print("-" * 40)

    def check_for_state_changes(self, bus: SMBus) -> List[Tuple[I2CPin, str, str]]:
        """
        Check all pins for any state changes.
        Returns a list of tuples: (pin, previous_state, current_state).
        """
        changes: List[Tuple[I2CPin, str, str]] = []
        for pin in self.pins:
            key = pin.get_unique_key()
            current_state = pin.read_state(bus)
            previous_state = self.last_states.get(key, "UNKNOWN")
            if current_state != previous_state:
                changes.append((pin, previous_state, current_state))
                self.last_states[key] = current_state

        if changes:
            print(f"\n{Style.BRIGHT}--- Detected State Changes ---")
            print(f"{'MCP':<10} {'Row':<3} {'Col':<3} {'Pin':<6} {'Old':<8} {'New':<8}")
            print("-" * 50)
            for pin, old_state, new_state in changes:
                old_color = Fore.GREEN if old_state == "LOW" else Fore.RED
                new_color = Fore.GREEN if new_state == "LOW" else Fore.RED
                print(f"{str(pin):<10} {pin.row:<3} {pin.col:<3} {pin.pin_name:<6} "
                      f"{old_color}{old_state:<8}{Style.RESET_ALL} {new_color}{new_state:<8}{Style.RESET_ALL}")
            print("-" * 50)

        return changes

class MCPInputManager(Manager):
    """
    Periodically polls the state of MCP pins.
    When a transition from HIGH to LOW is detected (indicating a reed switch activation),
    the game logic is updated by moving the player to the corresponding position.

    This manager is only enabled on Linux systems (Raspberry Pi).
    """

    def __init__(self, game: StoryGame, pin_definitions: List[dict]) -> None:
        super().__init__()
        self.game = game
        # Enable this manager only on Linux systems.
        self.enabled: bool = sys.platform.startswith("linux")
        if self.enabled:
            self.bus = SMBus(1)  # I2C Bus 1 on the Raspberry Pi
            self.pin_monitor = I2CPinMonitor(pin_definitions)
            self.pin_monitor.initialize_devices(self.bus)
        else:
            print("MCP Input Manager disabled (not running on Linux).")

    def get_valid_moves(self, current_row: int, current_col: int) -> List[Tuple[int, int]]:
        """
        Returns a list of valid neighboring positions for the hexagonal game board.
        """
        potential_moves = [
            (current_row, current_col - 1), (current_row, current_col + 1),  # Left & Right
            (current_row - 1, current_col - (current_row % 2)), (current_row - 1, current_col + (1 - current_row % 2)),  # Upper left & upper right
            (current_row + 1, current_col - (current_row % 2)), (current_row + 1, current_col + (1 - current_row % 2))   # Lower left & lower right
        ]
        return [(row, col) for row, col in potential_moves if row >= 0 and col >= 0]

    def process_events(self) -> None:
        """
        Process any detected pin state changes and update the game state accordingly.
        If a valid neighboring pin is activated (transition from HIGH to LOW),
        the player's position is updated.
        """
        if not self.enabled:
            return

        current_row = self.game.player_row
        current_col = self.game.player_col
        valid_moves = self.get_valid_moves(current_row, current_col)

        state_changes = self.pin_monitor.check_for_state_changes(self.bus)
        print("state_changes:", state_changes)
        for pin, previous_state, current_state in state_changes:
            if previous_state == "HIGH" and current_state == "LOW":
                new_position = (pin.row, pin.col)
                if new_position in valid_moves:
                    print(f"Reed switch activated at {new_position}; move allowed.")
                    self.game.move_player(pin.row, pin.col)
                    break
                else:
                    print(f"Invalid move to {new_position} ignored.")