import pygame
from pytmx.util_pygame import load_pygame
from os.path import join
from os import walk
from pygame.math import Vector2 as vector
import random as rd

# Funções e classes auxiliares
def importar_pasta(*path):
    frames = []
    for pasta, subpasta, imagens in walk(join(*path)):
        for nome in sorted(imagens, key = lambda name: int(name.split(".")[0])):
            fullpath = join(pasta, nome)
            surf = pygame.image.load(fullpath).convert_alpha()
            frames.append(surf)
    return frames

class Timer:
    def __init__(self, duração, fun = None, repetir = False):
        self.duração = duração
        self.função = fun
        self.início = 0
        self.activo = False
        self.repetir = repetir
        
    def activar(self):
        self.activo = True
        self.início = pygame.time.get_ticks()
    
    def desactivar(self):
        self.activo = False
        self.início = 0
        if self.repetir:
            self.activar()
    
    def actualizar(self):
        tempo_actual = pygame.time.get_ticks()
        if tempo_actual - self.início >= self.duração:
            if self.função and self.início != 0:
                self.função()
            self.desactivar()

# Constantes
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
TILE_SIZE = 96
ANIMATION_SPEED = 10
HANDMADE_LEVELS = ["25", "50", "75", "100"]
EMPTY_EDGES = [12, 12]

DEBUGGING = True

# Activação do package pygame
pygame.init()

pygame.display.set_caption('Jogo de Escalada')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
