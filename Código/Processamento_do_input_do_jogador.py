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
            jogador.interacção()
            jogador.interagir = True
        else:
            jogador.interagir = False
        #* Input via rato
        mouse_pos = pygame.mouse.get_pos()
        # y do jogador é sempre o meio do ecrã
        # o ecrã é um rect que se move com o jogador no centro
        offset = vector()
        jogador_center = jogador.rect.center
        offset.x = -EMPTY_EDGES[0]
        if "Loja" not in jogador.mapa.name:
            offset.y = (jogador_center[1] - SCREEN_HEIGHT / 2)
        else:
            offset.y = jogador.mapa.altura / 2
        posição_real = mouse_pos + offset
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.line(pygame.display.get_surface(), "red", posição_real, jogador.rect.center, 5)
            print(jogador_center, posição_real)