from game_of_life.grid import Grid


class RuleSimulator(object):
    def __init__(self, grid, debug=False):
        # Debug parameter
        self.debug = debug
        # The grid which will be simulated
        self.grid = grid

    def simulate_cycle(self):
        # Changes which wil be applied once the calculation of the cycle is done
        changes: list = list()
        # Only checking enabled pixels and their surroundings for changes
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
        # Returns the amount of living neighbour cells
        return sum([self.grid.get_pixel(pixel) for pixel in self.get_neighbours(cords=cords)])

    def get_neighbours(self, cords):
        # Getting the coordinates of all neighbours
        neighbours = [(cords[0] + x, cords[1] + y) for x in range(-1, 2) for y in range(-1, 2)]
        neighbours.remove(cords)
        return neighbours
