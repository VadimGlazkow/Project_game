import pygame
import sys
import os
import random
import time
import datetime as dt

FPS = 60
WIDTH, HEIGHT = 1280, 720
SIZE_HERO = 50, 60
GRAVITY = 0.2

def load_image(name, file="tiles"):
    fullname = os.path.join(file, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'tree': pygame.transform.scale(load_image('tree.png'), (100, 100)),
    'fence': pygame.transform.scale(load_image('fence.png'), (100, 100)),
    'stone': pygame.transform.scale(load_image('stone.png'), (100, 100)),
    'grass': pygame.transform.scale(load_image('grass.png'), (100, 100)),
    'home': pygame.transform.scale(load_image('home.jpg'), (200, 200)),
    'spawn_one': pygame.transform.scale(load_image('spawn.png'), (200, 300)),
    'spawn_two_1': pygame.transform.flip(pygame.transform.scale(load_image('spawn.png'),
                                                              (200, 300)), True, False),
    'spawn_two_2': pygame.transform.flip(pygame.transform.scale(load_image('spawn.png'),
                                                              (200, 300)), True, False),
    'flower_one': pygame.transform.scale(load_image('flower_one.png'), (50, 50)),
    'flower_two': pygame.transform.scale(load_image('flower_two.png'), (50, 50)),
    'flower_three': pygame.transform.scale(load_image('flower_three.png'), (50, 50)),
    'flower_four': pygame.transform.scale(load_image('flower_four.png'), (50, 50)),
    'flower_five': pygame.transform.scale(load_image('flower_five.png'), (50, 50)),
    'grass_one': pygame.transform.scale(load_image('grass_one.png'), (50, 50)),
    'list': pygame.transform.scale(load_image('list.png'), (50, 50)),
    'mushroom_one': pygame.transform.scale(load_image('mushroom_one.png'), (50, 50)),
    'mushroom_two': pygame.transform.scale(load_image('mushroom_two.png'), (50, 50)),
    'priming': pygame.transform.scale(load_image('priming.png'), (50, 50)),
    'stump': pygame.transform.scale(load_image('stump.png'), (50, 50)),
    'fon': pygame.transform.scale(load_image('fon.jpg'), (5300, 3900)),
    'Start_onclick': pygame.transform.scale(load_image('Start_onclick.png', 'Start_menu'),
                                            (400, 120)),
    'Start_click': pygame.transform.scale(load_image('Start_click.png', 'Start_menu'),
                                          (400, 120)),
    'go_menu_onclick': pygame.transform.scale(load_image('go_menu_onclick.png', 'end'),
                                         (400, 120)),
    'go_menu_click': pygame.transform.scale(load_image('go_menu_click.png', 'end'),
                                         (400, 120)),
    'quit_onclick': pygame.transform.scale(load_image('quit_onclick.png', 'Start_menu'),
                                           (400, 120)),
    'quit_click': pygame.transform.scale(load_image('quit_click.png', 'Start_menu'),
                                         (400, 120)),
    'heart_life': pygame.transform.scale(load_image('heart_life.png'), (60, 50)),
    'heart_half': pygame.transform.scale(load_image('heart_half.png'), (60, 50)),
    'heart_died': pygame.transform.scale(load_image('heart_died.png'), (60, 50)),
    'apple': pygame.transform.scale(load_image('apple.png'), (25, 25)),
    'gold_apple': pygame.transform.scale(load_image('gold_apple.png'), (30, 30)),
    'apple_dark': pygame.transform.scale(load_image('apple_dark.png'), (25, 25)),
    'none': pygame.transform.scale(load_image('none.png'), (25, 25)),
    'logo': pygame.transform.scale(load_image('logo.png', 'Start_menu'), (50, 50)),
    'star': load_image('star.png', 'end')
}
player_image = pygame.transform.scale(load_image("hero_stand_down.png", "heros"), (100, 100))
monstr = pygame.transform.scale(load_image("monstr.png", "monstors"), (100, 100))
tile_width = tile_height = 100
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
animation_group = pygame.sprite.Group()
opponents = pygame.sprite.Group()
star_group = pygame.sprite.Group()
cord_spawn = []


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == "fon":
            super().__init__(all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.hit_point_object = 20
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn = True

    def update(self, maybe_x=0, maybe_y=0):
        self.rect.x += maybe_x
        self.rect.y += maybe_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.cor_x, self.cor_y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_point = 2.5
        self.eat_sing = pygame.mixer.Sound('Sing\eat.wav')
        self.eat_sing.set_volume(0.4)
        self.eat_gold_sing = pygame.mixer.Sound('Sing\gold.wav')
        self.apple_hit = pygame.mixer.Sound('Sing\/apple_hit.wav')
        self.died_sing = pygame.mixer.Sound('Sing\/died.wav')
        self.hp_plus = pygame.mixer.Sound('Sing\/hp_plus.wav')
        self.hp_plus.set_volume(0.3)
        self.hp_minus = pygame.mixer.Sound('Sing\/hp_minus.wav')
        self.hp_minus.set_volume(0.2)
        self.dict_stop_hero = {
            "up": pygame.transform.scale(load_image("hero_stand_up.png", "heros"), (100, 100)),
            "down": pygame.transform.scale(load_image("hero_stand_down.png", "heros"), (100, 100)),
            "right": pygame.transform.scale(load_image("hero_stand_right.png", "heros"), (100, 100))
        }
        self.dict_stop_hero["left"] = pygame.transform.flip(self.dict_stop_hero["right"], True, False)

        self.dict_go_hero = {
            "up": AnimatedSprite(pygame.transform.scale(load_image("hero_up.png", "heros"),
                                                             (900, 100)), 9, 1, 0, 0),
            "down": AnimatedSprite(pygame.transform.scale(load_image("hero_down.png", "heros"),
                                                               (900, 100)), 9, 1, 0, 0),
            "left": AnimatedSprite(pygame.transform.scale(load_image("hero_left.png", "heros"),
                                                               (900, 100)), 9, 1, 0, 0),
            "right": AnimatedSprite(pygame.transform.scale(load_image("hero_right.png", "heros"),
                                                                (900, 100)), 9, 1, 0, 0)
        }
        self.died = AnimatedSprite(pygame.transform.scale(load_image("died.png", "heros"),
                                                       (900, 100)), 8, 1, 0, 0)
        self.dict_hit_hero = {
            "up": AnimatedSprite(pygame.transform.scale(load_image("hero_hit_up.png", "heros"),
                                                        (600, 100)), 6, 1, 0, 0),
            "down": AnimatedSprite(pygame.transform.scale(load_image("hero_hit_down.png", "heros"),
                                                        (700, 100)), 7, 1, 0, 0),
            "left": AnimatedSprite(pygame.transform.scale(load_image("hero_hit_left.png", "heros"),
                                                          (700, 100)), 7, 1, 0, 0),
            "right": AnimatedSprite(pygame.transform.scale(load_image("hero_hit_right.png", "heros"),
                                                          (700, 100)), 7, 1, 0, 0)
        }
        self.move = "stop"
        self.direction = "down"

    def update(self, maybe_x=0, maybe_y=0, speed=tile_width // 25):
        self.rect.x += maybe_x
        self.rect.y += maybe_y
        for i in range(len(cord_spawn)):
            if cord_spawn[i] is not None:
                cord_spawn[i].x += maybe_x * -1
                cord_spawn[i].y += maybe_y * -1

        if self.move == "go":
            self.image = self.dict_go_hero[self.direction].image
            self.dict_go_hero[self.direction].update()
        elif self.move == "stop":
            self.image = self.dict_stop_hero[self.direction]
        elif self.move == "hit":
            self.image = self.dict_hit_hero[self.direction].image
            self.dict_hit_hero[self.direction].update()
            fotos = len(self.dict_hit_hero[self.direction].frames) - 1
            if self.dict_hit_hero[self.direction].cur_frame == fotos:
                self.move = "stop"
        elif self.move == 'died':
            self.image = self.died.image

            self.died.update()
            fotos = len(self.died.frames) - 1
            if self.died.cur_frame == fotos:
                self.died_sing.play()
                pygame.mixer.music.pause()
                time.sleep(1)
                game(level)

        self.mask = pygame.mask.from_surface(self.image)

        collect = False

        for sprite in tiles_group:
            if pygame.sprite.collide_mask(self, sprite):
                if sprite.image == tile_images["apple"]:
                    if self.move != "hit":
                        if self.hit_point < 5:
                            self.hit_point += 0.5
                            sprite.image = tile_images['none']
                            self.eat_sing.play()
                            self.hp_plus.play()
                    else:
                        sprite.image = tile_images['none']
                        self.apple_hit.play()
                elif sprite.image == tile_images['gold_apple']:
                    if self.move != "hit":
                        if self.hit_point < 5:
                            self.hit_point += 1
                            if self.hit_point > 5:
                                self.hit_point = 5
                            sprite.image = tile_images['none']
                            self.eat_gold_sing.play()
                            self.hp_plus.play()
                    else:
                        sprite.image = tile_images['none']
                        self.apple_hit.play()
                elif sprite.image == tile_images['apple_dark']:
                    if self.move != "hit":
                        self.hit_point -= 1
                        sprite.image = tile_images['none']
                        if self.hit_point > 0:
                            self.eat_sing.play()
                            self.hp_minus.play()
                        else:
                            self.died_sing.play()
                    else:
                        sprite.image = tile_images['none']
                        self.apple_hit.play()
                elif sprite.image in (tile_images["stone"], tile_images["tree"],
                                      tile_images["fence"], tile_images["home"],
                                      tile_images['spawn_one'],  tile_images['spawn_two_1'],
                                      tile_images['spawn_two_2']):
                    collect = True
                if sprite.image == tile_images['spawn_one'] and\
                        sprite.hit_point_object > 0 and self.move == 'hit':
                    sprite.hit_point_object -= 0.5
                    if sprite.hit_point_object <= 0:
                        sprite.kill()
                        cord_spawn[0] = None
                if sprite.image == tile_images['spawn_two_1'] and\
                        sprite.hit_point_object > 0 and self.move == 'hit':
                    sprite.hit_point_object -= 0.5
                    if sprite.hit_point_object <= 0:
                        sprite.kill()
                        cord_spawn[1] = None
                if sprite.image == tile_images['spawn_two_2'] and\
                        sprite.hit_point_object > 0 and self.move == 'hit':
                    sprite.hit_point_object -= 0.5
                    if sprite.hit_point_object <= 0:
                        sprite.kill()
                        cord_spawn[2] = None
                if collect:
                    break

        if collect:
            self.rect.x -= maybe_x
            self.rect.y -= maybe_y
            for i in range(len(cord_spawn)):
                if cord_spawn[i] is not None:
                    cord_spawn[i].x += maybe_x
                    cord_spawn[i].y += maybe_y

        new_x, new_y = SIZE_HERO

        self.rect.x += int(new_x * 1.5)
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.x -= int(new_x * 1.5)
        else:
            self.rect.x -= int(new_x * 1.5) + speed

        self.rect.x -= int(new_x * 1.5)
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.x += int(new_x * 1.5)
        else:
            self.rect.x += int(new_x * 1.5) + speed

        self.rect.y += int(new_y * 1.3)
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= int(new_y * 1.3)
        else:
            self.rect.y -= int(new_y * 1.3) + speed

        self.rect.y -= int(new_y * 1.3)
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y += int(new_y * 1.3)
        else:
            self.rect.y += int(new_y * 1.3) + speed


class Opponents(pygame.sprite.Sprite):
    dict_cor_walk = {'left': (-tile_width // 25, 0),
                     'right': (tile_width // 25, 0),
                     'up': (0, -tile_width // 25),
                     'down': (0, tile_width // 25)
                          }
    negative_direct = {'left': 'right', 'right': 'left',
                       'up': 'down', 'down': 'up'}

    def __init__(self, rect):
        super().__init__(opponents, all_sprites)
        self.rect = rect.copy()
        self.rect.x -= 1500
        self.rect.y -= 300
        self.image = monstr
        self.hp_minus = pygame.mixer.Sound('Sing\/hp_minus.wav')
        self.hp_minus.set_volume(0.2)
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_point = 2.5
        self.died_sing = pygame.mixer.Sound('Sing\/died.wav')

        self.dict_go_hero = {
            "up": AnimatedSprite(pygame.transform.scale(load_image("zombie_up.png", "monstors"),
                                                        (700, 100)), 7, 1, 0, 0),
            "down": AnimatedSprite(pygame.transform.scale(load_image("zombie_down.png", "monstors"),
                                                          (700, 100)), 7, 1, 0, 0),
            "left": AnimatedSprite(pygame.transform.scale(load_image("zombie_left.png", "monstors"),
                                                          (700, 100)), 7, 1, 0, 0),
            "right": AnimatedSprite(pygame.transform.scale(load_image("zombie_right.png", "monstors"),
                                                           (700, 100)), 7, 1, 0, 0)
        }
        self.died = AnimatedSprite(pygame.transform.scale(load_image("died.png", "heros"),
                                                     (900, 100)), 8, 1, 0, 0)
        self.access = {'left': False, 'right': False,
                       'up': False, 'down': False}
        self.score = 0
        self.cor_hero_bot = None
        self.back_go = False
        self.direction = None
        self.determine = 25
        self.hit_time = None
        self.first_hit = True
        self.commands_hero = None
        self.died_music = True

    def check_motion(self, speed=tile_width // 25):
        for sprite in tiles_group:
            if pygame.sprite.collide_mask(self, sprite):
                if sprite.image in (tile_images["stone"], tile_images["tree"],
                                    tile_images["fence"], tile_images["home"],
                                    tile_images['spawn_one'], tile_images['spawn_two_1'],
                                    tile_images['spawn_two_2']):
                    return False
        new_x, new_y = SIZE_HERO
        self.rect.x += int(new_x * 1.5)
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.x -= int(new_x * 1.5)
        else:
            self.rect.x -= int(new_x * 1.5) + speed
            return False

        self.rect.x -= int(new_x * 2.5)
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.x += int(new_x * 2.5)
        else:
            self.rect.x += int(new_x * 2.5) + speed
            return False

        self.rect.y += int(new_y * 1.3)
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= int(new_y * 1.3)
        else:
            self.rect.y -= int(new_y * 1.3) + speed
            return False

        self.rect.y -= int(new_y * 2.3)
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y += int(new_y * 2.3)
        else:
            self.rect.y += int(new_y * 2.3) + speed
            return False
        return True

    def update(self, target):
        if pygame.sprite.collide_mask(self, target):
            if self.hit_time and self.hit_point > 0:
                if len(self.commands_hero) >= random.choice((2, 2, 1)):
                    time_hit_other = dt.datetime.now()
                    if 'hit' in self.commands_hero:
                        self.hit_point = 0
                        self.first_hit = False
                    elif self.first_hit or\
                            (time_hit_other - self.hit_time).seconds >= 1.25:
                        self.first_hit = False
                        self.hp_minus.play()
                        target.hit_point -= 1
                        self.hit_time = dt.datetime.now()
                if target.move == 'hit':
                    if target.direction != self.direction:
                        self.commands_hero.append(target.move)
                    else:
                        self.commands_hero.append(None)
                else:
                    self.commands_hero.append(None)
            else:
                self.hit_time = dt.datetime.now()
                self.commands_hero = []
                self.first_hit = True
        else:
            self.hit_time = None
            self.commands_hero = None

        if self.score == 0:
            self.cor_hero_bot = [(self.rect.x, self.rect.y),
                                 (target.rect.x, target.rect.y)]
            self.rect.x -= 50
            self.access['left'] = self.check_motion()
            self.rect.x += 50

            self.rect.x += 50
            self.access['right'] = self.check_motion()
            self.rect.x -= 50

            self.rect.y -= 40
            self.access['up'] = self.check_motion()
            self.rect.y += 40

            self.rect.y += 40
            self.access['down'] = self.check_motion()
            self.rect.y -= 40

            if self.direction is None:
                if abs(self.rect.x - target.rect.x) > abs(self.rect.y - target.rect.y):
                    if self.rect.x > target.rect.x:
                        self.direction = 'left'
                    else:
                        self.direction = 'right'
                else:
                    if self.rect.y > target.rect.y:
                        self.direction = 'up'
                    else:
                        self.direction = 'down'

            lst_straw = []
            for straw in 'left right up down'.split():
                if straw == self.negative_direct[self.direction]:
                    if straw in ('left', 'right') and\
                            self.direction in ('left', 'right'):
                        if abs(self.rect.y - target.rect.y) <= 40 and\
                                self.access[self.negative_direct[self.direction]]:
                            new_straw = self.negative_direct[self.direction]
                            flag_new_straw = True
                            if new_straw == 'left':
                                if self.rect.x < target.rect.x:
                                    flag_new_straw = False
                            else:
                                if self.rect.x > target.rect.x:
                                    flag_new_straw = False
                            if flag_new_straw:
                                self.direction = new_straw
                                self.back_go = True
                                break
                    elif straw in ('up', 'down') and\
                            self.direction in ('up', 'down'):
                        if abs(self.rect.x - target.rect.x) <= 50 and\
                                self.access[self.negative_direct[self.direction]]:
                            new_straw = self.negative_direct[self.direction]
                            flag_new_straw = True
                            if new_straw == 'up':
                                if self.rect.y < target.rect.y:
                                    flag_new_straw = False
                            else:
                                if self.rect.y > target.rect.y:
                                    flag_new_straw = False
                            if flag_new_straw:
                                self.direction = new_straw
                                self.back_go = True
                                break
                elif straw != self.direction:
                    if self.access[straw]:
                        lst_straw.append(straw)
            dict_cor = {'left': abs(self.cor_hero_bot[0][0] - self.cor_hero_bot[1][0]),
                        'up': abs(self.cor_hero_bot[0][1] - self.cor_hero_bot[1][1])}
            dict_cor['right'] = dict_cor['left']
            dict_cor['down'] = dict_cor['up']
            if self.back_go:
                lst_straw = []
            if len(lst_straw) == 2:
                if not self.access[self.direction]:
                    if lst_straw[0] in ('left', 'right'):
                        if self.rect.x > target.rect.x:
                            self.direction = 'left'
                        else:
                            self.direction = 'right'
                    else:
                        if self.rect.y > target.rect.y:
                            self.direction = 'up'
                        else:
                            self.direction = 'down'
                else:
                    if dict_cor[lst_straw[0]] > dict_cor[self.direction]:
                        if lst_straw[0] in ('left', 'right'):
                            if self.rect.x > target.rect.x:
                                self.direction = 'left'
                            else:
                                self.direction = 'right'
                        else:
                            if self.rect.y > target.rect.y:
                                self.direction = 'up'
                            else:
                                self.direction = 'down'
            elif len(lst_straw) == 1:
                if not self.access[self.direction]:
                    self.direction = lst_straw[0]
                else:
                    if dict_cor[lst_straw[0]] > dict_cor[self.direction]:
                        if lst_straw[0] == 'left':
                            if self.rect.x > target.rect.x:
                                self.direction = lst_straw[0]
                        elif lst_straw[0] == 'right':
                            if self.rect.x <= target.rect.x:
                                self.direction = lst_straw[0]
                        elif lst_straw[0] == 'up':
                            if self.rect.y > target.rect.y:
                                self.direction = lst_straw[0]
                        elif lst_straw[0] == 'down':
                            if self.rect.y <= target.rect.y:
                                self.direction = lst_straw[0]
            elif not lst_straw:
                if not self.access[self.direction]:
                    self.direction = self.negative_direct[self.direction]
                self.back_go = False

        if not pygame.sprite.collide_mask(self, target):
            self.rect.x += self.dict_cor_walk[self.direction][0]
            self.rect.y += self.dict_cor_walk[self.direction][1]
            self.score += 1
            self.score %= self.determine
            if not self.check_motion():
                self.rect.x -= self.dict_cor_walk[self.direction][0]
                self.rect.y -= self.dict_cor_walk[self.direction][1]
                self.score = 0

        if (abs(self.rect.x - target.rect.x) <= 100 and
                abs(self.rect.y - target.rect.y) <= 100):
            self.determine = 1
        else:
            self.determine = 25

        if self.hit_point > 0:
            self.image = self.dict_go_hero[self.direction].image
            self.dict_go_hero[self.direction].update()
            self.mask = pygame.mask.from_surface(self.image)
        else:
            if self.died_music:
                self.died_sing.play()
                self.died_music = False
            self.image = self.died.image
            self.died.update()
            fotos = len(self.died.frames) - 1
            if self.died.cur_frame == fotos:
                self.kill()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(animation_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, new_x=0, new_y=0):
        self.rect.x, self.rect.y = new_x, new_y
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Particle(pygame.sprite.Sprite):
    fire = [tile_images['star']]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(star_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.screen_rect = (0, 0, WIDTH, HEIGHT)
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.screen_rect):
            self.kill()


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


def create_particles(position):
    particle_count = 5
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def generate_level(level):
    new_player = None
    flowes = ['flower_one', 'flower_two', 'flower_three', 'flower_four', 'flower_five',
              'grass_one', 'list', 'mushroom_one', 'mushroom_two', 'priming', 'stump']
    Tile('fon', -7, -6)
    for y in range(len(level) - 2, -1, -1):
        for x in range(len(level[y]) - 1, -1, -1):
            Tile('grass', x, y)
            if level[y][x] == '.':
                if random.randint(1, 10) in [1, 5, 2]:
                    num_flowers = random.randint(0, 10)
                    Tile(flowes[num_flowers], x, y).update(25, 25)
            elif level[y][x] == '#':
                Tile('fence', x, y)
            elif level[y][x] == '*':
                Tile('stone', x, y)
            elif level[y][x] == '+':
                Tile('tree', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '&':
                Tile('home', x, y)
            elif level[y][x] == '-':
                spawn = Tile('spawn_one', x, y)
                spawn = spawn.rect.copy()
                spawn.x -= 300
                cord_spawn.append(spawn)
            elif level[y][x] == '_':
                spawn = Tile('spawn_two_1', x, y)
                cord_spawn.append(spawn.rect.copy())
            elif level[y][x] == '/':
                spawn = Tile('spawn_two_2', x, y)
                cord_spawn.append(spawn.rect.copy())
            elif level[y][x] == '%':
                number = random.randint(1, 5)
                if (x, y) == (23, 9):
                    apple_ex = Tile('apple', x, y)
                    apple_ex.update(random.randint(0, 75), random.randint(0, 75))
                    apple_ex.spawn = False
                elif number == 1:
                    apple_ex = Tile('gold_apple', x, y)
                    apple_ex.update(random.randint(0, 70), random.randint(0, 70))
                elif number == 2:
                    apple_ex = Tile('apple_dark', x, y)
                    apple_ex.update(random.randint(0, 75), random.randint(0, 75))
                else:
                    apple_ex = Tile('apple', x, y)
                    apple_ex.update(random.randint(0, 75), random.randint(0, 75))

    return new_player, dt.datetime.now()


def make_new_apple():
    for sprite in all_sprites:
        if sprite.image == tile_images['none'] and sprite.spawn:
            number = random.randint(1, 5)
            if number == 1:
                sprite.image = tile_images["gold_apple"]
            elif number == 2:
                sprite.image = tile_images["apple_dark"]
            else:
                sprite.image = tile_images["apple"]


class Button:
    def __init__(self, image_one, image_two):
        self.image_one = image_one
        self.image_two = image_two

    def draw(self, text, x, y, screen, event1=None):
        mausx1, mausy1 = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mausx1 < x + 400 and y < mausy1 < y + 120:
            screen.blit(self.image_one, (x, y))
            if click[0]:
                if event1 is not None:
                    event1()
                else:
                    return True
        else:
            screen.blit(self.image_two, (x, y))


def start_game(screen):
    pygame.mixer.music.load('Sing\sing_start_menu.wav')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    fon = pygame.transform.scale(pygame.image.load('Start_menu\/fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    run = True
    start_btn = Button(tile_images['Start_click'], tile_images['Start_onclick'])
    quit_btn = Button(tile_images['quit_click'], tile_images['quit_onclick'])
    pygame.mouse.set_visible(False)
    image_mouse = load_image("mouse.png", "Start_menu")
    cor_mouse = 0, 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                cor_mouse = event.pos

        screen.blit(fon, (0, 0))
        rez = start_btn.draw("Начать игру", 100, 90, screen)
        quit_btn.draw('Выйти', 100, 230, screen, terminate)
        if pygame.mouse.get_focused():
            screen.blit(image_mouse, cor_mouse)
        if rez:
            pygame.mixer.music.pause()
            run = False
        pygame.display.flip()
        clock.tick(FPS)


def game_final(screen):
    pygame.mixer.music.pause()
    pygame.mixer.music.load('Sing\sound_end.wav')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    fon = pygame.transform.scale(pygame.image.load('end\/Win.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    start_btn = Button(tile_images['go_menu_click'], tile_images['go_menu_onclick'])
    quit_btn = Button(tile_images['quit_click'], tile_images['quit_onclick'])
    run = True
    pygame.mouse.set_visible(False)
    image_mouse = load_image("mouse.png", "Start_menu")
    cor_mouse = 0, 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                cor_mouse = event.pos

        create_particles((random.randint(0, 1280), random.randint(0, 220)))
        star_group.update()
        screen.blit(fon, (0, 0))
        star_group.draw(screen)

        rez = start_btn.draw("В главное меню", 30, 410, screen)
        quit_btn.draw('Выйти', 30, 520, screen, terminate)
        if pygame.mouse.get_focused():
            screen.blit(image_mouse, cor_mouse)
        if rez:
            pygame.mixer.music.pause()
            game(level)
        pygame.display.flip()
        clock.tick(FPS)


def life_point(screen, hit_point):
    heart_x, heart_y = 20, 20
    for heart in range(5):
        if hit_point > 0.5:
            screen.blit(tile_images['heart_life'], (heart_x + heart * 50, heart_y))
        if hit_point <= 0:
            screen.blit(tile_images['heart_died'], (heart_x + heart * 50, heart_y))
        if hit_point == 0.5:
            screen.blit(tile_images['heart_half'], (heart_x + heart * 50, heart_y))
        hit_point -= 1


def game(level):
    for i in opponents:
        i.kill()
    for sprite in all_sprites:
        sprite.kill()
    for sprite in tiles_group:
        sprite.kill()
    for sprite in animation_group:
        sprite.kill()
    for sprite in player_group:
        sprite.kill()
    cord_spawn.clear()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DEFENDER OF THE FOREST")
    pygame.display.set_icon(tile_images['logo'])
    start_game(screen)
    pygame.mixer.music.load('Sing\Led_Zeppelin_-_Immigrant_Song_Thor_Ragnarok-_soundtrack_62699723.mp3')
    pygame.mixer.music.set_volume(0.025)
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    camera = Camera()
    shift = False
    dict_go = {"left": [False, [-tile_width // 25, 0]],
               "right": [False, [tile_width // 25, 0]],
               "up": [False, [0, -tile_height // 25]],
               "down": [False, [0, tile_height // 25]]}
    list_side = []
    hit_sing = pygame.mixer.Sound('Sing\sing_hit.wav')
    go_sing = pygame.mixer.Sound('Sing\go_sing.wav')
    player, time_spawn_apple = generate_level(level)
    time_monster = dt.datetime.now()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    shift = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    dict_go["left"][0] = True
                    list_side.append("left")
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    dict_go["right"][0] = True
                    list_side.append("right")
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    dict_go["up"][0] = True
                    list_side.append("up")
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    dict_go["down"][0] = True
                    list_side.append("down")
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    start_game(screen)
                    pygame.mixer.music.unpause()
            elif event.type == pygame.KEYUP:
                directions = [("left", pygame.K_LEFT), ("right", pygame.K_RIGHT),
                              ("up", pygame.K_UP), ("down", pygame.K_DOWN), ('down', pygame.K_s),
                              ('up', pygame.K_w), ('left', pygame.K_a), ("right", pygame.K_d)]
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    shift = False
                for name_straw, button in directions:
                    if event.key == button:
                        del list_side[list_side.index(name_straw)]
                        dict_go[name_straw][0] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.move = "hit"
                    hit_sing.play()

        screen.blit(fon, (0, 0))

        command = 0
        for straw in dict_go:
            bool, value = dict_go[straw]
            if bool and not shift:
                if command % 9 == 0:
                    go_sing.play()
                player.update(*value)
                command += 1
            if bool and shift:
                for _ in range(2):
                    if _ == 0:
                        go_sing.play()
                    player.update(*value)
                    command += 1
        if player.move != "hit":
            if command:
                player.move = "go"
            else:
                player.move = "stop"
                player.update()
        if player.move == "hit":
            player.update()

        if list_side:
            player.direction = list_side[-1]

        if player.hit_point <= 0:
            player.move = 'died'
            player.update()

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        now_time = dt.datetime.now()
        if (dt.datetime.now() - time_spawn_apple).seconds >= 60:
            make_new_apple()
            time_spawn_apple = now_time
        if cord_spawn[2] == cord_spawn[1] == cord_spawn[0]:
            game_final(screen)
        if (dt.datetime.now() - time_monster).seconds >= 2 and\
                len(opponents) <= 15:
            time_monster = dt.datetime.now()
            num_ran = random.randint(0, 2)
            while cord_spawn[num_ran] is None:
                num_ran = random.randint(0, len(cord_spawn) - 1)
            Opponents(cord_spawn[num_ran])
        for sprite in opponents:
            sprite.update(player)

        all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)
        opponents.draw(screen)
        life_point(screen, player.hit_point)

        pygame.display.flip()
        clock.tick(FPS)


name_map = "map.txt"
try:
    level = load_level(name_map)
    game(level)
except FileNotFoundError:
    print(f"Карты {name_map} не существует")
