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
        self.button_state: list = [False] * 4

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

    def simulate_cycle(self):
        # Changes which wil be applied once the calculation of the cycle is done
        changes: list = list()
        # Only checking ebabled pixels and their surroundings for changes
        for pixel in self.grid.enabled_pixels:
            # Rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            # Rule 2: Any live cell with two or three live neighbours lives on to the next generation.
            # Rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
            if self.get_neighbour_count(pixel) not in [2, 3]:
                changes.append(pixel)
            # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            for neighbour_pixel in self.get_neighbours(pixel):
                if not self.grid.get_pixel(neighbour_pixel) and self.get_neighbour_count(neighbour_pixel) == 3:
                    changes.append(neighbour_pixel)

        # Apply all change
        for pixel in changes:
            self.grid.toggle_pixel(cords=pixel)

    def get_neighbour_count(self, cords):
        return sum([self.grid.get_pixel(pixel) for pixel in self.get_neighbours(cords=cords)])

    @staticmethod
    def get_neighbours(cords):
        # Getting the coordinates of all neighbours
        neighbours = [(cords[0] + x, cords[1] + y) for x in range(-1, 2) for y in range(-1, 2)]
        neighbours.remove(cords)
        return neighbours

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
                self.simulate_cycle()

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
                if self.event_handling(event) == -1:
                    # Set window open to false => breaks main loop
                    window_open = False

            # Switch buffers
            pygame.display.flip()

        # Stop the pygame game engine
        pygame.quit()


def main():
    Game(debug=True)


if __name__ == '__main__':
    main()
