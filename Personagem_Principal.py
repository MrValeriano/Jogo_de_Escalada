import pygame
from Loop_principal_processos_do_jogo import screen
class Principal(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        rect = pygame.rect.Rect(600, 300, 10, 10)
        pygame.draw.rect(screen, "red", rect)