import pygame
import sys


FPS = 50
WIDTH, HEIGHT = 500, 500

tile_images = {
            'wall': pygame.image.load('box.png'),
            'empty': pygame.image.load('grass.png')
        }
player_image = pygame.image.load('mar.png')
tile_width = tile_height = 50
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
        if not collect:
            self.rect.x -= maybe_x
            self.rect.y -= maybe_y
        elif collect.image == tile_images["wall"]:
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
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player


def start_screen(level):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Перемещение героя. Новый уровень")
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    change_cors_hero_x = 0
    change_cors_hero_y = 0
    camera = Camera()
    player = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif not player:
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    player = generate_level(level)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_cors_hero_x -= tile_width
                elif event.key == pygame.K_RIGHT:
                    change_cors_hero_x += tile_width
                elif event.key == pygame.K_UP:
                    change_cors_hero_y -= tile_height
                elif event.key == pygame.K_DOWN:
                    change_cors_hero_y += tile_height

        if player:
            screen.fill(pygame.Color("Black"))
            player.update(change_cors_hero_x, change_cors_hero_y)
            change_cors_hero_x, change_cors_hero_y = 0, 0

            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

        all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


name_map = "map_of_lesson.txt"
try:
    start_screen(load_level(name_map))
except FileNotFoundError:
    print(f"Карты {name_map} не существует")