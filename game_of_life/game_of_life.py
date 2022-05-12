import pygame

from grid import Grid


class Game(object):

    def __init__(self, debug=False):
        # Debug parameter
        self.debug = debug

        # Initialize the game engine
        pygame.init()

        # The window size
        self.window_size = (1200, 900)

        # The grid for the game
        self.grid = None

        # Stores button states
        self.button_state: list = [False]*4

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
            # Set window open to false => breaks main loop
            window_open = False

        # Mouse movement event
        elif event.type == pygame.MOUSEMOTION:
            # Get position of mouse in window
            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse click is in grid
            if self.grid.act_constraints[0] < mouse_pos[1] < self.grid.act_constraints[2] and \
               self.grid.act_constraints[1] < mouse_pos[0] < self.grid.act_constraints[3]:
                # Get position of pixel on grid
                self.hover_pixel = ((mouse_pos[0] - self.grid.act_constraints[1]) // self.grid.pixel_size,
                                    (mouse_pos[1] - self.grid.act_constraints[0]) // self.grid.pixel_size)

                # Toggle pixel in grid at mouse position if mouse button is being pressed
                if self.button_state[1] or self.button_state[3]:
                    self.grid.set_pixel(cords=self.hover_pixel, state=self.button_state[1])

        # Mouse button down event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.button_state[1] = True
            elif event.button == 3:
                self.button_state[3] = True

        # Mouse button up event
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grid.set_pixel(cords=self.hover_pixel, state=self.button_state[1])
            self.button_state[event.button] = False

    def main_loop(self):
        # The clock controls the max frame rate
        clock = pygame.time.Clock()
        # Limit to 60 fps
        clock.tick(60)

        # Bool storing whether the window is still open
        window_open = True

        # The actual main loop
        while window_open:

            # Handle events
            for event in pygame.event.get():
                # Handle events
                self.event_handling(event)

            # Switch buffers
            pygame.display.flip()

        # Stop the pygame game engine
        pygame.quit()


def main():
    Game(debug=True)


if __name__ == '__main__':
    main()
