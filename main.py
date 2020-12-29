import pygame
import sys
import os


FPS = 50
WIDTH, HEIGHT = 1280, 720


def load_image(name, colorkey=None):
    fullname = os.path.join("tiles", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


tile_images = {
            'tree': pygame.transform.scale(load_image('tree.png'), (100, 100)),
            'fence': pygame.transform.scale(load_image('fence.png', colorkey=-1), (100, 100)),
            'stone': pygame.transform.scale(load_image('stone.png', colorkey=-1), (100, 100)),
            'grass': pygame.transform.scale(load_image('grass.png', colorkey=-1), (100, 100))
        }
player_image = pygame.transform.scale(load_image('mar.png'), (60, 75))
tile_width = tile_height = 100
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.cor_x, self.cor_y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, maybe_x=0, maybe_y=0):
        self.rect.x += maybe_x
        self.rect.y += maybe_y

        collect = pygame.sprite.spritecollideany(self, tiles_group)
        print(collect)
        if not collect:
            self.rect.x -= maybe_x
            self.rect.y -= maybe_y
        elif collect.image == tile_images["stone"]:
            self.rect.x -= maybe_x
            self.rect.y -= maybe_y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile('grass', x, y)
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile('fence', x, y)
            elif level[y][x] == '*':
                Tile('stone', x, y)
            elif level[y][x] == '+':
                Tile('tree', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player


class Button:
    def __init__(self, width, height, octbut, nooctbut):
        self.width = width
        self.height = height
        self.octbut = octbut
        self.nooctbut = nooctbut

    def draw(self, text, x, y, screen, event1=None):
        mausx1, mausy1 = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mausx1 < x + self.width and y < mausy1 < y + self.height:
            pygame.draw.rect(screen, self.nooctbut, (x, y, self.width, self.height))
            font = pygame.font.Font(None, 40)
            text = font.render(text, True, (255, 0, 0))
            screen.blit(text, (x, y))
            if click[0]:
                if event1 is not None:
                    event1()
                else:
                    return True
        else:
            pygame.draw.rect(screen, self.octbut, (x, y, self.width, self.height))
            font = pygame.font.Font(None, 40)
            text = font.render(text, True, (255, 255, 255))
            screen.blit(text, (x, y))


def start_game(screen):
    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    run = True
    start_btn = Button(300, 70, (200, 0, 0), (255, 255, 255))
    quit_btn = Button(300, 70, (200, 0, 0), (255, 255, 255))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        rez = start_btn.draw("Начать игру", 100, 90, screen)
        quit_btn.draw('Выйти', 100, 200, screen, terminate)
        if rez:
            run = False
        pygame.display.flip()
        clock.tick(FPS)


def game(level):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Перемещение героя. Новый уровень")
    start_game(screen)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    change_cors_hero_x = 0
    change_cors_hero_y = 0
    camera = Camera()
    go = False
    player = generate_level(level)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_cors_hero_x -= tile_width // 4
                elif event.key == pygame.K_RIGHT:
                    change_cors_hero_x += tile_width // 4
                elif event.key == pygame.K_UP:
                    change_cors_hero_y -= tile_height // 4
                elif event.key == pygame.K_DOWN:
                    change_cors_hero_y += tile_height // 4
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    go = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    go = False

        screen.fill(pygame.Color("Black"))
        if go:
            player.update(change_cors_hero_x, change_cors_hero_y)
        else:
            change_cors_hero_x, change_cors_hero_y = 0, 0

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


name_map = "map.txt"
try:
    game(load_level(name_map))
except FileNotFoundError:
    print(f"Карты {name_map} не существует")