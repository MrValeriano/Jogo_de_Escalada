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
fronteiras = []
lista_plataformas = {}

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Mapa:
    def __init__(self):
        self.importar_grafismos()
        self.setup(self.mapas_tmx["Mapa"], "Início")
    
    def importar_grafismos(self):
        self.mapas_tmx = {
            "Mapa": load_pygame(join('Grafismos','Mapa','Dados','Mapa.tmx')),
            "Tutorial": load_pygame(join('Grafismos','Mapa','Dados','Tutorial.tmx'))
        }
        self.plataformas_surf = {
            "Pequena": pygame.image.load(join('Grafismos','Mapa','Plataforma_pequena.png')),
            "Média": pygame.image.load(join('Grafismos','Mapa','Plataforma_media.png')),
            "Grande": pygame.image.load(join('Grafismos','Mapa','Plataforma_grande.png'))
        }
    
    def setup(self, tmx_mapa, pos_inicial_jog):
        #* fundo
        for layer in ["Fundo", "Paredes"]:
            for x, y, surf in tmx_mapa.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, todos_sprites)
        #* entidades
        for obj in tmx_mapa.get_layer_by_name("Entidades"):
            if obj.name == "Jogador" and obj.properties["Posição"] == pos_inicial_jog:
                self.posição = (obj.x, obj.y)
            else:
                self.fim_do_jogo = Sprite((obj.x, obj.y), obj.image, todos_sprites)
        #* fronteiras
        for area in tmx_mapa.get_layer_by_name("Bordas_Colisão"):
            rect = pygame.Rect(area.x, area.y, area.width, area.height)
            fronteiras.append(rect)
        #* plataformas base de cada nível - fixas no fundo de cada nível, em ambos os lados
        for area in tmx_mapa.get_layer_by_name("Níveis"):
            lista_plataformas.update({area.name:[]})
            if area.name == "1": continue
            if area.name in HANDMADE_LEVELS: continue
            surf = self.plataformas_surf["Pequena"]
            for i in range(2):
                if i == 0:
                    coords = (area.x, ((area.y + area.height) - surf.height))
                else:
                    coords = (((area.x + area.width) - surf.width), ((area.y + area.height) - surf.height))
                plataforma = Sprite(coords, surf, todos_sprites)
                lista_plataformas[area.name].append(plataforma)
        #* plataformas aleatórias de cada nível
        for area in tmx_mapa.get_layer_by_name("Níveis"):
            if area.name in HANDMADE_LEVELS: continue
            print(f"\n{area.name}")
            # definir tamanho e limites da área útil para a geração de plataformas
            area_util = (int((area.width // TILE_SIZE) * TILE_SIZE),
                         int((area.height // TILE_SIZE) * TILE_SIZE))
            topleft = (int(area.x + ((area.width - area_util[0]) / 2)), int(area.y + TILE_SIZE))
            rightlimit = topleft[0] + area_util[0]
            # definir uma matriz de possíveis pontos de origem para as plataformas
            origens = []
            cols_rows = [int(i/(TILE_SIZE*2)) for i in area_util]
            for i in range(cols_rows[1]):
                for j in range(cols_rows[0]):
                    origens.append((topleft[0] + ((TILE_SIZE*2)*j), topleft[1] + ((TILE_SIZE*2)*i)))
            # definir plataformas no nível
            n_plataformas = rd.randint(cols_rows[1], cols_rows[0])
            for plat in range(n_plataformas):
                while True:
                    tamanho = rd.sample(list(self.plataformas_surf.keys()), 1)[0]
                    pt_origem = rd.sample(origens, 1)[0]
                    surf = self.plataformas_surf[tamanho]
                    rect = surf.get_rect(topleft=pt_origem)
                    if rect.right > rightlimit: continue
                    if rect.collidelist(lista_plataformas[area.name]) != -1: continue
                    break
                plataforma = Sprite(pt_origem, surf, todos_sprites)
                lista_plataformas[area.name].append(plataforma)
                origens.remove(pt_origem)
            # print(origens)
            
            