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
        self.hitbox = self.rect.inflate(-16, 0)
        self.rect_anterior = self.hitbox.copy()
        # movimentos
        self.direção = vector()
        self.velocidade = 400
        self.gravidade = 1400
        self.saltar = False
        self.altura_salto = 800
        self.no_chão = False
        self.bounce_away = False
        self.interagir = False
        # timers
        self.invencibilidade = Timer(3000)
        self.ignorar_input = Timer(500)
        # inventário
        self.inventário = {
            "Moedas": 0,
            "Item": "",
            "Vidas": 3
        }
    
    def movimentação(self, dt):
        if DEBUGGING:
            self.rect.center += self.direção * self.velocidade * dt
        else:
            #* horizontal
            self.hitbox.centerx += self.direção.x * self.velocidade * dt
            self.colisão_mapa("horizontal")
            #* vertical
            self.direção.y += self.gravidade / 2 * dt
            self.hitbox.centery += self.direção.y * dt
            # repetição de linha necessária para simular aceleração de gravidade em vez de velocidade constante
            self.direção.y += self.gravidade / 2 * dt
            self.colisão_mapa("vertical")
            if self.saltar:
                if self.no_chão:
                    self.direção.y = -self.altura_salto
                self.saltar = False
                self.altura_salto = 800
            self.rect.center = self.hitbox.center
    
    def ver_contacto(self):
        rect_chão = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 2))
        rects_colisão = [sprite.rect for sprite in self.mapa.sprites_colisão]
        self.no_chão = True if rect_chão.collidelist(rects_colisão) >= 0 else False
    
    def colisão_mapa(self, eixo):
        for sprite in self.mapa.sprites_colisão:
            if sprite.rect.colliderect(self.hitbox):
                if eixo == "horizontal":
                    if self.hitbox.left <= sprite.rect.right and self.rect_anterior.left >= sprite.rect_anterior.right:
                        self.hitbox.left = sprite.rect.right
                    if self.hitbox.right >= sprite.rect.left and self.rect_anterior.right <= sprite.rect_anterior.left:
                        self.hitbox.right = sprite.rect.left
                elif eixo == "vertical":
                    if self.hitbox.top <= sprite.rect.bottom and self.rect_anterior.top >= sprite.rect_anterior.bottom:
                        self.hitbox.top = sprite.rect.bottom
                    if self.hitbox.bottom >= sprite.rect.top and self.rect_anterior.bottom <= sprite.rect_anterior.top:
                        self.hitbox.bottom = sprite.rect.top
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
        print(self.inventário)
    
    def collisão_entidades(self, dt):
        if self.hitbox.collidelist(self.mapa.lista_objectos["Moeda"]) > -1:
            moeda = self.hitbox.collidelist(self.mapa.lista_objectos["Moeda"])
            if self.mapa.lista_objectos["Moeda"][moeda].alive():
                self.mapa.lista_objectos["Moeda"][moeda].kill()
                self.inventário["Moedas"] += 1
        if not DEBUGGING:
            if not self.invencibilidade.activo:
                inimigos = self.mapa.lista_objectos["Vespa"] + self.mapa.lista_objectos["Tartaruga"]
                if self.hitbox.collidelist(inimigos) > -1:
                    qual = self.hitbox.collidelist(inimigos)
                    if inimigos[qual].alive():
                        self.invencibilidade.activar()
                        self.ignorar_input.activar()
                        self.inventário["Vidas"] -= 1
                        self.bounce_away = True
                        self.bounce(dt,inimigos[qual])
    
    def bounce(self, dt, sprite):
        dist = vector()
        dist.x += self.hitbox.centerx - sprite.rect.centerx
        self.direção = dist.normalize()
        self.hitbox.centerx += self.direção.x * self.velocidade * dt
        self.saltar = True
        self.no_chão = True
        self.altura_salto /= 2
        self.colisão_mapa("horizontal")
    
    def verificar_estado(self):
        if not self.ignorar_input.activo:
            input_jogador(self)
        
        if self.inventário["Vidas"] == 0:
            print("GAME OVER")

    def update(self, dt):
        self.rect_anterior = self.hitbox.copy()
        self.invencibilidade.actualizar()
        self.ignorar_input.actualizar()
        self.verificar_estado()
        self.movimentação(dt)
        self.ver_contacto()
        self.collisão_entidades(dt)
        self.animação(dt)
        print(self.interagir)