from Definições import *
from Mapa import *
from Itens import *
from NPCs import *
from Inimigos import *
from Loop_de_gestao_de_eventos import event_loop
from Personagem_Principal import *

mapa = Mapa()
jogador = Principal(mapa.posição, todos_sprites)
tarta = Inimigo("Tartaruga",lista_plataformas["1"][0], mapa, todos_sprites)
vespa = Inimigo("Vespa",lista_plataformas["1"][3], mapa, todos_sprites)
# print(AREA_DE_JOGO)
while True:
    #* tick
    dt = clock.tick()/2000
    #* eventos
    event_loop()
    #* representações no ecrã
    todos_sprites.update(dt)
    screen.fill('black')
    todos_sprites.draw(jogador.rect.center)
    
    pygame.display.update()
