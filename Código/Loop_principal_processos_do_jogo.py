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
hud = HUD(jogador, False)

jogador.inventário["Moedas"] = 60
# if mapa.name == "Tutorial":
#     jogador.inventário["Moedas"] = 99999999
#     # make it show as [∞]
jogador.inventário["Item"] = ""
# jogador.inventário["Vidas"] = 1

while True:
    #* tick
    dt = clock.tick()/1000
    if dt >= 1: dt = 0.05
    screen.fill('black')
    #* eventos
    event_loop()
    #* verificações & updates
    mapa.check_transição(jogador)
    todos_sprites.update(dt)
    #* representações no ecrã
    todos_sprites.draw(jogador)
    hud.update()
    hud.draw(dt)
    vendedor = [i for i in todos_sprites.sprites() if isinstance(i, NPC)]
    if len(vendedor) > 0:
        vendedor = vendedor[0]
        if vendedor.em_conversa: vendedor.em_conversa.update()
    
    mapa.fade(dt, jogador)
    pygame.display.update()
