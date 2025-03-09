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


def get_pin_status_str(pin_def):
    """
    Liest den Status eines Pins und gibt einen formatierten String zurück.
    Die gesamte Zeile wird farblich markiert, je nachdem, ob der Pin aktiv (LOW, grün)
    oder inaktiv (HIGH, rot) ist.
    Format: MCP   Row  Col  Pin   State
    """
    try:
        reg_value = bus.read_byte_data(pin_def["mcpAddress"], pin_def["register"])
        state = reg_value & pin_def["mask"]
        if state == 0:
            color = Fore.GREEN
            state_text = "LOW"
        else:
            color = Fore.RED
            state_text = "HIGH"
    except Exception as e:
        color = Fore.RED
        state_text = "ERR"
    # Die gesamte Zeile wird in der gewählten Farbe ausgegeben
    return f"{color}{pin_def['mcpName']:<5} {pin_def['row']:<3} {pin_def['col']:<3} {pin_def['pinName']:<4} {state_text:<8}{Style.RESET_ALL}"


def print_four_tables_side_by_side():
    """
    Teilt die Pin-Definitionen in vier Gruppen auf und gibt sie zeilenweise nebeneinander aus.
    Dabei erhält die zweite Tabelle einen etwas geringeren linken Einzug (3 Leerzeichen) als die anderen (4 Leerzeichen).
    """
    total = len(PIN_DEFINITIONS)
    per_table = math.ceil(total / 4)

    group1 = PIN_DEFINITIONS[0:per_table]
    group2 = PIN_DEFINITIONS[per_table:2 * per_table]
    group3 = PIN_DEFINITIONS[2 * per_table:3 * per_table]
    group4 = PIN_DEFINITIONS[3 * per_table:4 * per_table]

    header = f"{'MCP':<5} {'Row':<3} {'Col':<3} {'Pin':<4} {'State':<8}"
    separator = "-" * 30

    # Alle Tabellen erhalten einen linken Einzug; Tabelle 2 bekommt hier 3 Leerzeichen, die übrigen 4.
    indents = ["    ", "   ", "    ", "    "]

    def get_rows(group):
        return [get_pin_status_str(pin) for pin in group]

    rows1 = get_rows(group1)
    rows2 = get_rows(group2)
    rows3 = get_rows(group3)
    rows4 = get_rows(group4)

    # Falls eine Gruppe weniger Zeilen hat, mit Leerzeilen auffüllen
    max_rows = max(len(rows1), len(rows2), len(rows3), len(rows4))

    def pad_rows(rows):
        while len(rows) < max_rows:
            rows.append(" " * 30)
        return rows

    rows1 = pad_rows(rows1)
    rows2 = pad_rows(rows2)
    rows3 = pad_rows(rows3)
    rows4 = pad_rows(rows4)

    header_line = (f"{indents[0]}{header:<30}   "
                   f"{indents[1]}{header:<30}   "
                   f"{indents[2]}{header:<30}   "
                   f"{indents[3]}{header:<30}")
    sep_line = (f"{indents[0]}{separator:<30}   "
                f"{indents[1]}{separator:<30}   "
                f"{indents[2]}{separator:<30}   "
                f"{indents[3]}{separator:<30}")

    print(header_line)
    print(sep_line)

    for i in range(max_rows):
        line = (f"{indents[0]}{rows1[i]:<30}   "
                f"{indents[1]}{rows2[i]:<30}   "
                f"{indents[2]}{rows3[i]:<30}   "
                f"{indents[3]}{rows4[i]:<30}")
        print(line)


def main():
    unique_addresses = {pin_def["mcpAddress"] for pin_def in PIN_DEFINITIONS}
    for addr in unique_addresses:
        initialize_mcp(addr)

    while True:
        print(f"\n{Style.BRIGHT}--- Pin Status ---")
        print_four_tables_side_by_side()
        time.sleep(1)


if __name__ == "__main__":
    main()