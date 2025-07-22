from Definições import *
from Processamento_do_input_do_jogador import *

class Principal(pygame.sprite.Sprite):
    def __init__(self, mapa, *groups):
        super().__init__(*groups)
        self.frames = {
            "parado": {
                "direita": importar_pasta("Grafismos","Personagem_Principal","Idle","Direita"),
                "esquerda": importar_pasta("Grafismos","Personagem_Principal","Idle","Esquerda")
            },
            "andar": {
                "direita": importar_pasta("Grafismos","Personagem_Principal","Walk_Cycle","Direita"),
                "esquerda": importar_pasta("Grafismos","Personagem_Principal","Walk_Cycle","Esquerda")
            },
            "salto": {
                "direita": importar_pasta("Grafismos","Personagem_Principal","Jump_Cycle","Direita"),
                "esquerda": importar_pasta("Grafismos","Personagem_Principal","Jump_Cycle","Esquerda")
            },
            "pendurado": {
                "direita": importar_pasta("Grafismos","Personagem_Principal","Hang_Cycle","Direita"),
                "esquerda": importar_pasta("Grafismos","Personagem_Principal","Hang_Cycle","Esquerda")
            }
        }
        # estados
        self.acção = "parado"
        self.lado = "direita"
        # frames
        self.indice_frame = 0
        self.frames_invencibilidade = 0
        self.image = self.frames[self.acção][self.lado][self.indice_frame]
        # referências
        self.mapa = mapa
        self.rect = self.image.get_frect(center = self.mapa.posição)
        self.rect_anterior = self.rect.copy()
        # movimentos
        self.direção = vector()
        self.velocidade = 400
        self.gravidade = 1400
        self.saltar = False
        self.altura_salto = 800
        self.no_chão = False
        # timers
        self.invencibilidade = Timer(3000)
        self.ignorar_input = Timer(500)
        # inventário
        self.inventário = {
            "Moedas": 0,
            "Itens": [],
            "Vidas": 3
        }
    
    def movimentação(self, dt):
        #* horizontal
        self.rect.centerx += self.direção.x * self.velocidade * dt
        self.colisão_mapa("horizontal")
        #* vertical
        self.direção.y += self.gravidade / 2 * dt
        self.rect.centery += self.direção.y * dt
        # repetição de linha necessária para simular aceleração de gravidade em vez de velocidade constante
        self.direção.y += self.gravidade / 2 * dt
        self.colisão_mapa("vertical")
        if self.saltar:
            if self.no_chão:
                self.direção.y = -self.altura_salto
            self.saltar = False
    
    def ver_contacto(self):
        rect_chão = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        rects_colisão = [sprite.rect for sprite in self.mapa.sprites_colisão]
        self.no_chão = True if rect_chão.collidelist(rects_colisão) >= 0 else False
    
    def colisão_mapa(self, eixo):
        for sprite in self.mapa.sprites_colisão:
            if sprite.rect.colliderect(self.rect):
                if eixo == "horizontal":
                    if self.rect.left <= sprite.rect.right and self.rect_anterior.left >= sprite.rect_anterior.right:
                        self.rect.left = sprite.rect.right
                    if self.rect.right >= sprite.rect.left and self.rect_anterior.right <= sprite.rect_anterior.left:
                        self.rect.right = sprite.rect.left
                elif eixo == "vertical":
                    if self.rect.top <= sprite.rect.bottom and self.rect_anterior.top >= sprite.rect_anterior.bottom:
                        self.rect.top = sprite.rect.bottom
                    if self.rect.bottom >= sprite.rect.top and self.rect_anterior.bottom <= sprite.rect_anterior.top:
                        self.rect.bottom = sprite.rect.top
                    self.direção.y = 0

    def animação(self, dt):
        if self.no_chão == False: self.acção = "salto"
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames[self.acção][self.lado]):
            self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][int(self.indice_frame)]
        if self.invencibilidade.activo:
            self.frames_invencibilidade += ANIMATION_SPEED * dt
            if int(self.frames_invencibilidade) % 4 == 0:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
        else:
            self.frames_invencibilidade = 0
            self.image.set_alpha(255)
    
    def interacção(self):
        self.rect.collidelist(self.mapa.lista_objectos["Moeda"])
        print(self.inventário)
    
    def collisão_entidades(self, dt):
        if self.rect.collidelist(self.mapa.lista_objectos["Moeda"]) > -1:
            moeda = self.rect.collidelist(self.mapa.lista_objectos["Moeda"])
            if self.mapa.lista_objectos["Moeda"][moeda].alive():
                self.mapa.lista_objectos["Moeda"][moeda].kill()
                self.inventário["Moedas"] += 1
        if not self.invencibilidade.activo:
            inimigos = self.mapa.lista_objectos["Vespa"] + self.mapa.lista_objectos["Tartaruga"]
            if self.rect.collidelist(inimigos) > -1:
                qual = self.rect.collidelist(inimigos)
                if inimigos[qual].alive():
                    self.invencibilidade.activar()
                    self.ignorar_input.activar()
                    self.inventário["Vidas"] -= 1
                    # self.bounce_away(dt, inimigos[qual])
    
    def bounce_away(self, dt, sprite):
        dist = vector()
        dist.x = self.rect.centerx - sprite.rect.centerx
        dist.y = -400
        self.direção = dist
        # self.rect.centerx += self.direção.x * self.velocidade * dt
        
        pass
    
    def verificar_estado(self):
        if not self.ignorar_input.activo:
            input_jogador(self)
        else:
            self.direção = vector()
        
        if self.inventário["Vidas"] == 0:
            print("GAME OVER")

    def update(self, dt):
        self.rect_anterior = self.rect.copy()
        self.invencibilidade.actualizar()
        self.ignorar_input.actualizar()
        self.verificar_estado()
        self.movimentação(dt)
        self.ver_contacto()
        self.collisão_entidades(dt)
        self.animação(dt)