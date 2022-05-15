import pygame
import numpy as np

import game_of_life.ui as ui


class Grid(object):
    def __init__(self, screen, pixel_size, constraints=(0, 0, 1, 1), debug=False):
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
        # Amount of grid-pixels on the grid (x, y)
        self.bounds: tuple = (1, 1)

        # A list of the cords of all enabled pixels (otherwise all pixels would neet to be checked on every update)
        self.enabled_pixels = list()

        # Calculate absolute constraints of the grid in actual pixels
        self.act_constraints = ui.get_act_constraints(screen=self.screen, constraints=constraints, debug=self.debug)

        # The size of the grid in width and height
        self.grid_size = ui.get_size(act_constraints=self.act_constraints, debug=self.debug)

        # Dict of colors for the pixels
        self.pixel_color = dict()
        self.pixel_color[False] = ((10, 10, 10), (15, 15, 15))
        self.pixel_color[True] = ((200, 200, 200), (200, 200, 200))

        # Generate an empty grid
        self.gen_grid()

    def toggle_pixel(self, cords):
        # Toggle pixel state
        self.set_pixel(cords, not self.get_pixel(cords))

    def pixel_to_bounds(self, cords):
        cords = [cords[i] % self.bounds[i] for i in range(0, 2)]
        return tuple(cords)

    def set_pixel(self, cords, state):
        # Correct coordinates to fit grid bounds
        cords = self.pixel_to_bounds(cords)
        # Set pixel state
        self.grid[cords] = state
        if cords in self.enabled_pixels and not state:
            # Remove pixel from enabled_pixels list
            self.enabled_pixels.remove(cords)
        elif cords not in self.enabled_pixels and state:
            # Add to enabled pixels list
            self.enabled_pixels.append(cords)
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

    def in_grid(self, cords):
        # Return whether the position is in the grid
        return self.act_constraints[0] < cords[1] < self.act_constraints[2] and \
               self.act_constraints[1] < cords[0] < self.act_constraints[3]

    def get_pixel_from_cords(self, cords):
        return ((cords[0] - self.act_constraints[1]) // self.pixel_size,
                (cords[1] - self.act_constraints[0]) // self.pixel_size)

    def get_pixel(self, cords) -> bool:
        # Correct coordinates to fit grid bounds
        cords = self.pixel_to_bounds(cords)
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
            # Update x position in grid
            grid_pos[0] = 0
            for y in np.arange(self.act_constraints[1], self.act_constraints[3], self.pixel_size):
                # Creating rect for pixel
                rect = pygame.Rect(y, x, self.pixel_size, self.pixel_size)
                # Drawing pixel on buffer
                pygame.draw.rect(color=(self.pixel_color[self.get_pixel(tuple(grid_pos))][grid_pos[0] % 2 == grid_pos[1] % 2]), surface=self.screen, rect=rect,
                                 width=self.pixel_size)
                # Update x position in grid
                grid_pos[0] += 1

            # Update y position in grid
            grid_pos[1] += 1

        # Get size of grid
        self.bounds = tuple(grid_pos)

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
