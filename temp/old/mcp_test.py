import math
from smbus2 import SMBus
import time
from colorama import Fore, Style, init

init(autoreset=True)

# Initialize I2C bus (Raspberry Pi typically uses bus 1)
bus = SMBus(1)

PIN_DEFINITIONS = [
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

# If you want to set all pins as inputs with pull-ups:
IODIRA = 0x00  # I/O direction register for Port A
IODIRB = 0x01  # I/O direction register for Port B
GPPUA = 0x0C  # Pull-up enable register for Port A
GPPUB = 0x0D  # Pull-up enable register for Port B


def initialize_mcp(mcp_address):
    """
    Setzt alle Pins als Eingänge und aktiviert die Pull-ups.
    """
    try:
        bus.write_byte_data(mcp_address, IODIRA, 0xFF)  # Port A
        bus.write_byte_data(mcp_address, IODIRB, 0xFF)  # Port B
        bus.write_byte_data(mcp_address, GPPUA, 0xFF)
        bus.write_byte_data(mcp_address, GPPUB, 0xFF)
        print(f"{Fore.CYAN}Initialized MCP @ 0x{mcp_address:02X} as inputs + pull-ups.")
    except Exception as e:
        print(f"{Fore.RED}Failed to init MCP @ 0x{mcp_address:02X}: {e}")


def read_pin_state(pin_def):
    """
    Liest den Zustand eines Pins.
    Rückgabe: "LOW" (aktiv), "HIGH" (inaktiv) oder "ERR", falls ein Fehler auftritt.
    """
    try:
        reg_value = bus.read_byte_data(pin_def["mcpAddress"], pin_def["register"])
        state = reg_value & pin_def["mask"]
        return "LOW" if state == 0 else "HIGH"
    except Exception as e:
        return "ERR"


def main():
    # Alle verwendeten MCPs initialisieren
    unique_addresses = {pin_def["mcpAddress"] for pin_def in PIN_DEFINITIONS}
    for addr in unique_addresses:
        initialize_mcp(addr)

    # Dictionary zum Speichern der letzten Zustände; Schlüssel: Kombination aus MCP, Row, Col, PinName
    last_states = {}

    # Erster Durchlauf: Initialzustände erfassen (ohne Ausgabe)
    for pin in PIN_DEFINITIONS:
        key = f"{pin['mcpName']}_{pin['row']}_{pin['col']}_{pin['pinName']}"
        last_states[key] = read_pin_state(pin)

    # Endlosschleife: Prüfe periodisch auf Zustandsänderungen
    while True:
        changes = []
        for pin in PIN_DEFINITIONS:
            key = f"{pin['mcpName']}_{pin['row']}_{pin['col']}_{pin['pinName']}"
            current_state = read_pin_state(pin)
            if current_state != last_states[key]:
                changes.append((pin, last_states[key], current_state))
                last_states[key] = current_state  # Aktualisiere den gespeicherten Zustand

        # Ausgabe nur, wenn sich ein Zustand geändert hat
        if changes:
            print(f"\n{Style.BRIGHT}--- Changes Detected ---")
            print(f"{'MCP':<5} {'Row':<3} {'Col':<3} {'Pin':<4} {'Old':<8} {'New':<8}")
            print("-" * 50)
            for (pin, old, new) in changes:
                # Farbe abhängig vom neuen Zustand
                color_new = Fore.GREEN if new == "LOW" else Fore.RED
                color_old = Fore.GREEN if old == "LOW" else Fore.RED
                print(f"{pin['mcpName']:<5} {pin['row']:<3} {pin['col']:<3} {pin['pinName']:<4} "
                      f"{color_old}{old:<8}{Style.RESET_ALL} {color_new}{new:<8}{Style.RESET_ALL}")
        time.sleep(1)


if __name__ == "__main__":
    main()