import pygame
import sys
from .constants import *

class Button:
    selected_mode = 0
    selected_difficulty = 0
    selected_difficulty_two = 0
    def draw_button(win, x, y, width, height, text, button_color, border_color):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(win, button_color, rect,
                         border_radius=BORDER_RADIUS)

        # Add a border around the button
        pygame.draw.rect(win, border_color, rect, 3,
                         border_radius=BORDER_RADIUS)

        text_surface = FONT.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        win.blit(text_surface, text_rect)

    def is_mouse_over_button(x, y, width, height):
        mx, my = pygame.mouse.get_pos()
        return x <= mx <= x + width and y <= my <= y + height

    def draw_hover_button(win, x, y, width, height, text, button_color, hover_color):
        # Determine whether the mouse is over the button
        if Button.is_mouse_over_button(x, y, width, height):
            Button.draw_button(win, x, y, width, height, text,
                               hover_color, hover_color)
        else:
            Button.draw_button(win, x, y, width, height, text,
                               button_color, button_color)

    def exit_game():
        pygame.quit()
        sys.exit()
