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

    def main_loop(self):
        # The clock controls the max frame rate
        clock = pygame.time.Clock()
        # Limit to 60 fps
        clock.tick(60)

        # Bool storing whether the window is still open
        window_open = True

        # Stores the last selected pixel in the grid
        selected_pixel: tuple = tuple()

        # Stores whether the primary mouse button is being pressed
        button_pressed: dict = dict()
        button_pressed['button 1'] = False
        button_pressed['button 3'] = False

        # The actual main loop
        while window_open:

            # Handle events
            for event in pygame.event.get():
                # Check which event we're dealing with

                # Quit events
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
                        # Get position on square grid
                        x = (mouse_pos[0] - self.grid.act_constraints[1]) // self.grid.pixel_size
                        y = (mouse_pos[1] - self.grid.act_constraints[0]) // self.grid.pixel_size
                        selected_pixel = (x, y)

                        # Toggle pixel in grid at mouse position if mouse button is being pressed
                        if button_pressed['button 1']:
                            self.grid.set_pixel(cords=selected_pixel, state=True)
                        elif button_pressed['button 3']:
                            self.grid.set_pixel(cords=selected_pixel, state=False)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        button_pressed['button 1'] = True
                    elif event.button == 3:
                        button_pressed['button 3'] = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        button_pressed['button 1'] = False
                        self.grid.set_pixel(cords=selected_pixel, state=True)
                    elif event.button == 3:
                        button_pressed['button 3'] = False
                        self.grid.set_pixel(cords=selected_pixel, state=False)

            # Switch buffers
            pygame.display.flip()

        # Stop the pygame game engine
        pygame.quit()


def main():
    Game(debug=True)


if __name__ == '__main__':
    main()
