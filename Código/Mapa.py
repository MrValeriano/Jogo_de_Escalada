from Definições import *
from Personagem_Principal import *
from Itens import *
from Inimigos import *
from NPCs import *

#* Para todos os processos relativos ao mapa do jogo e a itens representados no mesmo

class TodosSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = vector()
        
    def draw(self, player_center):
        self.offset.x = EMPTY_EDGES[0]
        self.offset.y = -(player_center[1] - SCREEN_HEIGHT / 2)
        
        for sprite in self:
            self.display_surf.blit(sprite.image, sprite.rect.topleft + self.offset)

todos_sprites = TodosSprites()
fronteiras = []

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.rect_anterior = self.rect.copy()

class Porta(Sprite):
    def __init__(self, pos, surf, conn, *groups):
        super().__init__(pos, surf, *groups)
        self.target = conn

class Mapa:
    def __init__(self):
        self.importar_grafismos()
        self.lista_plataformas = {}
        self.sprites_colisão = pygame.sprite.Group()
        # self.ligações = {}
        # self.lojas = {}
        self.lista_objectos = {
            "Moeda":[],
            "Tartaruga":[],
            "Vespa":[]
        }
        self.setup("Mapa", "Início")
    
    def importar_grafismos(self):
        self.mapas_tmx = {
            "Mapa": load_pygame(join('Grafismos','Mapa','Dados','Mapa.tmx')),
            "Tutorial": load_pygame(join('Grafismos','Mapa','Dados','Tutorial.tmx')),
            "Loja": load_pygame(join('Grafismos','Mapa','Dados','Loja.tmx'))
        }
        self.plataformas_surf = {
            "Pequena": pygame.image.load(join('Grafismos','Mapa','Plataforma_pequena.png')),
            "Média": pygame.image.load(join('Grafismos','Mapa','Plataforma_media.png')),
            "Grande": pygame.image.load(join('Grafismos','Mapa','Plataforma_grande.png'))
        }
    
    def transição(self):
        pass
    
    def setup(self, nome_mapa, pos_inicial_jog):
        tmx_mapa = self.mapas_tmx[nome_mapa]
        lista_rects = {}
        #* fronteiras
        for area in tmx_mapa.get_layer_by_name("Bordas_Colisão"):
            rect = pygame.Rect(area.x, area.y, area.width, area.height)
            surf = pygame.Surface((area.width, area.height))
            Sprite((area.x, area.y), surf, (todos_sprites, self.sprites_colisão))
            # print(surf)
            fronteiras.append(rect)
        self.área_de_jogo = [
            int(tmx_mapa.get_layer_by_name("Área_de_Jogo")[0].x),
            int(tmx_mapa.get_layer_by_name("Área_de_Jogo")[0].x)+int(tmx_mapa.get_layer_by_name("Área_de_Jogo")[0].width)]
        #* fundo
        for layer in ["Fundo", "Paredes"]:
            for x, y, surf in tmx_mapa.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, todos_sprites)
        #* entidades
        if nome_mapa == "Mapa":
            for obj in tmx_mapa.get_layer_by_name("Entidades"):
                if obj.name == "Jogador" and obj.properties["Posição"] == pos_inicial_jog:
                    self.posição = (obj.x, obj.y)
                elif obj.name != "Jogador":
                    self.fim_do_jogo = Sprite((obj.x, obj.y), obj.image, (todos_sprites, self.sprites_colisão))
        else:
            for obj in tmx_mapa.get_layer_by_name("Entidades"):
                if obj.name == "Jogador" and obj.properties["Posição"] == pos_inicial_jog:
                    self.posição = (obj.x, obj.y)
                elif obj.name == "Vendedor":
                    self.vendedor = NPC((obj.x, obj.y), todos_sprites)
        
        #* plataformas base de cada nível - fixas no fundo de cada nível, em ambos os lados
        for area in tmx_mapa.get_layer_by_name("Níveis"):
            lista_rects.update({area.name:[]})
            self.lista_plataformas.update({area.name:[]})
            if area.name == "1": continue
            if area.name in HANDMADE_LEVELS: continue
            surf = self.plataformas_surf["Pequena"]
            for i in range(2):
                if i == 0:
                    coords = (area.x, ((area.y + area.height) - surf.height))
                else:
                    coords = (((area.x + area.width) - surf.width), ((area.y + area.height) - surf.height))
                plataforma = Sprite(coords, surf, (todos_sprites, self.sprites_colisão))
                lista_rects[area.name].append(plataforma)
                self.lista_plataformas[area.name].append(plataforma)
        #* plataformas aleatórias de cada nível
        for area in tmx_mapa.get_layer_by_name("Níveis"):
            if area.name in HANDMADE_LEVELS: continue
            # definir tamanho e limites da área útil para a geração de plataformas
            area_util = (int((area.width // TILE_SIZE) * TILE_SIZE) - int(TILE_SIZE),
                         int((area.height // TILE_SIZE) * TILE_SIZE))
            topleft = (int(area.x + ((area.width - area_util[0]) / 2)), int(area.y + TILE_SIZE))
            rightlimit = topleft[0] + area_util[0]
            # definir uma matriz de possíveis pontos de origem para as plataformas
            origens = []
            alturas = []
            rows = int(area_util[1]/(TILE_SIZE*2))
            cols = int(area_util[0]/TILE_SIZE)-1
            for i in range(rows):
                for j in range(cols):
                    origens.append((topleft[0] + ((TILE_SIZE)*j), topleft[1] + ((TILE_SIZE*2)*i)))
                alturas.append(topleft[1] + ((TILE_SIZE*2)*i))
            # definir plataformas no nível
            tamanhos_todos = ["Pequena", "Média", "Grande"]
            if int(area.name) < 25:
                tam_nível = tamanhos_todos[1:]
                freq = [4, 6]
            elif int(area.name) < 50:
                tam_nível = tamanhos_todos[1:2]
                freq = [3, 5]
            elif int(area.name) < 75:
                tam_nível = tamanhos_todos[0:2]
                freq = [2, 4]
            elif int(area.name) < 100:
                tam_nível = tamanhos_todos[0:1]
                freq = [1, 2]
            # pelo menos uma plataforma por altura, nos lados do ecrã
            lados = [topleft[0], topleft[0]+TILE_SIZE*(cols-1)]
            índice = rd.randint(0,1)
            for i in alturas:
                while True:
                    # tamanho = rd.sample(tam_nível, 1)[0]
                    tamanho = tamanhos_todos[0]
                    pt_origem = rd.sample(origens, 1)[0]
                    if pt_origem[1] != i: continue
                    if pt_origem[0] != lados[índice % len(lados)] :continue
                    surf = self.plataformas_surf[tamanho]
                    rect = surf.get_rect(topleft=pt_origem)
                    if rect.right > rightlimit: continue
                    l_buffer = pygame.rect.Rect(rect.right,rect.top, int(TILE_SIZE/2), TILE_SIZE)
                    r_buffer = pygame.rect.Rect((rect.left-int(TILE_SIZE/2)),rect.top, int(TILE_SIZE/2), TILE_SIZE)
                    break
                índice += 1
                plataforma = Sprite(pt_origem, surf, (todos_sprites, self.sprites_colisão))
                lista_rects[area.name].extend([plataforma, l_buffer, r_buffer])
                self.lista_plataformas[area.name].append(plataforma)
                origens.remove(pt_origem)
            # preencher o espaço restante com plataformas
            n_plataformas = rd.randint(freq[0], freq[1])
            for p in range(n_plataformas):
                tentativas = 0
                desistencia = False
                while True:
                    tentativas += 1
                    if tentativas == 100:
                        desistencia = True
                        origens.remove(pt_origem)
                        break
                    tamanho = rd.sample(tam_nível, 1)[0]
                    pt_origem = rd.sample(origens, 1)[0]
                    surf = self.plataformas_surf[tamanho]
                    rect = surf.get_rect(topleft=pt_origem)
                    if rect.right > rightlimit: continue
                    l_buffer = pygame.rect.Rect(rect.right,rect.top, int(TILE_SIZE/2), TILE_SIZE)
                    r_buffer = pygame.rect.Rect((rect.left-int(TILE_SIZE/2)),rect.top, int(TILE_SIZE/2), TILE_SIZE)
                    if rect.collidelist(lista_rects[area.name]) != -1: continue
                    break
                if desistencia: continue
                plataforma = Sprite(pt_origem, surf, (todos_sprites, self.sprites_colisão))
                lista_rects[area.name].extend([plataforma, l_buffer, r_buffer])
                self.lista_plataformas[area.name].append(plataforma)
                origens.remove(pt_origem)
        #* geração aleatória de inimigos/obstáculos
        for area in tmx_mapa.get_layer_by_name("Níveis"):
            if area.name in HANDMADE_LEVELS: continue
            if DEBUGGING:
                if area.name < HANDMADE_LEVELS[0]:
                    prob = 100
                else:
                    prob = 0
            else:
                if area.name < HANDMADE_LEVELS[0]:
                    prob = 10
                elif area.name < HANDMADE_LEVELS[1]:
                    prob = 20
                elif area.name < HANDMADE_LEVELS[2]:
                    prob = 40
                elif area.name < HANDMADE_LEVELS[3]:
                    prob = 60
            for plat in self.lista_plataformas[area.name]:
                if rd.sample(["sim", "não"], 1, counts=[prob, 100-prob])[0] == "sim":
                    tipo = rd.sample(["Vespa", "Tartaruga"], 1, counts=[50, 50])[0]
                    objecto = Inimigo(tipo, plat, self, "1", todos_sprites)
                    self.lista_objectos[tipo].append(objecto)
        #* geração aleatória de moedas
        for area in tmx_mapa.get_layer_by_name("Níveis"):
            if area.name in HANDMADE_LEVELS: continue
            if area.name < HANDMADE_LEVELS[0]:
                prob = 6
            elif area.name < HANDMADE_LEVELS[1]:
                prob = 4
            elif area.name < HANDMADE_LEVELS[2]:
                prob = 2
            elif area.name < HANDMADE_LEVELS[3]:
                prob = 1
            # definir pontos possíveis de origem
            pts_moedas = []
            alturas = list(set([i.rect.topleft[1] for i in self.lista_plataformas[area.name]]))
            alturas.sort()
            for pto_y in alturas:
                for pto_x in range(topleft[0], rightlimit, TILE_SIZE):
                    pts_moedas.append((pto_x + (TILE_SIZE/2), pto_y))
            # escolher quais serão usados para gerar moedas
            for pt in pts_moedas:
                if rd.sample(["sim", "não"], 1, counts=[prob, 100-prob])[0] == "sim":
                    pts_moedas.remove(pt)
                    objecto = Itens("Moeda", pt, todos_sprites)
                    self.lista_objectos["Moeda"].append(objecto)
        for obj in tmx_mapa.get_layer_by_name("Handmade"):
            if len(obj.properties.keys()) > 0:
                if obj.properties['type'] == "plataforma":
                    Sprite((obj.x, obj.y), obj.image, (todos_sprites, self.sprites_colisão))
                elif obj.properties['type'] == "porta":
                    Porta((obj.x, obj.y), obj.image, obj.properties["L"], todos_sprites)
