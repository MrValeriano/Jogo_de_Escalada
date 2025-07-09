import pygame

class Principal(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("Grafismos/Personagem_Principal/pixil-frame-0.png")
        self.rect = self.image.get_rect(center = (600, 300))