import pygame

import rule_simulation as simulation
from grid import Grid


class Game(object):

    def __init__(self, debug=False):
        # Debug parameter
        self.debug = debug

        # Initialize the game engine
        pygame.init()

        # The window bounds
        self.window_size = (1200, 900)

        # The grid for the game
        self.grid = None

        # Stores button states
        self.button_state: list = [False] * 4

        # Controls whether the simulation is currently playing
        self.simulation_state = False

        # The last selected pixel
        self.hover_pixel: tuple = tuple()

        # Open the game window
        self.open_window()

    def open_window(self):
        # Create pygame screen (window)
        screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Game Of Life')

        # Generate the grid
        self.grid = Grid(screen, pixel_size=10, constraints=(0.05, 0.05, 0.65, 0.95), debug=self.debug)

        # Pass window to the main loop
        self.main_loop()

    def event_handling(self, event):
        # Quit event
        if event.type == pygame.QUIT:
            # Debug statement
            if self.debug:
                print('DEBUG: User closed window')
            # Return -1 to close the window
            return -1

        # Mouse movement event
        elif event.type == pygame.MOUSEMOTION:
            # Get position of mouse in window
            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse click is in grid
            if self.grid.in_grid(mouse_pos):
                # Get position of pixel on grid
                self.hover_pixel = self.grid.get_pixel_from_cords(mouse_pos)
                # Toggle pixel in grid at mouse position if mouse button is being pressed
                if self.button_state[1] or self.button_state[3]:
                    self.grid.set_pixel(cords=self.hover_pixel, state=self.button_state[1])

        # Mouse button down event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.button_state[event.button] = True

        # Mouse button up event
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grid.set_pixel(cords=self.hover_pixel, state=self.button_state[1])
            self.button_state[event.button] = False

        # Key down event
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Debug statement
                if self.debug:
                    print('DEBUG: Changing simulation state')
                self.simulation_state = not self.simulation_state

    def main_loop(self):
        # The clock controls the max frame rate
        clock = pygame.time.Clock()
        # Limit to 60 fps
        clock.tick(60)

        # Bool storing whether the window is still open
        window_open = True

        # Time since last simulation cycle
        last_sym = 0

        # The actual main loop
        while window_open:

            # Handle events
            for event in pygame.event.get():
                # Handle events
                if self.event_handling(event) == -1:
                    # Set window open to false => breaks main loop
                    window_open = False

            # Switch buffers
            pygame.display.flip()

            # Simulate rules
            last_sym += clock.get_time()
            if self.simulation_state and last_sym > 700:
                last_sym = 0
                simulation.simulate_cycle(self.grid)

        # Stop the pygame game engine
        pygame.quit()


def main():
    Game(debug=True)


if __name__ == '__main__':
    main()
