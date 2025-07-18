from Definições import *
from Processamento_do_input_do_jogador import input_jogador

class Principal(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("Grafismos/Personagem_Principal/Idle/pixil-frame-0.png")
        self.rect = self.image.get_frect(center = pos)
        self.direção = vector()
        self.lado = "right"
        self.indice_frame = 0
    
    def movimentação(self, dt):
        self.rect.center += self.direção * 500 * dt

    def animação(self, dt):
        self.indice_frame += 4 * dt
        self.image = self.frames[int(self.indice_frame % len(self.frames))]

    def update(self, dt):
        self.direção = input_jogador()
        self.movimentação(dt)
        self.animação(dt)