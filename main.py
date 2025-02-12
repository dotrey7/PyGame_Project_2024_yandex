import pygame
import sys
import os
import sqlite3
from pygame.math import Vector2
import random

SCREEN = WIDTH, HEIGHT = 800, 800
FPS = 60
BACKGROUND_COLOR = (13, 242, 97)
WOOD_COLOR = (149, 99, 13)
LOGIN_COLOR = (41, 58, 41)
TEXT_COLOR = (239, 239, 239)
TIMER_EVENT_TYPE = 30
pygame.init()
INDIAN_SOUND = pygame.mixer.Sound('data/click-for-game-menu-131903.mp3')
SLIDE_IN = pygame.mixer.Sound('data/click-button-app-147358.mp3')
EXIT_LOGIN_EVENT_TYPE = 31
cell_size = 40
cell_number = 20
game_font = pygame.font.Font(None, 25)


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print('Image not found:', fullname)
        sys.exit()
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (400, 300))
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()
    return image


class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        self.sprites.append(load_image('data/attack_1.png'))
        self.sprites.append(load_image('data/attack_2.png'))
        self.sprites.append(load_image('data/attack_3.png'))
        self.sprites.append(load_image('data/attack_4.png'))
        self.sprites.append(load_image('data/attack_5.png'))
        self.sprites.append(load_image('data/attack_6.png'))
        self.sprites.append(load_image('data/attack_7.png'))
        self.sprites.append(load_image('data/attack_8.png'))
        self.sprites.append(load_image('data/attack_9.png'))
        self.sprites.append(load_image('data/attack_10.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating:
            self.current_sprite += 0.25
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]


def draw_text(text, font, color, x, y, bold, size):
    font = pygame.font.SysFont(font, size, bold=bold)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


class Menu:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

    def render(self, screen):
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, WOOD_COLOR,
                         (0, self.height - 85,
                          self.width, self.height), 0)


