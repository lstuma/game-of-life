from grid import Grid


def simulate_cycle(grid):
    # Changes which wil be applied once the calculation of the cycle is done
    changes: list = list()
    # Only checking enabled pixels and their surroundings for changes
    for pixel in grid.enabled_pixels:
        # Rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # Rule 2: Any live cell with two or three live neighbours lives on to the next generation.
        # Rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
        if get_neighbour_count(pixel, grid) not in [2, 3]:
            changes.append(pixel)
        # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        for neighbour_pixel in get_neighbours(pixel, grid):
            if not grid.get_pixel(neighbour_pixel) and get_neighbour_count(neighbour_pixel, grid) == 3:
                changes.append(neighbour_pixel)

    # Apply all change
    for pixel in changes:
        grid.toggle_pixel(cords=pixel)


def get_neighbour_count(cords, grid):
    # Returns the amount of living neighbour cells
    return sum([grid.get_pixel(pixel) for pixel in get_neighbours(cords=cords, grid=grid)])


def get_neighbours(cords, grid):
    # Getting the coordinates of all neighbours
    neighbours = [(cords[0] + x, cords[1] + y) for x in range(-1, 2) for y in range(-1, 2)]
    neighbours.remove(cords)
    return neighbours
