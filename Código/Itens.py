from Definições import *

class Itens(pygame.sprite.Sprite):
    def __init__(self, tipo, âncora, *groups):
        super().__init__(*groups)
        self.âncora = âncora
        self.tipo = tipo
        self.frames = importar_pasta("Grafismos", "Itens", self.tipo)
        if self.tipo == "Moeda":
            self.indice_frame = 0
            self.acção = "não brilhar"
            self.image = self.frames[self.indice_frame]
            self.pos = (self.âncora[0], self.âncora[1] - self.image.height)
        else:
            # self.pos = (self.âncora.rect.midtop[0], self.âncora.rect.midtop[1] - self.image.height)
            self.indice_frame = rd.choice(range(len(self.frames)))
            self.acção = "brilhar"
            self.image = self.frames[self.indice_frame]
            self.pos = (self.âncora[0], self.âncora[1] - self.image.height)
        self.rect = self.image.get_frect(center = self.pos)
        self.ymax_min = [self.rect.centery + 5, self.rect.centery - 5]
        self.movimento = vector()
        self.direção = "cima"
        self.freq = ["brilhar"]*3 + ["não brilhar"]*7
        if self.tipo == "Moeda":
            self.rect.centery = self.rect.centery + rd.choice(range(-5, 5))
    
    def flutuar(self, dt):
        if self.direção == "cima":
            self.movimento.y -= 1
            if self.rect.centery <= self.ymax_min[1]:
                self.direção = "baixo"
                self.movimento = vector()
        if self.direção == "baixo":
            self.movimento.y += 1
            if self.rect.centery >= self.ymax_min[0]:
                self.direção = "cima"
                self.movimento = vector()
        self.rect.center += self.movimento * 0.5 * dt
    
    def animação(self, dt):
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames):
            self.indice_frame = 0
            if self.tipo == "Moeda":
                self.acção = rd.sample(self.freq,1)[0]
        if self.acção == "brilhar":
            self.image = self.frames[int(self.indice_frame)]
        else:
            self.image = self.frames[0]
    
    def update(self, dt):
        if self.tipo == "Moeda":
            self.flutuar(dt)
        self.animação(dt)

EQUIPAVEIS = ["Apicultor", "Calças", "Chicote"]