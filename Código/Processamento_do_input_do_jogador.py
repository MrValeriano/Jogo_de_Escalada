from Definições import *

def input_jogador(jogador):
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
        jogador.direção = input_vector