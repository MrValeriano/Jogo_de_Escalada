import pygame

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
x, y = screen.get_size()