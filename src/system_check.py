from __future__ import annotations

import random
import sys
import time
from typing import List, TYPE_CHECKING

import pygame
import pygame_gui
from pygame import Rect

from src.components.ui.ui_button import UIButton
from src.components.ui.ui_label import UILabel
from src.components.ui.ui_panel import UIPanel
from src.components.ui.ui_text_box import UITextBox

if TYPE_CHECKING:
    from src.star_engine import StarEngine


class SystemCheck:
    """
     Perform a system check,
     check the I2C connection on the RPI
     It verifies if MCP devices are responsive within the address range 0x20 to 0x27 (defined MCP addresses)
    """

    def __init__(self, engine: StarEngine, bus_number: int = 1) -> None:
        """
        Initializes the SystemCheck with the specified I2C bus number.
        :param bus_number: The I2C bus number (default is 1 for RPI).
        """
        self.engine = engine
        background_path: str = random.choice(self.engine.config.system_check_backgrounds)
        self.background_image = pygame.image.load(background_path).convert()
        self.bus_number = bus_number
        self.mcp_addresses = list(range(0x20, 0x28))  # Addresses from 0x20 to 0x27
        self.is_running: bool = False
        self.is_valid: bool = False
        self.is_init: bool = False

    def is_system_valid(self) -> bool:
        self.__show_system_message()
        return self.is_valid

    def __check_i2c_connection(self, device_address: int) -> bool:
        """
        Checks if an I2C device is responding at the given address.
        :param device_address: The I2C address of the device.
        :return: True if the device responds, otherwise False.
        """
        if sys.platform.startswith("linux"):
            try:
                from smbus2 import SMBus
                with SMBus(self.bus_number) as bus:
                    bus.write_quick(device_address)  # Attempt a quick write to check presence
                return True
            except Exception:
                return False

        return True

    def __show_system_message(self):
        self.__build_ui()

        description = "<b>Initialisiere Spielbrett</b><br/>"
        self.description.set_text(description)
        detected_mcps = []
        self.is_running = True
        while self.is_running:
            delta_time = self.engine.clock.tick(self.engine.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_system_check_running = False
                    return False
                self.engine.pygame_gui_ui_manager.process_events(event)
            # Update UI
            self.engine.pygame_gui_ui_manager.update(delta_time)
            self.engine.window.blit(self.background_image, (0, 0))
            self.engine.pygame_gui_ui_manager.draw_ui(self.engine.window)
            pygame.display.update()

            if len(detected_mcps) < len(self.mcp_addresses):
                addr = self.mcp_addresses[len(detected_mcps)]
                success = self.__check_i2c_connection(addr)
                if success:
                    self.is_valid = True
                    description += f"MCP mit der Adresse: {hex(addr)} initialisiert <br/>"
                else:
                    self.is_valid = False
                    description += f"<span style='color:red;'>MCP mit der Adresse: {hex(addr)} konnte nicht initialisiert werden</span> <br/>"

                detected_mcps.append(addr)
                self.description.set_text(description)
                print(
                    f"MCP mit der Adresse: {hex(addr)} {'initialisiert' if success else 'konnte nicht initialisiert werden'}")
                time.sleep(1)
            else:
                if not self.is_init:
                    self.is_init = True
                    if not self.is_valid:
                        description += F"<span style='color:red;'>Fehler bei Initialisierung, bitte den Raspberry Pi herunterfahren, die Stromversorgung für 5 Sekunden abschalten und erneut versuchen</span> <br/>"
                        self.description.set_text(description)
                        self.confirm_button.set_text("beenden")
                        self.confirm_button.enable()
                    else:
                        description += "Initialisierung abgeschlossen<br/>"
                        self.description.set_text(description)
                        self.confirm_button.set_text("starten")
                        self.confirm_button.enable()

    def __build_ui(self):
        # Create title label at the top
        title_rect = Rect(0, 60, 800, 100)
        self.title = UILabel(
            relative_rect=title_rect,
            text="Systemcheck",
            manager=self.engine.pygame_gui_ui_manager,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="planet_menu_title",
        )
        # Create a centered transparent background panel
        self.panel_bg = UIPanel(
            relative_rect=Rect(0, 50, 550, 480),
            manager=self.engine.pygame_gui_ui_manager,
            anchors={"center": "center"},
            object_id="default_panel_transparent"
        )

        # Create the inner panel for quiz content
        self.panel = UIPanel(
            relative_rect=Rect(0, 10, 530, 400),
            manager=self.engine.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="default_panel"
        )

        # Create the planet description text box
        self.description = UITextBox(
            relative_rect=Rect(0, 20, 500, 400),
            html_text="",
            manager=self.engine.pygame_gui_ui_manager,
            container=self.panel,
            anchors={"left": "left"},
        )

        # Create the confirm button
        confirm_rect = Rect(0, -60, 500, 50)
        self.confirm_button = UIButton(
            relative_rect=confirm_rect,
            text="Bitte warten...",
            manager=self.engine.pygame_gui_ui_manager,
            container=self.panel_bg,
            anchors={"centerx": "centerx", "bottom": "bottom"},
            object_id="panel_button",
        )
        self.confirm_button.disable()
        self.confirm_button.bind(pygame_gui.UI_BUTTON_PRESSED, lambda event: self.__kill_system_message())

    def __kill_system_message(self):
        self.is_running = False
        if self.title:
            self.title.kill()
        if self.panel:
            self.panel.kill()
        if self.panel_bg:
            self.panel_bg.kill()
        if self.confirm_button:
            self.confirm_button.kill()
