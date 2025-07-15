from Definições import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Mapa:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.import_assets()
        self.setup(self.tmx_maps["overworld"], "gamestart")
    
    def import_assets(self):
        self.tmx_maps = load_pygame(join('Mapa','Dados','overworld.tmx'))
    
    def setup(self, tmx_map, player_start_pos):
        #* terrain
        for layer in ["Terrain", "Terrain Top"]:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
        #* objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)
        #* entities
        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player" and obj.properties["pos"] == player_start_pos:
                self.player = Player((obj.x, obj.y), self.all_sprites)