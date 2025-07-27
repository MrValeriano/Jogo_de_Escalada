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
            self.frames_esgotado = importar_pasta("Grafismos", "Itens", "Esgotados", self.tipo)
            self.indice_frame = rd.choice(range(len(self.frames)))
            self.acção = "brilhar"
            self.image = self.frames[self.indice_frame]
            self.pos = (self.âncora[0], self.âncora[1] - self.image.height / 2)
        self.esgotado = False
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
            if self.esgotado:
                self.image = self.frames_esgotado[int(self.indice_frame)]
            else:
                self.image = self.frames[int(self.indice_frame)]
        else:
            self.image = self.frames[0]
    
    def compra(self):
        jogador = self.groups()[0].sprites()[-1]
        if self.tipo == "Coração":
            if jogador.inventário["Vidas"] == jogador.max_vidas:
                self.esgotado = True
            else:
                self.esgotado = False
        elif jogador.inventário["Item"] == self.tipo:
            self.esgotado = True
        else:
            self.esgotado = False
        if self.rect.colliderect(jogador.rect):
            if not self.esgotado:
                if jogador.interagir:
                    if jogador.inventário["Moedas"] >= Preços[self.tipo]:
                        if self.tipo == "Coração":
                            jogador.inventário["Vidas"] += 1
                        else:
                            jogador.inventário["Item"] = self.tipo
                        jogador.inventário["Moedas"] -= Preços[self.tipo]
                        self.esgotado = True
        
    
    def update(self, dt):
        if self.tipo == "Moeda":
            self.flutuar(dt)
        else:
            self.compra()
        self.animação(dt)

EQUIPAVEIS = ["Apicultor", "Calças", "Chicote"]
Preços = {
    "Apicultor": 15,
    "Calças": 15,
    "Chicote": 25,
    "Coração": 50
}