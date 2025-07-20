from Definições import *

def input_jogador():
        keys = pygame.key.get_pressed()
        input_vector = vector()
        other_action = "None"
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_w]:
            input_vector.y -= 1
        if keys[pygame.K_s]:
            input_vector.y += 1
        # if keys[pygame.K_SPACE]:
        #     other_action = "collect"
        return [input_vector, other_action]