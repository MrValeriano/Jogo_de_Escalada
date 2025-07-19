from Definições import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, tipo, âncora, mapa, *groups):
        super().__init__(*groups)
        self.mapa = mapa
        self.âncora = âncora
        self.tipo = tipo
        self.frames = {
            "parado": {
                "direita": importar_pasta("Grafismos","Inimigos",tipo,"Idle","Direita"),
                "esquerda": importar_pasta("Grafismos","Inimigos",tipo,"Idle","Esquerda")
            },
            "andar": {
                "direita": importar_pasta("Grafismos","Inimigos",tipo,"Walk_Cycle","Direita"),
                "esquerda": importar_pasta("Grafismos","Inimigos",tipo,"Walk_Cycle","Esquerda")
            }
        }
        self.acção = "parado"
        self.lado = "direita"
        self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][self.indice_frame]
        if tipo == "Tartaruga":
            self.freq_actividades = ["andar", "parado"]
            self.pos = (self.âncora.rect.midtop[0], self.âncora.rect.midtop[1] - (self.image.height / 2))
        elif tipo == "Vespa":
            self.freq_actividades = ["andar", "andar", "andar", "parado"]
            self.pos = (self.âncora.rect.midtop[0], self.âncora.rect.midtop[1] - (3*self.image.height/2))
        self.rect = self.image.get_frect(center = self.pos)
        self.direção = vector()
        self.passo = 0
    
    def actividade(self, dt):
        #* esperar o fim da acção anterior
        if int(self.indice_frame) == 0:
            #* escolha aleatória de acção
            # para tartaruga: dentro da plataforma de âncora
            # para vespa: dentro da área de jogo
            if self.tipo == "Tartaruga":
                self.limite_área = [self.âncora.rect.left, self.âncora.rect.right]
                self.velocidade = 2
            elif self.tipo == "Vespa":
                self.limite_área = [self.mapa.área_de_jogo[0]+(TILE_SIZE/2), self.mapa.área_de_jogo[1]-(TILE_SIZE/2)]
                self.velocidade = 1000
            self.acção = rd.sample(self.freq_actividades, 1)[0]
            if self.rect.right >= self.limite_área[1]:
                self.lado = "esquerda"
            elif self.rect.left <= self.limite_área[0]:
                self.lado = "direita"
        if self.acção == "andar":
            if self.lado == "direita":
                self.direção.x += 1
                self.passo = 1
                if self.rect.right >= self.limite_área[1]:
                    self.direção = vector()
                    self.passo = 0
            elif self.lado == "esquerda":
                self.direção.x -= 1
                self.passo = -1
                if self.rect.left <= self.limite_área[0]:
                    self.direção = vector()
                    self.passo = 0
        else:
            self.direção = vector()
            self.passo = 0
        if self.tipo == "Tartaruga":
            self.rect.center += self.direção * self.velocidade * dt
        elif self.tipo == "Vespa":
            self.rect.centerx += self.passo * self.velocidade * dt

    def animação(self, dt):
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames[self.acção][self.lado]):
            self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][int(self.indice_frame)]

    def update(self, dt):
        self.actividade(dt)
        self.animação(dt)
