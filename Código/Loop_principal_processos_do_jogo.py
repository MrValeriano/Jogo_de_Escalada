from Definições import *
from HUD import *
from Mapa import *
from Itens import *
from NPCs import *
from Inimigos import *
from Loop_de_gestao_de_eventos import event_loop
from Personagem_Principal import *

mapa = Mapa()
clock.tick()
jogador = Principal(mapa, todos_sprites)        
# jogador.inventário["Moedas"] = 60

while True:
    #* tick
    dt = clock.tick()/1000
    screen.fill('black')
    #* eventos
    event_loop()
    #* verificações & updates
    mapa.check_transição(jogador)
    todos_sprites.update(dt)
    #* representações no ecrã
    todos_sprites.draw(jogador)
    vendedor = [i for i in todos_sprites.sprites() if isinstance(i, NPC)]
    if len(vendedor) > 0:
        vendedor = vendedor[0]
        if vendedor.em_conversa: vendedor.em_conversa.update()
    
    mapa.fade(dt, jogador)
    pygame.display.update()
