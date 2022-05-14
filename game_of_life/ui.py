from typing import Optional

import pygame


def get_act_constraints(screen, constraints: tuple, debug=False) -> tuple:
    try:
        # Get the size of the window
        size = screen.get_size()
        # Calculate absolute constraints of the grid in actual pixels
        return tuple([constraints[x] * size[(x + 1) % 2] for x in range(0, len(constraints))])
    except Exception as e:
        # Debug statement
        if debug:
            print(f'WARNING: Could not convert relative constraints to absolute positions: {e}')
        return tuple()


def get_size(act_constraints: tuple, debug=False) -> tuple:
    # Get size of object from constraints in width and height
    size = (act_constraints[2] - act_constraints[0], act_constraints[3] - act_constraints[1])
    return size


def pos_in_rect(pos: tuple, rect: pygame.Rect) -> bool:
    # Get actual constrains of rect
    rect_act_constrains = (rect.left, rect.top, rect.right, rect.bottom)
    # Check if position is in rect
    return rect_act_constrains[0] < pos[0] < rect_act_constrains[2] and \
           rect_act_constrains[1] < pos[1] < rect_act_constrains[3]


def draw_button(screen, constraints: tuple, text: str = '', button_color=(200, 200, 200), text_color=(0, 0, 0),
                outline_color=None, outline_width=1, debug=False) -> pygame.Rect:
    # Get button constraints in actual pixels
    act_constraints = get_act_constraints(screen=screen, constraints=constraints, debug=debug)
    # Get button size in actual pixels
    size = get_size(act_constraints=act_constraints, debug=debug)
    # Create rect for button
    rect = pygame.Rect(act_constraints[1], act_constraints[0], size[1], size[0])
    # Draw rect
    pygame.draw.rect(screen, rect=rect, color=button_color)
    # Draw outline if available
    if outline_color:
        # Create rect for button
        rect = pygame.Rect(act_constraints[1]-outline_width, act_constraints[0]-outline_width, size[1]+2*outline_width, size[0]+2*outline_width)
        # Draw rect
        pygame.draw.rect(screen, rect=rect, color=outline_color, width=outline_width)
    # Instantiate font object
    font = pygame.font.SysFont(name='Arial', size=25, bold=True)
    # Create an image of the text using the font object
    img = font.render(text, True, text_color)
    # Get the size of the image
    img_size = img.get_size()
    # Render image and position it centered on the button
    screen.blit(img, (act_constraints[1] + size[1] / 2 - img_size[0] / 2,
                      act_constraints[0] + size[0] / 2 - img_size[1] / 2))
    # Return rect of button
    return rect
