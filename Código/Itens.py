from Definições import *

class Itens(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.frames = importar_pasta("Grafismos","Personagem_Principal","Idle","Direita")
        self.indice_frame = 0
        self.image = self.frames[self.indice_frame]
        self.rect = self.image.get_frect(center = pos)
        self.direção = vector()
    
    def movimentação(self, dt):
        self.rect.center += self.direção * 500 * dt

    def animação(self, dt):
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames):
            self.indice_frame = 0
        self.image = self.frames[int(self.indice_frame)]

    def update(self, dt):
        self.animação(dt)