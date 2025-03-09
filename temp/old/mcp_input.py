import smbus2
import time
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP23017 register definitions
IODIRA = 0x00  # I/O direction register for Port A
IODIRB = 0x01  # I/O direction register for Port B
GPPUA  = 0x0C  # Pull-up enable register for Port A
GPPUB  = 0x0D  # Pull-up enable register for Port B

# Define pin configurations for the reed switches (all on one MCP device in this example)
PIN_DEFINITIONS: List[Dict[str, Any]] = [
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
        "col": 20,
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
# Mapping of specific pin names to movement directions.
# (Adjust these mappings to suit your hardware layout and desired movement actions.)
PIN_TO_DIRECTION = {
    "A0": "UP",
    "A1": "DOWN",
    "A2": "LEFT",
    "A3": "RIGHT",
    # Additional mappings can be defined here if needed.
}


class MCPInput:
    """
    Handles input reading from MCP23017 devices for reed switch monitoring.
    """

    def __init__(self, bus_number: int = 1):
        """
        Initialize the MCPInput instance with the given I2C bus.
        """
        self.bus = smbus2.SMBus(bus_number)
        # Determine unique MCP addresses from the pin definitions.
        self.mcp_addresses = {pin["mcp_address"] for pin in PIN_DEFINITIONS}
        self.initialize_all_mcp()

    def initialize_all_mcp(self) -> None:
        """
        Initialize each MCP device: set all pins as inputs and enable pull-ups.
        """
        for addr in self.mcp_addresses:
            self.initialize_mcp(addr)

    def initialize_mcp(self, mcp_address: int) -> None:
        """
        Initialize a single MCP device.
        """
        try:
            # Set all pins to inputs for both Port A and Port B.
            self.bus.write_byte_data(mcp_address, IODIRA, 0xFF)
            self.bus.write_byte_data(mcp_address, IODIRB, 0xFF)
            # Enable pull-ups on both ports.
            self.bus.write_byte_data(mcp_address, GPPUA, 0xFF)
            self.bus.write_byte_data(mcp_address, GPPUB, 0xFF)
            logger.info(f"Initialized MCP @ 0x{mcp_address:02X} as inputs with pull-ups.")
        except Exception as e:
            logger.error(f"Failed to initialize MCP @ 0x{mcp_address:02X}: {e}")

    def read_pin(self, pin_def: Dict[str, Any]) -> bool:
        """
        Read the state of a single pin.
        Returns True if the pin is HIGH (inactive) and False if LOW (active).
        """
        try:
            reg_value = self.bus.read_byte_data(pin_def["mcp_address"], pin_def["register"])
            state = reg_value & pin_def["mask"]
            return state != 0
        except Exception as e:
            logger.error(f"Failed to read pin {pin_def['pin_name']} on MCP @ 0x{pin_def['mcp_address']:02X}: {e}")
            return True  # Assume inactive on error

    def get_reed_switch_states(self) -> Dict[str, bool]:
        """
        Returns a dictionary mapping pin names (only those used for movement) to their active state.
        A value of True indicates the switch is not pressed (HIGH), and False means active (LOW).
        """
        states = {}
        for pin_def in PIN_DEFINITIONS:
            pin_name = pin_def["pin_name"]
            if pin_name in PIN_TO_DIRECTION:
                # Reed switches are active low.
                is_active = not self.read_pin(pin_def)
                states[pin_name] = is_active
        return states

    def get_movement_directions(self) -> List[str]:
        """
        Check all reed switches and return a list of movement directions that are active.
        """
        directions = []
        states = self.get_reed_switch_states()
        for pin_name, active in states.items():
            if active:
                direction = PIN_TO_DIRECTION.get(pin_name)
                if direction:
                    directions.append(direction)
        return directions


# Test routine for standalone testing of MCPInput functionality.
def test_mcp_input() -> None:
    mcp_input = MCPInput()
    while True:
        states = mcp_input.get_reed_switch_states()
        for pin, active in states.items():
            status = "ACTIVE" if active else "INACTIVE"
            print(f"Pin {pin}: {status}")
        directions = mcp_input.get_movement_directions()
        if directions:
            print("Movement directions:", directions)
        time.sleep(1)


if __name__ == "__main__":
    test_mcp_input()
