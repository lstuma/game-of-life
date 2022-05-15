import pygame
import pathlib

import game_of_life.ui as ui
from game_of_life.rule_simulation import RuleSimulator
from game_of_life.grid import Grid

__this_path__ = pathlib.Path('game_of_life.py').resolve()
__img_path__ = pathlib.Path(str(__this_path__).replace('game_of_life.py', '\\img', 1))


class Game(object):

    def __init__(self, debug=False):
        print(f'PATH ths: {__this_path__}')
        print(f'PATH img: {__img_path__}')
        # Debug parameter
        self.debug = debug

        # Initialize the game engine
        pygame.init()

        # The window bounds
        self.window_size = (1200, 900)

        # The grid for the game
        self.grid = None

        # Stores button states (mouse, keys)
        self.button_state: list = [False] * 4

        # Stores UI button rects
        self.ui_buttons: dict = dict()

        # Controls whether the simulation is currently playing
        self.simulation_state = False

        # The last selected pixel
        self.hover_pixel: tuple = (0, 0)

        # The screen which is being drawn upon
        self.screen = None

        # Instance of the RuleSimulator class, which will simulate the grid
        self.rule_simulator = None

        # Instance of the LayoutManager class, which will be used to handle boundaries etc.
        self.ui = None

        # Simulation speed
        self.simulation_speed = 10

        # Open the game window
        self.open_window()

    def open_window(self):
        # Create pygame screen (window)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Game Of Life')

        # Generate and draw grid
        self.grid = Grid(self.screen, pixel_size=20, constraints=(0.05, 0.05, 0.85, 0.95), debug=self.debug)

        # Instantiate RuleSimulator
        self.rule_simulator = RuleSimulator(grid=self.grid, debug=self.debug)

        # Draw buttons on window
        self.create_buttons()

        # Pass window to the main loop
        self.main_loop()

    def create_buttons(self):
        # Crete reset button
        self.ui_buttons['reset'] = ui.draw_button(screen=self.screen, constraints=(0.9, 0.05, 0.95, 0.3), text='RESET',
                                                  button_color=(10, 10, 10), text_color=(200, 200, 200),
                                                  outline_color=(20, 20, 20), outline_width=5, debug=self.debug)
        # Create slow down button
        self.ui_buttons['slow down'] = ui.draw_button(screen=self.screen, constraints=(0.9, 0.55, 0.95, 0.68), text='<',
                                                      button_color=(10, 10, 10), text_color=(200, 200, 200),
                                                      outline_color=(20, 20, 20), outline_width=5, debug=self.debug)
        # Create pause down button
        self.ui_buttons['pause'] = ui.draw_button(screen=self.screen, constraints=(0.9, 0.68, 0.95, 0.82), text='||',
                                                  button_color=(10, 10, 10), text_color=(200, 200, 200),
                                                  outline_color=(20, 20, 20), outline_width=5, debug=self.debug)
        # Create speed up button
        self.ui_buttons['speed up'] = ui.draw_button(screen=self.screen, constraints=(0.9, 0.82, 0.95, 0.95), text='>',
                                                     button_color=(10, 10, 10), text_color=(200, 200, 200),
                                                     outline_color=(20, 20, 20), outline_width=5, debug=self.debug)

    def multiple_event_handling(self, event):
        # Handle events separate from one another
        if isinstance(event, list):
            for event in event:
                return self.single_event_handling(event=event)
        else:
            return self.single_event_handling(event=event)

    def single_event_handling(self, event):
        # Get position of mouse in window
        mouse_pos = pygame.mouse.get_pos()

        # Quit event
        if event.type == pygame.QUIT:
            # Debug statement
            if self.debug:
                print('DEBUG: User closed window')
            # Return -1 to close the window
            return -1

        # Mouse movement event
        elif event.type == pygame.MOUSEMOTION:
            # Check if mouse click is in grid
            if self.grid.in_grid(mouse_pos):
                # Get position of pixel on grid
                self.hover_pixel = self.grid.get_pixel_from_cords(mouse_pos)
                # Toggle pixel in grid at mouse position if mouse button is being pressed
                if self.button_state[1] or self.button_state[3]:
                    self.grid.set_pixel(cords=self.hover_pixel, state=self.button_state[1])

            # If mouse is not in grid reset button states (less buggy)
            if not self.grid.in_grid(mouse_pos):
                self.button_state = [False for i in range(0, len(self.button_state))]

        # Mouse button down event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.button_state[event.button] = True

            # Check if button is primary mouse button
            if event.button == 1:
                # Check if mouse is on reset button
                if ui.pos_in_rect(pos=mouse_pos, rect=self.ui_buttons['reset']) and event.button == 1:
                    self.reset_grid()
                # Check if mouse is on slow down button
                elif ui.pos_in_rect(pos=mouse_pos, rect=self.ui_buttons['slow down']) and event.button == 1:
                    if self.simulation_speed > 1:
                        self.simulation_speed -= 3
                # Check if mouse is on pause button
                elif ui.pos_in_rect(pos=mouse_pos, rect=self.ui_buttons['pause']) and event.button == 1:
                    self.simulation_state = not self.simulation_state
                # Check if mouse is on speed up button
                elif ui.pos_in_rect(pos=mouse_pos, rect=self.ui_buttons['speed up']) and event.button == 1:
                    if self.simulation_speed < 20:
                        self.simulation_speed += 3

        # Mouse button up event
        elif event.type == pygame.MOUSEBUTTONUP:
            # Check if mouse click is in grid
            if self.grid.in_grid(mouse_pos):
                # Set hover pixel to correct state
                self.grid.set_pixel(cords=self.hover_pixel, state=self.button_state[1])
                self.button_state[event.button] = False

        # Key down event
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.simulation_state = not self.simulation_state

    def reset_grid(self):
        # Iterate through all enabled pixels
        for pixel in self.grid.enabled_pixels.copy():
            # Disable all enabled pixels
            self.grid.set_pixel(pixel, False)

    def main_loop(self):
        # The clock controls the max frame rate
        clock = pygame.time.Clock()
        # Limit to 60 fps
        clock.tick(60)

        # Bool storing whether the window is still open
        window_open = True

        # Time since last simulation cycle
        last_sym = 0

        # Debug statement
        if self.debug:
            print('DEBUG: Window creation and setup done, entering main window')

        # The actual main loop
        while window_open:

            # Handle events
            for event in pygame.event.get():
                # Handle events
                if self.multiple_event_handling(event) == -1:
                    # Set window open to false => breaks main loop
                    window_open = False

            # Switch buffers
            pygame.display.flip()

            # Update time since last simulation cycle
            last_sym += clock.get_time()
            # Check if time since last simulation cycle is over threshold
            if self.simulation_state and last_sym > 700 / self.simulation_speed * 10:
                # Reset time since last simulation cycle
                last_sym = 0
                # Simulate rules of the game on grid
                self.rule_simulator.simulate_cycle()

        # Stop the pygame game engine
        pygame.quit()


def main():
    Game(debug=True)


if __name__ == '__main__':
    main()
