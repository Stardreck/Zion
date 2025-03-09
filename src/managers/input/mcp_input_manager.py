from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional

import sys
import time
from smbus2 import SMBus
from colorama import Fore, Style, init

from src.managers.manager import Manager

if TYPE_CHECKING:
    from src.games.story_game import StoryGame

init(autoreset=True)

# MCP‑Registerdefinitionen
IODIRA = 0x00
IODIRB = 0x01
GPPUA = 0x0C
GPPUB = 0x0D

# Beispielregister für GPIO (je nach MCP, z. B. 0x12 = GPIOA, 0x13 = GPIOB)
GPIOA = 0x12
GPIOB = 0x13

PIN_DEFINITIONS_FOR_GAME_BOARD = [
    {
        "row": 0,
        "col": 0,
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,  # 0x12 = GPIOA
        "mcpAddress": 0x20,  # e.g. MCP1
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 1,
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 2,
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 3,
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 4,
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 5,
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 6,
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 7,
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 8,
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 0,
        "col": 9,
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 1,
        "col": 0,
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 1,
        "col": 1,
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 1,
        "col": 2,
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },

    {
        "row": 1,
        "col": 3,
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 1,
        "col": 4,
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "row": 1,
        "col": 5,
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    #####MCP 2 #####
    {
        "row": 1,
        "col": 6,
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 1,
        "col": 7,
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 1,
        "col": 8,
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 1,
        "col": 9,
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 1,
        "col": 10,
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 0,
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 1,
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 2,
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 3,
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 4,
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 5,
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 6,
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 7,
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },

    {
        "row": 2,
        "col": 8,
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 9,
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    {
        "row": 2,
        "col": 10,
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x21,
        "mcpName": "MCP2"
    },
    #####MCP 3 #####
    {
        "row": 3,
        "col": 0,
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 1,
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 2,
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 3,
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 4,
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 5,
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 6,
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 7,
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 8,
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 9,
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 3,
        "col": 10,
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 4,
        "col": 0,
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 4,
        "col": 1,
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },

    {
        "row": 4,
        "col": 2,
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 4,
        "col": 3,
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    {
        "row": 4,
        "col": 4,
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x22,
        "mcpName": "MCP3"
    },
    #####MCP 4 #####
    {
        "row": 4,
        "col": 6,
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 4,
        "col": 7,
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 4,
        "col": 8,
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 4,
        "col": 9,
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 4,
        "col": 10,
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 5,
        "col": 0,
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 5,
        "col": 1,
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 5,
        "col": 2,
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 5,
        "col": 3,
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 5,
        "col": 8,
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 5,
        "col": 9,
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 5,
        "col": 10,
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 6,
        "col": 0,
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },

    {
        "row": 6,
        "col": 1,
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 6,
        "col": 2,
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    {
        "row": 6,
        "col": 3,
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x23,
        "mcpName": "MCP4"
    },
    ##### MCP 5 #####
    {
        "row": 6,
        "col": 7,
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 6,
        "col": 8,
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 6,
        "col": 9,
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 6,
        "col": 10,
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 7,
        "col": 0,
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 7,
        "col": 1,
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 7,
        "col": 2,
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 7,
        "col": 3,
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 7,
        "col": 8,
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 7,
        "col": 9,
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 7,
        "col": 10,
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 8,
        "col": 0,
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 8,
        "col": 1,
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },

    {
        "row": 8,
        "col": 2,
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 8,
        "col": 3,
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    {
        "row": 8,
        "col": 4,
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x24,
        "mcpName": "MCP5"
    },
    #####MCP 6 #####
    {
        "row": 8,
        "col": 6,
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 8,
        "col": 7,
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 8,
        "col": 8,
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 8,
        "col": 9,
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 8,
        "col": 10,
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 0,
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 1,
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 2,
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 3,
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 4,
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 5,
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 6,
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 7,
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },

    {
        "row": 9,
        "col": 8,
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 9,
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    {
        "row": 9,
        "col": 10,
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x25,
        "mcpName": "MCP6"
    },
    ##### MCP 7 #####
    {
        "row": 10,
        "col": 0,
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 1,
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 2,
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 3,
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 4,
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 5,
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 6,
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 7,
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 8,
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 9,
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 10,
        "col": 10,
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 11,
        "col": 0,
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 11,
        "col": 1,
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },

    {
        "row": 11,
        "col": 2,
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 11,
        "col": 3,
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    {
        "row": 11,
        "col": 4,
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x26,
        "mcpName": "MCP7"
    },
    #####MCP 8 #####
    {
        "row": 11,
        "col": 5,
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 11,
        "col": 6,
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 11,
        "col": 7,
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 11,
        "col": 8,
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 11,
        "col": 9,
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 11,
        "col": 10,
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 12,
        "col": 0,
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 12,
        "col": 1,
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 12,
        "col": 2,
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 12,
        "col": 3,
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 12,
        "col": 4,
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 12,
        "col": 5,
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 12,
        "col": 6,
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },

    {
        "row": 12,
        "col": 7,
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 12,
        "col": 8,
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },
    {
        "row": 11,
        "col": 9,
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x27,
        "mcpName": "MCP8"
    },

]


# --- Hilfsklassen ---

class I2CPin:
    def __init__(self, definition):
        self.row = definition["row"]
        self.col = definition["col"]
        self.mask = definition["mask"]
        self.pin_name = definition["pinName"]
        self.register = definition["register"]
        self.mcp_address = definition["mcpAddress"]
        self.mcp_name = definition["mcpName"]

    def get_key(self):
        """Erzeuge einen eindeutigen Schlüssel für den Pin."""
        return f"{self.mcp_name}_{self.row}_{self.col}_{self.pin_name}"

    def read_state(self, bus):
        """
        Lies den Zustand des Pins.
        Gibt "LOW" zurück, wenn der entsprechende Bitwert 0 ist (Reed‑Schalter geschlossen),
        andernfalls "HIGH".
        """
        try:
            reg_value = bus.read_byte_data(self.mcp_address, self.register)
            state = reg_value & self.mask
            return "LOW" if state == 0 else "HIGH"
        except Exception:
            return "ERR"


class PinMonitor:
    """
    Überwacht eine Liste von I2C‑Pins und liefert alle Zustandsänderungen.
    """

    def __init__(self, pin_definitions):
        self.pins = [I2CPin(defn) for defn in pin_definitions]
        self.last_states = {}

    def initialize_devices(self, bus):
        unique_addresses = {pin.mcp_address for pin in self.pins}
        for addr in unique_addresses:
            try:
                bus.write_byte_data(addr, IODIRA, 0xFF)  # Alle Pins Port A als Eingang
                bus.write_byte_data(addr, IODIRB, 0xFF)  # Alle Pins Port B als Eingang
                bus.write_byte_data(addr, GPPUA, 0xFF)  # Pull-ups auf Port A aktivieren
                bus.write_byte_data(addr, GPPUB, 0xFF)  # Pull-ups auf Port B aktivieren
                print(f"{Fore.CYAN}Initialized MCP @ 0x{addr:02X}")
            except Exception as e:
                print(f"{Fore.RED}Failed to initialize MCP @ 0x{addr:02X}: {e}")

        # Initialzustände erfassen
        print(f"\n{Style.BRIGHT}Initial States:")
        print(f"{'MCP':<5} {'Row':<3} {'Col':<3} {'Pin':<4} {'State':<8}")
        print("-" * 40)
        for pin in self.pins:
            key = pin.get_key()
            state = pin.read_state(bus)
            self.last_states[key] = state
            color = Fore.GREEN if state == "LOW" else Fore.RED
            print(f"{str(pin)} {color}{state:<8}{Style.RESET_ALL}")
        print("-" * 40)

    def check_for_changes(self, bus):
        """
        Prüft alle Pins auf Zustandsänderungen und gibt eine Liste der Änderungen zurück.
        Jede Änderung ist ein Tupel (pin, alter_zustand, neuer_zustand).
        """
        changes = []
        for pin in self.pins:
            key = pin.get_key()
            current_state = pin.read_state(bus)
            if current_state != self.last_states.get(key):
                changes.append((pin, self.last_states.get(key), current_state))
                self.last_states[key] = current_state
        if len(changes) > 0:
            print(f"\n{Style.BRIGHT}--- Changes Detected ---")
            print(f"{'MCP':<5} {'Row':<3} {'Col':<3} {'Pin':<4} {'Old':<8} {'New':<8}")
            print("-" * 50)
            for pin, old, new in changes:
                color_old = Fore.GREEN if old == "LOW" else Fore.RED
                color_new = Fore.GREEN if new == "LOW" else Fore.RED
                print(f"{str(pin)} {color_old}{old:<8}{Style.RESET_ALL} {color_new}{new:<8}{Style.RESET_ALL}")
            print("-" * 50)

        return changes


# --- MCP Input Manager ---

class McpInputManager(Manager):
    """
    Dieser Manager fragt periodisch den Zustand der MCP‑Pins ab.
    Bei einer Änderung von HIGH zu LOW wird angenommen, dass ein Reed‑Schalter
    (und damit ein physisches Feld) aktiviert wurde – die Spielfigur wird dann
    in der Game‑Logik auf diese Position gesetzt.

    Der Manager wird nur auf Linux-Systemen (z.B. Raspberry Pi) aktiviert.
    """

    def __init__(self, game: StoryGame, pin_definitions):
        super().__init__()
        self.game = game
        # Aktivierung nur, wenn wir unter Linux laufen
        self.enabled = sys.platform.startswith("linux")
        if self.enabled:
            self.bus = SMBus(1)  # I2C Bus (normalerweise Bus 1 auf dem Pi)
            self.pin_monitor = PinMonitor(pin_definitions)
            self.pin_monitor.initialize_devices(self.bus)
        else:
            print("MCP Input Manager deaktiviert (nicht Linux).")

    def get_valid_moves(self, row: int, col: int) -> list[tuple[int, int]]:
        """
        Gibt eine Liste der gültigen Nachbarpositionen für ein Hexagon-Spielfeld zurück.
        """
        valid_moves = [
            (row, col - 1), (row, col + 1),  # Links & Rechts
            (row - 1, col - (row % 2)), (row - 1, col + (1 - row % 2)),  # Oben links & oben rechts
            (row + 1, col - (row % 2)), (row + 1, col + (1 - row % 2))  # Unten links & unten rechts
        ]
        return [(r, c) for r, c in valid_moves if r >= 0 and c >= 0]

    def process_events(self):
        if not self.enabled:
            return

        current_row = self.game.player_row
        current_col = self.game.player_col
        valid_moves = self.get_valid_moves(current_row, current_col)

        changes = self.pin_monitor.check_for_changes(self.bus)
        for pin, old_state, new_state in changes:
            if old_state == "HIGH" and new_state == "LOW":
                new_position = (pin.row, pin.col)
                if new_position in valid_moves:
                    print(f"Reed-Schalter aktiviert an {new_position}, Bewegung erlaubt.")
                    self.game.move_player(pin.row, pin.col)

                    break
                else:
                    print(f"Ungültige Bewegung zu {new_position}, ignoriert.")

    def close(self):
        if self.enabled:
            self.bus.close()
