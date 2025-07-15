from Definições import *
from Personagem_Principal import *

#* Para todos os processos relativos ao mapa do jogo e a itens representados no mesmo

class TodosSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = vector()
        
    def draw(self, player_center):
        self.offset.x = -(player_center[0] - SCREEN_WIDTH / 2)
        self.offset.y = -(player_center[1] - SCREEN_HEIGHT / 2)
        
        for sprite in self:
            self.display_surf.blit(sprite.image, sprite.rect.topleft + self.offset)

todos_sprites = TodosSprites()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Mapa:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.importar_dados()
        self.setup(self.tmx_maps["Mapa"], "Início")
    
    def importar_dados(self):
        self.tmx_maps = {
            "Mapa": load_pygame(join('Mapa','Dados','Mapa.tmx'))
        }
    
    def setup(self, tmx_map, player_start_pos):
        #* terrain
        for layer in ["Fundo", "Paredes"]:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.todos_sprites)
        #* entities
        for obj in tmx_map.get_layer_by_name("Entidades"):
            if obj.name == "Jogador" and obj.properties["Posição"] == player_start_pos:
                self.player = Principal((obj.x, obj.y), self.todos_sprites)