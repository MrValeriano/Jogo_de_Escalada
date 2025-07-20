from Definições import *
from Mapa import *
from Itens import *
from NPCs import *
from Inimigos import *
from Loop_de_gestao_de_eventos import event_loop
from Personagem_Principal import *

mapa = Mapa()
jogador = Principal(mapa.posição, todos_sprites)
Inimigo("Tartaruga",mapa.lista_plataformas["1"][0], mapa, "1", todos_sprites)
Inimigo("Vespa",mapa.lista_plataformas["1"][5], mapa, "1", todos_sprites)
# Itens("Moeda", lista_plataformas["1"][6], todos_sprites)
# Itens("Moeda", lista_plataformas["1"][9], todos_sprites)

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
