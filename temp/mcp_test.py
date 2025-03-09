import time
from smbus2 import SMBus
from colorama import Fore, Style, init

# Initialize colorama and I2C bus (Raspberry Pi typically uses bus 1)
init(autoreset=True)
bus = SMBus(1)

# Constants for MCP registers
IODIRA = 0x00  # I/O direction register for Port A
IODIRB = 0x01  # I/O direction register for Port B
GPPUA = 0x0C  # Pull-up enable register for Port A
GPPUB = 0x0D  # Pull-up enable register for Port B


def initialize_mcp(mcp_address):
    """
    Initialize an MCP device by setting all pins as inputs and enabling pull-ups.
    """
    try:
        bus.write_byte_data(mcp_address, IODIRA, 0xFF)  # Set Port A as inputs
        bus.write_byte_data(mcp_address, IODIRB, 0xFF)  # Set Port B as inputs
        bus.write_byte_data(mcp_address, GPPUA, 0xFF)  # Enable pull-ups on Port A
        bus.write_byte_data(mcp_address, GPPUB, 0xFF)  # Enable pull-ups on Port B
        print(f"{Fore.CYAN}Initialized MCP @ 0x{mcp_address:02X} as inputs with pull-ups.")
    except Exception as e:
        print(f"{Fore.RED}Failed to initialize MCP @ 0x{mcp_address:02X}: {e}")


class I2CPin:
    """Represents an individual pin on an MCP device."""

    def __init__(self, definition):
        self.row = definition["row"]
        self.col = definition["col"]
        self.mask = definition["mask"]
        self.pin_name = definition["pinName"]
        self.register = definition["register"]
        self.mcp_address = definition["mcpAddress"]
        self.mcp_name = definition["mcpName"]

    def get_key(self):
        """Generate a unique key for this pin."""
        return f"{self.mcp_name}_{self.row}_{self.col}_{self.pin_name}"

    def read_state(self):
        """
        Read the state of the pin.
        Returns 'LOW' if the bit is 0, 'HIGH' if not, or 'ERR' on error.
        """
        try:
            reg_value = bus.read_byte_data(self.mcp_address, self.register)
            state = reg_value & self.mask
            return "LOW" if state == 0 else "HIGH"
        except Exception:
            return "ERR"

    def __str__(self):
        # Format pin information for display
        return f"{self.mcp_name:<5} {self.row:<3} {self.col:<3} {self.pin_name:<4}"


class PinMonitor:
    """Monitors a collection of I2C pins and prints only when a state changes."""

    def __init__(self, pin_definitions):
        self.pins = [I2CPin(defn) for defn in pin_definitions]
        self.last_states = {}

    def initialize_devices(self):
        """
        Initialize all unique MCP devices and record the initial states.
        Prints the initial state of each pin.
        """
        unique_addresses = {pin.mcp_address for pin in self.pins}
        for addr in unique_addresses:
            initialize_mcp(addr)

        print(f"\n{Style.BRIGHT}Initial States:")
        print(f"{'MCP':<5} {'Row':<3} {'Col':<3} {'Pin':<4} {'State':<8}")
        print("-" * 40)
        for pin in self.pins:
            key = pin.get_key()
            state = pin.read_state()
            self.last_states[key] = state
            color = Fore.GREEN if state == "LOW" else Fore.RED
            print(f"{str(pin)} {color}{state:<8}{Style.RESET_ALL}")
        print("-" * 40)

    def check_for_changes(self):
        """
        Check each pin for state changes.
        If a change is detected, print the pin information along with the old and new states.
        """
        changes = []
        for pin in self.pins:
            key = pin.get_key()
            current_state = pin.read_state()
            if current_state != self.last_states.get(key):
                changes.append((pin, self.last_states.get(key), current_state))
                self.last_states[key] = current_state

        if changes:
            print(f"\n{Style.BRIGHT}--- Changes Detected ---")
            print(f"{'MCP':<5} {'Row':<3} {'Col':<3} {'Pin':<4} {'Old':<8} {'New':<8}")
            print("-" * 50)
            for pin, old, new in changes:
                color_old = Fore.GREEN if old == "LOW" else Fore.RED
                color_new = Fore.GREEN if new == "LOW" else Fore.RED
                print(f"{str(pin)} {color_old}{old:<8}{Style.RESET_ALL} {color_new}{new:<8}{Style.RESET_ALL}")
            print("-" * 50)

    def run(self, interval=3):
        """Continuously monitor the pins for changes, checking every `interval` seconds."""
        while True:
            self.check_for_changes()
            time.sleep(interval)


# Example pin definitions
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

if __name__ == "__main__":
    monitor = PinMonitor(PIN_DEFINITIONS)
    monitor.initialize_devices()
    monitor.run(interval=3)
