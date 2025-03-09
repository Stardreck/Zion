import smbus
import time
from colorama import Fore, Style, init

init(autoreset=True)

# Initialize I2C bus (Raspberry Pi typically uses bus 1)
bus = smbus.SMBus(1)

PIN_DEFINITIONS = [
    {
        "coord": "0x0",
        "mask": 0x01,
        "pinName": "A0",
        "register": 0x12,  # 0x12 = GPIOA
        "mcpAddress": 0x20,  # e.g. MCP1
        "mcpName": "MCP1"
    },
    {
        "coord": "0x1",
        "mask": 0x02,
        "pinName": "A1",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "0x2",
        "mask": 0x04,
        "pinName": "A2",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "0x3",
        "mask": 0x08,
        "pinName": "A3",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "0x4",
        "mask": 0x10,
        "pinName": "A4",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "0x5",
        "mask": 0x20,
        "pinName": "A5",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "0x6",
        "mask": 0x40,
        "pinName": "A6",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "0x7",
        "mask": 0x80,
        "pinName": "A7",
        "register": 0x12,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "0x8",
        "mask": 0x01,
        "pinName": "B0",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "0x9",
        "mask": 0x02,
        "pinName": "B1",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "1x0",
        "mask": 0x04,
        "pinName": "B2",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "1x1",
        "mask": 0x08,
        "pinName": "B3",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "1x2",
        "mask": 0x10,
        "pinName": "B4",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },

    {
        "coord": "1x3",
        "mask": 0x20,
        "pinName": "B5",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "1x4",
        "mask": 0x40,
        "pinName": "B6",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },
    {
        "coord": "1x5",
        "mask": 0x80,
        "pinName": "B7",
        "register": 0x13,
        "mcpAddress": 0x20,
        "mcpName": "MCP1"
    },

]

# If you want to set all pins as inputs with pull-ups:
IODIRA = 0x00  # I/O direction register for Port A
IODIRB = 0x01  # I/O direction register for Port B
GPPUA = 0x0C  # Pull-up enable register for Port A
GPPUB = 0x0D  # Pull-up enable register for Port B


def initialize_mcp(mcp_address):
    """
    Example: Set all pins to inputs, enable pull-ups.
    Adjust as needed based on your actual hardware usage.
    """
    try:
        # All pins as inputs
        bus.write_byte_data(mcp_address, IODIRA, 0xFF)  # Port A
        bus.write_byte_data(mcp_address, IODIRB, 0xFF)  # Port B
        # Enable pull-ups on all pins
        bus.write_byte_data(mcp_address, GPPUA, 0xFF)
        bus.write_byte_data(mcp_address, GPPUB, 0xFF)
        print(f"{Fore.CYAN}Initialized MCP @ 0x{mcp_address:02X} as inputs + pull-ups.")
    except Exception as e:
        print(f"{Fore.RED}Failed to init MCP @ 0x{mcp_address:02X}: {e}")


def read_pin(pin_def):
    """
    Reads a single pin from the MCP.
    - pin_def["register"]: 0x12 (GPIOA) or 0x13 (GPIOB)
    - pin_def["mask"]: which bit to check
    - pin_def["mcpAddress"]: the I2C address
    - pin_def["pinName"]: a label like "A0" or "B7"
    - pin_def["mcpName"]: e.g. "MCP1"
    """
    try:
        # Read the register (GPIOA or GPIOB)
        reg_value = bus.read_byte_data(pin_def["mcpAddress"], pin_def["register"])

        # Apply the bitmask
        # If the result is 0, that pin is LOW; otherwise it's HIGH
        state = reg_value & pin_def["mask"]

        # Print the result
        if state == 0:
            print(f"{Fore.GREEN}{pin_def['mcpName']} {pin_def['coord']} - {pin_def['pinName']} is LOW (active).")
        else:
            print(f"{Fore.RED}{pin_def['mcpName']} {pin_def['coord']} - {pin_def['pinName']} is HIGH (inactive).")

    except Exception as e:
        print(f"{Fore.RED}Failed to read {pin_def['pinName']} on MCP @ 0x{pin_def['mcpAddress']:02X}: {e}")


def main():
    # 1) Identify all unique MCP addresses in your table
    unique_addresses = {pin_def["mcpAddress"] for pin_def in PIN_DEFINITIONS}

    # 2) Initialize each MCP (optional if you already have a config)
    for addr in unique_addresses:
        initialize_mcp(addr)

    # 3) Continuously read each pin in a loop
    while True:
        print(f"\n{Style.BRIGHT}--- Reading individual pins ---")
        for pin_def in PIN_DEFINITIONS:
            read_pin(pin_def)
        time.sleep(1)  # Wait 2 seconds before reading again


if __name__ == "__main__":
    main()