class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def render(self, screen):
        btn = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, WOOD_COLOR, btn, border_radius=20)
        font = pygame.font.SysFont('Arial', 33)
        text = font.render(self.text, True, TEXT_COLOR)
        draw_text(self.text, 'Arial', TEXT_COLOR,
                  self.x + (self.width // 2 - text.get_width() // 2),
                  self.y + (self.height // 2 - text.get_height() // 2),
                  True, 33)

    def is_clicked(self, pos):
        x, y = pos
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return True
        return False

    def update_view(self, screen):
        btn = pygame.Rect(self.x - 5, self.y - 5, self.width + 10, self.height + 10)
        pygame.draw.rect(screen,
                         (WOOD_COLOR[0] - 1, WOOD_COLOR[1] - 1, WOOD_COLOR[2] - 1),
                         btn, border_radius=20)
        font = pygame.font.SysFont('Arial', 33)


def main_menu():
    log = login()
    screen.fill(BACKGROUND_COLOR)
    frog_sound = pygame.mixer.Sound('data/eating-sound-effect-36186.mp3')
    is_moved = False
    running = True
    men = Menu()
    frog_sprite = pygame.sprite.Group()
    frog = Animation(65, 415)
    frog_sprite.add(frog)
    play_button = Button(35, 45, 225, 50, "Play")
    options_button = Button(35, 125, 225, 50, "Options")
    scoreboard_button = Button(35, 205, 225, 50, "Scoreboard")
    check_for_collision = Button(112, 610, 100, 110, "")
    click = False
    updated = False
    clock = pygame.time.Clock()
    while running:
        pos = pygame.mouse.get_pos()
        updated = False

        if play_button.is_clicked(pos):
            if click:
                play_view(log)
            else:
                updated = True
                play_button.update_view(screen)
                if is_moved:
                    INDIAN_SOUND.play()
                    is_moved = False
        elif options_button.is_clicked(pos):
            if click:
                options_view()
            else:
                updated = True
                options_button.update_view(screen)
                if is_moved:
                    INDIAN_SOUND.play()
                    is_moved = False

        elif scoreboard_button.is_clicked(pos):
            if click:
                score_view()
            else:
                updated = True
                scoreboard_button.update_view(screen)
                if is_moved:
                    INDIAN_SOUND.play()
                    is_moved = False
        else:
            is_moved = True

        if check_for_collision.is_clicked(pos):
            if click:
                frog.animate()
                frog_sound.play()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        if not updated:
            men.render(screen)
        play_button.render(screen)
        options_button.render(screen)
        scoreboard_button.render(screen)
        frog_sprite.draw(screen)
        frog_sprite.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


def draw_play_view(screen, updated1=False, updated2=False):
    image1 = load_image('data/level1.png', -1)
    if not updated1:
        image1 = pygame.transform.scale(image1, (250, 250))
        draw_text('Level 1', None, TEXT_COLOR, 125, 220, True, 38)
    else:
        image1 = pygame.transform.scale(image1, (270, 270))
        draw_text('Level 1', None, TEXT_COLOR, 125, 220, True, 44)
    image2 = load_image('data/level2.png', -1)
    if not updated2:
        image2 = pygame.transform.scale(image2, (250, 250))
        draw_text('Level 2', None, TEXT_COLOR, 450, 220, True, 38)
    else:
        image2 = pygame.transform.scale(image2, (270, 270))
        draw_text('Level 2', None, TEXT_COLOR, 450, 220, True, 44)
    screen.blit(image1, (70, 260))
    screen.blit(image2, (400, 260))


def play_view(log):
    men = Menu()
    clicked = False
    exit_button = Button(20, 20, 120, 45, "Exit")
    running = True
    moved = False
    moved_2 = False
    image_rect = pygame.Rect(70, 260, 250, 250)
    image_rect2 = pygame.Rect(400, 260, 250, 250)
    while running:
        updated_1 = False
        updated_2 = False
        pos = pygame.mouse.get_pos()
        if exit_button.is_clicked(pos):
            if clicked:
                running = False
                INDIAN_SOUND.play()
        else:
            moved = True

        if image_rect.collidepoint(pos):
            updated_1 = True
            if moved_2:
                SLIDE_IN.play()
                moved_2 = False
            if clicked:
                level_one_loop(log)
        elif image_rect2.collidepoint(pos):
            updated_2 = True
            if moved_2:
                SLIDE_IN.play()
                moved_2 = False
            if clicked:
                level_two_loop(log)
        else:
            moved_2 = True

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        men.render(screen)
        exit_button.render(screen)
        draw_play_view(screen, updated_1, updated_2)
        pygame.display.flip()


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.transform.scale(load_image('data/head_up.png'), (40, 40))
        self.head_down = pygame.transform.scale(load_image('data/head_down.png'), (40, 40))
        self.head_right = pygame.transform.scale(load_image('data/head_right.png'), (40, 40))
        self.head_left = pygame.transform.scale(load_image('data/head_left.png'), (40, 40))
        self.head = self.head_up

        self.tail_up = pygame.transform.scale(load_image('data/tail_up.png'), (40, 40))
        self.tail_down = pygame.transform.scale(load_image('data/tail_down.png'), (40, 40))
        self.tail_right = pygame.transform.scale(load_image('data/tail_right.png'), (40, 40))
        self.tail_left = pygame.transform.scale(load_image('data/tail_left.png'), (40, 40))

        self.tail = self.tail_up
        self.body_vertical = pygame.transform.scale(load_image('data/body_vertical.png'), (40, 40))
        self.body_horizontal = pygame.transform.scale(load_image('data/body_horizontal.png'), (40, 40))

        self.body_tr = pygame.transform.scale(load_image('data/body_topright.png'), (40, 40))
        self.body_tl = pygame.transform.scale(load_image('data/body_topleft.png'), (40, 40))
        self.body_br = pygame.transform.scale(load_image('data/body_bottomright.png'), (40, 40))
        self.body_bl = pygame.transform.scale(load_image('data/body_bottomleft.png'), (40, 40))

        self.fail_cound = pygame.mixer.Sound('data/__kantouth__cartoon-bing-lo.wav')
        self.crunch_sound = pygame.mixer.Sound('data/poedanie-ukus-yabloka.wav')

    def draw_snake(self):
        self.update_head_graph()
        self.update_tail_graph()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                if previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

        # for block in self.body:
        #     x_pos = int(block.x * cell_size)
        #     y_pos = int(block.y * cell_size)
        #     snake_block = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        #     pygame.draw.rect(screen, (183, 111, 122), snake_block)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def update_head_graph(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graph(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_fall_cound(self):
        self.fail_cound.play()


class Fruit:
    def __init__(self):
        self.apple = pygame.transform.scale(load_image('data/apple.png', -1), (40, 40))
        self.clubnika = pygame.transform.scale(load_image('data/clubnika.png', -1), (40, 40))
        self.sliva = pygame.transform.scale(load_image('data/sliva.png', -1), (40, 40))
        self.arbuz = pygame.transform.scale(load_image('data/arbuz.png', -1), (40, 40))
        self.vishna = pygame.transform.scale(load_image('data/vishna.png', -1), (40, 40))
        self.banani = pygame.transform.scale(load_image('data/banani.png', -1), (40, 40))
        self.orange = pygame.transform.scale(load_image('data/orange.png', -1), (40, 40))
        self.limon = pygame.transform.scale(load_image('data/limon.png', -1), (40, 40))
        self.sp = [self.apple, self.clubnika, self.sliva, self.arbuz, self.vishna, self.banani, self.orange, self.limon]
        self.randomise()

    def draw_fruit(self):
        # прямоугольник

        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.sp[self.vibor], fruit_rect)
        # screen.blit(vibor, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomise(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.vibor = random.randint(0, 7)


class Wall:
    def __init__(self):
        self.one = True
        self.wall1 = pygame.transform.scale(load_image('data/wall1.png'), (40, 40))
        self.wall2 = pygame.transform.scale(load_image('data/wall2.png'), (40, 40))
        self.wall3 = pygame.transform.scale(load_image('data/wall3.png'), (40, 40))
        self.lis = [self.wall1, self.wall3, self.wall2]
        self.walls = list()
        self.rand()

    def draw_wall(self):
        # прямоугольник
        self.map_generate()
        self.generate_place()
        for i in self.walls:
            wall_rect = pygame.Rect(i[0] * cell_size, i[1] * cell_size, cell_size, cell_size)
            screen.blit(self.lis[self.vibor], wall_rect)

    def map_generate(self):
        if self.one:
            matrix = [[0] * 20 for _ in range(20)]
            for i in range(20):
                for j in range(20):
                    matrix[i][j] = random.randint(0, 18)
            self.m = matrix
            self.one = False

    def generate_place(self):
        for j in range(len(self.m)):
            for i in range(0, len(self.m[j])):
                if self.m[j][i] == 0:
                    self.walls.append((i, j))
                    # pygame.draw.rect(screen, 'white', (cell_size * i, cell_size * j, 40, 40))

    def rand(self):
        self.vibor = random.randint(0, 2)


class MAIN:
    def __init__(self, login, level):
        self.icon = pygame.transform.scale(load_image('data/apple.png'), (25, 25))
        self.snake = Snake()
        self.fruit = Fruit()
        self.fruit1 = Fruit()
        self.fruit2 = Fruit()
        self.running = True
        self.level = level
        self.log = login
        if level != -1:
            self.wall = Wall()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()

        self.fruit1.draw_fruit()
        if self.level != -1:
            self.wall.draw_wall()
        self.fruit2.draw_fruit()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        self.f = [[0] * 20 for _ in range(20)]
        for i in range(20):
            for j in range(20):
                self.f[i][j] = (i, j)

        for el in range(len(self.f)):
            for m in range(len(self.f[el])):
                if self.f[el][m] != 0:
                    if Vector2(self.f[el][m][0], self.f[el][m][1]) in self.snake.body:
                        self.f[el][m] = 0
                    elif self.level != -1 and self.f[el][m] in self.wall.walls:
                        self.f[el][m] = 0

        # print('snack')
        # переместить фрукт в другую ячейку и создать новый блок в змее
        # + защита от отрисовки на змейке или другом фрукте
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomise()
            n = False
            while not n:
                for el in self.snake.body:
                    if self.fruit.pos == el or self.fruit.pos == self.fruit1.pos or self.fruit == self.fruit2.pos:
                        self.fruit.randomise()
                n = True
            self.snake.add_block()
            self.snake.play_crunch_sound()
        elif self.fruit1.pos == self.snake.body[0]:
            self.fruit1.randomise()
            n = False
            while not n:
                for el in self.snake.body:
                    if self.fruit1.pos == el or self.fruit1.pos == self.fruit.pos or self.fruit1 == self.fruit2.pos:
                        self.fruit1.randomise()
                n = True
            self.snake.add_block()
            self.snake.play_crunch_sound()
        elif self.fruit2.pos == self.snake.body[0]:
            self.fruit2.randomise()
            n = False
            while not n:
                for el in self.snake.body:
                    if self.fruit2.pos == el or self.fruit2.pos == self.fruit1.pos or self.fruit2 == self.fruit.pos:
                        self.fruit2.randomise()
                n = True
            self.snake.add_block()
            self.snake.play_crunch_sound()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake.play_fall_cound()
            pygame.time.wait(1000)
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.play_fall_cound()
                pygame.time.wait(1000)
                self.game_over()
        if self.level != -1:
            for el in self.wall.walls:
                if self.snake.body[0].x == el[0] and self.snake.body[0].y == el[1]:
                    self.snake.play_fall_cound()
                    pygame.time.wait(1000)
                    self.game_over()
                    break

    def game_over(self):
        self.running = False

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        try:
            con = sqlite3.connect('data/snake_game.db')
            last_score = con.cursor().execute("SELECT result FROM info WHERE name=?", (self.log,)).fetchone()
            if int(last_score[0]) < int(score_text):
                con.cursor().execute("UPDATE info SET result=? WHERE name=?", (score_text, self.log))
                con.commit()
        except Exception as e:
            pass
        score_surface = game_font.render(score_text, True, '#090974')
        score_x = int(cell_size * 1.25)
        score_y = int(cell_size * 19)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        icon_rect = self.icon.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(icon_rect.left, icon_rect.top, icon_rect.width + score_rect.width + 10, icon_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(self.icon, icon_rect)
        pygame.draw.rect(screen, '#090974', bg_rect, 2)


SCREEN_UPDATE = pygame.USEREVENT

image = ''
apple = ''


def level_one_loop(log):
    global image, apple
    clicked = False
    exit_button = Button(20, 20, 120, 45, "Exit")
    clock = pygame.time.Clock()
    image = load_image('data/apple.png')
    apple = pygame.transform.scale(image, (40, 40))
    main_game = MAIN(log, -1)
    pygame.time.set_timer(SCREEN_UPDATE, 100)
    while main_game.running:
        pos = pygame.mouse.get_pos()

        if exit_button.is_clicked(pos):
            if clicked:
                main_game.running = False

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

        screen.fill((175, 215, 70))
        main_game.draw_elements()
        exit_button.render(screen)
        pygame.display.flip()
        clock.tick(60)


pygame.time.set_timer(SCREEN_UPDATE, 100)


def level_two_loop(log):
    global image, apple
    clicked = False
    exit_button = Button(20, 20, 120, 45, "Exit")
    clock = pygame.time.Clock()
    image = load_image('data/apple.png')
    apple = pygame.transform.scale(image, (40, 40))
    main_game = MAIN(log, 2)
    pygame.time.set_timer(SCREEN_UPDATE, 100)
    while main_game.running:
        pos = pygame.mouse.get_pos()

        if exit_button.is_clicked(pos):
            if clicked:
                main_game.running = False

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

        screen.fill((175, 215, 70))
        main_game.draw_elements()
        exit_button.render(screen)
        pygame.display.flip()
        clock.tick(60)
    print('ran')


def options_view():
    clicked = False
    men = Menu()
    exit_button = Button(20, 20, 120, 45, "Exit")
    running = True
    while running:
        pos = pygame.mouse.get_pos()

        if exit_button.is_clicked(pos):
            if clicked:
                running = False

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        men.render(screen)
        exit_button.render(screen)
        pygame.display.flip()


def draw_scoreboard():
    pygame.draw.rect(screen, WOOD_COLOR, pygame.Rect(250, 75, 330, 50))
    draw_text("Place", None, TEXT_COLOR, 285, 85, True, 33)
    draw_text("Score", None, TEXT_COLOR, 430, 85, True, 33)
    con = sqlite3.connect('data/snake_game.db')
    res = con.cursor().execute("SELECT name, result FROM info ORDER BY -result").fetchmany(10)
    if res is not None:
        for i, j in enumerate(res):
            pygame.draw.rect(screen, WOOD_COLOR, pygame.Rect(250, 75 + (i + 1) * 50, 330, 50))
            draw_text(j[0], None, TEXT_COLOR, 285, 85 + (i + 1) * 50, True, 33)
            draw_text(str(j[1]), None, TEXT_COLOR, 460, 85 + (i + 1) * 50, True, 33)


def score_view():
    clicked = False
    men = Menu()
    exit_button = Button(20, 20, 120, 45, "Exit")
    running = True
    while running:
        pos = pygame.mouse.get_pos()

        if exit_button.is_clicked(pos):
            if clicked:
                INDIAN_SOUND.play()
                running = False

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
        men.render(screen)
        draw_scoreboard()
        exit_button.render(screen)
        pygame.display.flip()


WAS_CLICKED = False


def check_info(login, password, screen, reg_clicked, login_clicked):
    global WAS_CLICKED
    screen.fill(BACKGROUND_COLOR)
    if not login or not password:
        draw_text("Please enter your login and password.", None, LOGIN_COLOR, 200, 375, True,
                  33)
    elif not all(i.islower() for i in login if i.isalpha()):
        draw_text("Please use ONLY small letters and numbers.", None, LOGIN_COLOR, 200, 375, True,
                  33)
    else:
        con = sqlite3.connect("data/snake_game.db")
        cursor = con.cursor()
        res = cursor.execute("SELECT * FROM info WHERE name = ? AND password = ?",
                             (login, password)).fetchall()
        if login_clicked:
            if len(res) == 0:
                draw_text("Информация о Вас не найдена",
                          None, LOGIN_COLOR, 190, 375, True, 33)
                draw_text("пожалуйста, зарегистрируйтесь",
                          None, LOGIN_COLOR, 190, 410, True, 33)
            else:
                draw_text("Происходит вход, подождите",
                          None, LOGIN_COLOR, 190, 410, True, 33)
                if not WAS_CLICKED:
                    pygame.time.set_timer(EXIT_LOGIN_EVENT_TYPE, 1000)
                    WAS_CLICKED = True
        if reg_clicked:
            if len(res) == 0:
                draw_text("Записываем Ваши данные",
                          None, LOGIN_COLOR, 200, 375, True, 33)
            else:
                draw_text("Осуществляем вход, подождите",
                          None, LOGIN_COLOR, 200, 375, True, 33)
                if not WAS_CLICKED:
                    pygame.time.set_timer(EXIT_LOGIN_EVENT_TYPE, 1000)
                    WAS_CLICKED = True
            if len(res) == 0:
                cursor.execute("INSERT INTO info (name, password) VALUES (?, ?)", (login, password))
                con.commit()
                pygame.time.set_timer(EXIT_LOGIN_EVENT_TYPE, 1000)


def login():
    user_login = ""
    user_password = ""
    input_rect = pygame.Rect(295, 245, 140, 32)
    input_rect_password = pygame.Rect(295, 300, 140, 32)
    active_color = pygame.Color('black')
    passive_color = pygame.Color('gray63')
    color = passive_color
    color2 = passive_color
    active = False
    active2 = False
    running = True
    moved = False
    updated = False
    checked_condition = False
    reg_clicked = False
    login_clicked = False
    pass_clicked = False
    font = pygame.font.Font(None, 32)
    screen.fill(BACKGROUND_COLOR)
    draw_text('Пароль должен содержать ТОЛЬКО '
              'строчные', None, LOGIN_COLOR, 20, 20, True, 38)
    draw_text('буквы и цифры', None, LOGIN_COLOR, 20, 80, True, 38)

    clock = pygame.time.Clock()
    pygame.display.flip()
    register = Button(120, 450, 200, 55, "Register")
    login = Button(450, 450, 200, 55, "Login")
    while running:

        pos = pygame.mouse.get_pos()

        if register.is_clicked(pos):
            if moved:
                INDIAN_SOUND.play()
                moved = False
            if clicked:
                reg_clicked = True

        elif login.is_clicked(pos):
            if moved:
                INDIAN_SOUND.play()
                moved = False
            if clicked:
                login_clicked = True
        else:
            moved = True
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == EXIT_LOGIN_EVENT_TYPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if input_rect_password.collidepoint(event.pos):
                    active2 = True
                else:
                    active2 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    active = False
                    active2 = False
                if active:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_login = user_login[:-1]
                    else:
                        user_login += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        active2 = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_password = user_password[:-1]
                    else:
                        user_password += event.unicode

        if active:
            color = active_color
        else:
            color = passive_color
        if active2:
            color2 = active_color
        else:
            color2 = passive_color

        check_info(user_login, user_password, screen, reg_clicked, login_clicked)
        draw_text('Пароль должен содержать ТОЛЬКО строчные', None, LOGIN_COLOR, 20, 20, True, 38)
        draw_text('буквы и цифры', None, LOGIN_COLOR, 20, 80, True, 38)
        draw_text('Login ', None, LOGIN_COLOR, 120, 250, True, 33)
        draw_text('Password', None, LOGIN_COLOR, 120, 310, True, 33)
        text_surface = font.render(user_login, True, (255, 255, 255))
        password_surface = font.render(user_password, True, (255, 255, 255))
        input_rect.width = max(240, text_surface.get_width() + 20)
        input_rect_password.width = max(240, password_surface.get_width() + 20)
        pygame.draw.rect(screen, color, input_rect, 2)
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 5))
        pygame.draw.rect(screen, color2, input_rect_password, 2)
        screen.blit(password_surface, (input_rect_password.x + 10, input_rect_password.y + 5))
        register.render(screen)
        login.render(screen)

        pygame.display.flip()
        clock.tick(FPS)
    return user_login


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    main_menu()
