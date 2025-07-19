from Definições import *

class Itens(pygame.sprite.Sprite):
    def __init__(self, tipo, âncora, *groups):
        super().__init__(*groups)
        self.âncora = âncora
        self.frames = importar_pasta("Grafismos", "Itens", tipo)
        self.indice_frame = 0
        self.image = self.frames[self.indice_frame]
        self.pos = (self.âncora.rect.midtop[0], self.âncora.rect.midtop[1] - self.image.height)
        self.rect = self.image.get_frect(center = self.pos)
        self.direcção = vector()
        self.acção = "não brilhar"
        self.freq = ["brilhar"]*3 + ["não brilhar"]*7
    
    def flutuar(self, dt):
        pass
            
            
    def animação(self, dt):
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames):
            self.indice_frame = 0
            self.acção = rd.sample(self.freq,1)[0]
        if self.acção == "brilhar":
            self.image = self.frames[int(self.indice_frame)]
        else:
            self.image = self.frames[0]

    def update(self, dt):
        self.animação(dt)