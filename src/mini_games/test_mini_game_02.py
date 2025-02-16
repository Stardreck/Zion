import pygame
import pymunk
import random
import math


class CableConnectionGame:
    """
    Cable Connection Mini-Game:
    The player must connect matching colored cable endpoints on a switchboard.
    Once all cables are connected, the door opens.
    """

    def __init__(self, screen, config):
        """
        Initialize the mini-game.

        :param screen: The pygame display Surface.
        :param config: Configuration dictionary (unused in this example but can be extended).
        """
        self.screen = screen
        self.config = config
        self.width, self.height = self.screen.get_size()

        # Initialize the physics simulation space (Pymunk)
        self.space = pymunk.Space()
        self.space.gravity = (0, 980)  # Gravity pointing downward

        # List of cable endpoints; each endpoint is a dict containing its pymunk body, shape, color, and connection state
        self.endpoints = []
        # List of established connections; each connection is a tuple of two endpoints
        self.connections = []

        # Currently selected endpoint (if any) for dragging
        self.selected_endpoint = None
        # Current drag line from the selected endpoint to the current cursor position
        self.drag_line = None

        # Door state: door is open when all cables are correctly connected
        self.door_open = False
        # Flag to mark that the mini-game is finished
        self.finished = False

        # Font for drawing text
        self.font = pygame.font.SysFont(None, 36)

        # Initialize game objects (cable endpoints)
        self.__init_endpoints()

    def __init_endpoints(self):
        """
        Initialize the cable endpoints on the switchboard.
        For demonstration, two pairs (four endpoints total) are created.
        """
        # Define positions for endpoints (two pairs) and their matching colors
        positions = [(150, 150), (450, 150), (150, 300), (450, 300)]
        colors = [(255, 0, 0), (255, 0, 0), (0, 255, 0), (0, 255, 0)]
        for pos, color in zip(positions, colors):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Circle(body, 20)
            shape.sensor = True  # Sensors do not generate collisions
            self.space.add(body, shape)
            self.endpoints.append({
                'body': body,
                'shape': shape,
                'color': color,
                'connected': False,
                'connection': None  # Will reference the connected endpoint once linked
            })

    def handle_event(self, event):
        """
        Process a single pygame event for touch/mouse interaction.
        The user taps an endpoint to select it, then drags and releases near another endpoint.

        :param event: A pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Check if the touch is near any unconnected endpoint
            for ep in self.endpoints:
                if not ep['connected']:
                    bx, by = ep['body'].position
                    if math.hypot(pos[0] - bx, pos[1] - by) < 25:
                        self.selected_endpoint = ep
                        break
        elif event.type == pygame.MOUSEMOTION:
            if self.selected_endpoint:
                self.drag_line = (self.selected_endpoint['body'].position, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected_endpoint:
                pos = event.pos
                target = None
                # Look for another endpoint of the same color that is near the release position
                for ep in self.endpoints:
                    if ep is not self.selected_endpoint and not ep['connected'] and ep['color'] == \
                            self.selected_endpoint['color']:
                        bx, by = ep['body'].position
                        if math.hypot(pos[0] - bx, pos[1] - by) < 25:
                            target = ep
                            break
                if target:
                    # Mark both endpoints as connected and record the connection
                    self.selected_endpoint['connected'] = True
                    target['connected'] = True
                    self.selected_endpoint['connection'] = target
                    target['connection'] = self.selected_endpoint
                    self.connections.append((self.selected_endpoint, target))
                # Reset the selection and drag line
                self.selected_endpoint = None
                self.drag_line = None

    def update(self, delta_time):
        """
        Update the physics simulation and check if the game is completed.

        :param delta_time: Time elapsed since the last frame.
        """
        self.space.step(delta_time)
        # If all endpoints are connected, mark the door as open and finish the game
        if all(ep['connected'] for ep in self.endpoints):
            self.door_open = True
            self.finished = True

    def draw(self):
        """
        Draw the mini-game elements on the screen.
        """
        # Clear the screen with a dark gray background
        self.screen.fill((30, 30, 30))
        # Draw the switchboard area (a rectangle)
        pygame.draw.rect(self.screen, (60, 60, 60), (100, 50, self.width - 200, 300))
        # Draw each cable endpoint as a circle
        for ep in self.endpoints:
            pos = ep['body'].position
            pygame.draw.circle(self.screen, ep['color'], (int(pos.x), int(pos.y)), 20)
        # Draw the connection lines between matched endpoints
        for ep1, ep2 in self.connections:
            pos1 = ep1['body'].position
            pos2 = ep2['body'].position
            pygame.draw.line(self.screen, ep1['color'], (int(pos1.x), int(pos1.y)), (int(pos2.x), int(pos2.y)), 8)
        # If the player is dragging a cable, draw a line from the selected endpoint to the cursor
        if self.drag_line:
            start, end = self.drag_line
            pygame.draw.line(self.screen, self.selected_endpoint['color'], (int(start.x), int(start.y)), end, 4)
        # Draw door status text at the bottom of the screen
        door_text = "Door Open!" if self.door_open else "Door Closed"
        text_surface = self.font.render(door_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, self.height - 50))

    def is_finished(self) -> bool:
        """
        Check if the mini-game is finished.

        :return: True if finished, otherwise False.
        """
        return self.finished

    def get_result(self) -> bool:
        """
        Get the result of the mini-game.

        :return: True if the door is open (win), otherwise False.
        """
        return self.door_open


# Example integration: Running the Cable Connection Mini-Game
def run_cable_connection_game():
    """
    Run the Cable Connection mini-game.
    This function creates a pygame window, instantiates the mini-game, and runs its loop.
    """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Kabelverbindung Mini-Spiel")
    clock = pygame.time.Clock()
    config = {}  # Placeholder configuration dictionary; can be extended as needed.
    mini_game = CableConnectionGame(screen, config)

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            mini_game.handle_event(event)
        mini_game.update(delta_time)
        mini_game.draw()
        pygame.display.flip()
        if mini_game.is_finished():
            running = False

    if mini_game.get_result():
        print("Mini-game won! Door opened.")
    else:
        print("Mini-game lost!")
    pygame.quit()


if __name__ == "__main__":
    run_cable_connection_game()
