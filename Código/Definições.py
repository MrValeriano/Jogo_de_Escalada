import pygame
from pytmx.util_pygame import load_pygame
from os.path import join
from pygame.math import Vector2 as vector
from random import sample
pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
TILE_SIZE = 96
ANIMATION_SPEED = 6
HANDMADE_LEVELS = ["25", "50", "75", "100"]

pygame.display.set_caption('Jogo de Escalada')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()