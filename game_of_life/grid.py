import pygame

import numpy as np


class Grid(object):
    def __init__(self, screen, pixel_size, constraints = (0, 0, 1, 1), debug=False):
        # Debug parameter
        self.debug = debug

        # Dict containing all grid pixels
        self.grid: dict = dict()

        # The screen on which will be drawn
        self.screen = screen
        # The size of one individual pixel on the grid
        self.pixel_size = pixel_size
        # Relative constraints of the grid (which space of the window it will take up)
        self.constraints = constraints

        try:
            # Get the size of the window
            size = screen.get_size()
            # Calculate absolute constraints of the grid in pixels
            self.act_constraints = [self.constraints[x] * size[(x+1) % 2] for x in range(0, 4)]
        except Exception as e:
            # Debug statement
            if self.debug:
                print(f'WARNING: Could not convert relative constraints to absolute positions: {e}')
            return

        # The size of the grid in width and height
        self.grid_size = (self.act_constraints[2] - self.act_constraints[0],
                          self.act_constraints[3] - self.act_constraints[1])

        # Dict of colors for the pixels
        self.pixel_color = dict()
        self.pixel_color[False] = ((100, 100, 100), (150, 150, 150))
        self.pixel_color[True] = ((200, 200, 100), (200, 200, 100))

        # Generate an empty grid
        self.gen_grid()

    def toggle_pixel(self, cords):
        # Toggle pixel state
        self.grid[cords] = not self.get_pixel(cords)
        # Redraw the toggled pixel
        self.draw_pixel(cords=cords)

    def draw_pixel(self, cords):
        # Create rect for pixel
        rect = pygame.Rect(cords[0] * self.pixel_size + self.act_constraints[1],
                           cords[1] * self.pixel_size + self.act_constraints[0],
                           self.pixel_size, self.pixel_size)
        # Drawing pixel on buffer
        pygame.draw.rect(color=self.pixel_color[self.get_pixel(cords)][cords[0] % 2 == cords[1] % 2],
                         surface=self.screen, rect=rect, width=self.pixel_size)
        # Update only the rect
        pygame.display.update(rect)

    def get_pixel(self, cords) -> bool:
        # Check if pixel exists, otherwise generate one
        if cords not in self.grid.keys():
            self.grid[cords] = False
            return False
        # Return pixel state
        return self.grid[cords]

    def gen_grid(self):
        # Debug statement
        if self.debug:
            print('DEBUG: Drawing square grid')

        # The position in the grid
        grid_pos = [0, 0]
        for x in np.arange(self.act_constraints[0], self.act_constraints[2], self.pixel_size):
            for y in np.arange(self.act_constraints[1], self.act_constraints[3], self.pixel_size):
                # Creating rect for pixel
                rect = pygame.Rect(y, x, self.pixel_size, self.pixel_size)
                # Drawing pixel on buffer
                pygame.draw.rect(color=(self.pixel_color[self.get_pixel(tuple(grid_pos))][grid_pos[0] % 2 == grid_pos[1] % 2]), surface=self.screen, rect=rect,
                                 width=self.pixel_size)
                # Update position in grid
                grid_pos[0] += 1

            # Update position in the grid
            grid_pos[0] = 0
            grid_pos[1] += 1

        # Create the outline
        outline = pygame.Rect(self.act_constraints[1]-5,
                              self.act_constraints[0]-5,
                              self.grid_size[1]+10,
                              self.grid_size[0]+10)
        # Draw outline
        pygame.draw.rect(color=(200, 200, 200), surface=self.screen, rect=outline, width=5)

        # Update screen
        pygame.display.update()

        # Debug parameter
        if self.debug:
            print('DEBUG: Done drawing grid')