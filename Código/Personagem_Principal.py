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
            }
        }
        #* estados
        self.acção = "parado"
        self.lado = "direita"
        #* frames
        self.indice_frame = 0
        self.frames_invencibilidade = 0
        self.image = self.frames[self.acção][self.lado][self.indice_frame]
        #* referências
        self.mapa = mapa
        self.rect = self.image.get_frect(center = self.mapa.posição)
        self.hitbox = self.rect.inflate(-16, 0)
        self.rect_anterior = self.hitbox.copy()
        #* movimentos
        self.direção = vector()
        self.velocidade = 400 if not DEBUGGING else 1200
        self.velocidade_calças = int(self.velocidade/3)
        self.gravidade = 1400
        self.saltar = False
        self.segundo_salto = False
        self.segundo_salto_dado = False
        self.altura_salto = 800
        self.no_chão = False
        self.bounce_away = False
        self.interagir = False
        #* timers
        self.invencibilidade = Timer(3000)
        self.ignorar_input = Timer(500)
        
        self.primeiro_salto = Timer(300)
        #* inventário
        self.max_vidas = 3
        self.inventário = {
            "Moedas": 0,
            "Item": "",
            "Vidas": 3
        }
    
    def movimentação(self, dt):
        if DEBUGGING:
            self.rect.center += self.direção * self.velocidade * dt
        else:
            if self.inventário["Item"] == "Calças":
                vel_actual = self.velocidade_calças
            else:
                vel_actual = self.velocidade
            #* horizontal
            self.hitbox.centerx += self.direção.x * vel_actual * dt
            self.colisão_mapa("horizontal")
            #* vertical
            self.direção.y += self.gravidade / 2 * dt
            self.hitbox.centery += self.direção.y * dt
            # repetição de linha necessária para simular aceleração de gravidade em vez de velocidade constante
            self.direção.y += self.gravidade / 2 * dt
            self.colisão_mapa("vertical")
            #* salto
            if self.saltar:
                if self.no_chão:
                    self.primeiro_salto.activar()
                    if self.inventário["Item"] == "Calças":
                        self.direção.y = -(9*self.altura_salto/10)
                    else:
                        self.direção.y = -self.altura_salto
            self.saltar = False
            self.altura_salto = 800
            
            if self.segundo_salto and not self.segundo_salto_dado:
                if self.inventário["Item"] == "Sapato":
                    if not self.primeiro_salto.activo:
                        self.direção.y = -self.altura_salto
                        self.segundo_salto_dado = True
            self.segundo_salto = False

            self.rect.center = self.hitbox.center
    
    def ver_contacto(self):
        rect_chão = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 2))
        rects_colisão = [sprite.rect for sprite in self.mapa.sprites_colisão]
        self.no_chão = True if rect_chão.collidelist(rects_colisão) >= 0 else False
        if self.no_chão: self.segundo_salto_dado = False
    
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
        if not self.no_chão:
            self.acção = "salto"
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
    
    def collisão_entidades(self, dt):
        if self.hitbox.collidelist(self.mapa.lista_objectos["Moeda"]) > -1:
            moeda = self.hitbox.collidelist(self.mapa.lista_objectos["Moeda"])
            if self.mapa.lista_objectos["Moeda"][moeda].alive():
                self.mapa.lista_objectos["Moeda"][moeda].kill()
                self.inventário["Moedas"] += 1
        if not DEBUGGING:
            if not self.invencibilidade.activo:
                if self.inventário["Item"] == "Apicultor":
                    inimigos = self.mapa.lista_objectos["Tartaruga"]
                elif self.inventário["Item"] == "Calças":
                    inimigos = self.mapa.lista_objectos["Vespa"]
                else:
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
        if self.inventário["Item"] == "Calças":
                vel_actual = self.velocidade_calças
        else:
            vel_actual = self.velocidade
        self.hitbox.centerx += self.direção.x * vel_actual * dt
        self.saltar = True
        self.no_chão = True
        self.altura_salto /= 2
        self.colisão_mapa("horizontal")
    
    def verificar_estado(self):
        if not self.ignorar_input.activo:
            input_jogador(self)
        
        if self.inventário["Vidas"] == 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))

    def update(self, dt):
        self.rect_anterior = self.hitbox.copy()
        self.invencibilidade.actualizar()
        self.ignorar_input.actualizar()
        self.primeiro_salto.actualizar()
        self.verificar_estado()
        self.movimentação(dt)
        self.ver_contacto()
        self.collisão_entidades(dt)
        self.animação(dt)