from Definições import *

def input_jogador(jogador):
    if DEBUGGING:
        keys = pygame.key.get_pressed()
        input_vector = vector()
        other_action = "None"
        if any([keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_s], keys[pygame.K_w]]):
            if keys[pygame.K_a]:
                jogador.lado = "esquerda"
                jogador.acção = "andar"
                input_vector.x -= 1
            if keys[pygame.K_d]:
                jogador.lado = "direita"
                jogador.acção = "andar"
                input_vector.x += 1
            if keys[pygame.K_w]:
                jogador.acção = "salto"
                input_vector.y -= 1
            if keys[pygame.K_s]:
                input_vector.y += 1
        else: jogador.acção = "parado"
        if keys[pygame.K_SPACE]:
            jogador.interacção()
            jogador.interagir = True
        else:
            jogador.interagir = False
        jogador.direção = input_vector.normalize() if input_vector else input_vector
        
    else:
        #* Input via teclado
        keys = pygame.key.get_pressed()
        input_vector = vector()
        other_action = "None"
        if any([keys[pygame.K_a], keys[pygame.K_d]]):
            if keys[pygame.K_a]:
                jogador.lado = "esquerda"
                jogador.acção = "andar"
                input_vector.x -= 1
            if keys[pygame.K_d]:
                jogador.lado = "direita"
                jogador.acção = "andar"
                input_vector.x += 1
        else: jogador.acção = "parado"
        jogador.direção.x = input_vector.normalize().x if input_vector else input_vector.x
        if keys[pygame.K_w]:
                jogador.acção = "salto"
                jogador.saltar = True
        if keys[pygame.K_s]:
            jogador.interagir = True
            print("dialog")
        else:
            jogador.interagir = False
        # #* Input via rato
        # # if not jogador.no_chão:
        # if pygame.mouse.get_pressed()[0]:
        #     jogador.pendurar = True
        #     jogador.ponta_chicote = pygame.mouse.get_pos()
        # else:
        #     jogador.pendurar = False
        #     jogador.ponta_chicote = ()
