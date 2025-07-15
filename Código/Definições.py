import pygame
from pytmx.util_pygame import load_pygame
from os.path import join

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
TILE_SIZE = 96
ANIMATION_SPEED = 6

pygame.display.set_caption('Jogo de Escalada')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
x, y = screen.get_size()

clock = pygame.time.Clock()