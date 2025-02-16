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
WINNIG_SCORE = 50

TIMER_EVENT_TYPE = 30
pygame.init()
try:
    INDIAN_SOUND = pygame.mixer.Sound('data/click-for-game-menu-131903.mp3')
    SLIDE_IN = pygame.mixer.Sound('data/click-button-app-147358.mp3')
    frog_sound = pygame.mixer.Sound('data/eating-sound-effect-36186.mp3')
    winning_sound = pygame.mixer.Sound('data/Alex Ferrari - Bara Bara Bere Bere (Radio Edit) (mp3cut.net).wav')
except Exception as e:
    print('Файлы с музыкой не найдены, пожалуйста, переместите их в папку с проектом')
EXIT_LOGIN_EVENT_TYPE = 31
cell_size = 40
cell_number = 20
game_font = pygame.font.Font(None, 25)


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print('Image not found:', fullname, "Пожалуйста, переместите папку с изображениями в проект")
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
    # класс для анимации лягушки на рабочем экране
    # self.update - смена изображений лягушки
    # self.animate - функция для изменения поля is_animating
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        try:
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
        except Exception as e:
            print('файл не найден')

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
    # функция для размещения текста на экране
    font = pygame.font.SysFont(font, size, bold=bold)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


class Menu:
    # класс отрисовки основного меню
    # self.render() - непосредственно функция рисования
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

    def render(self, screen):
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, WOOD_COLOR,
                         (0, self.height - 85,
                          self.width, self.height), 0)


class Button:
    # класс для удобного создания кнопок
    # конструктор принимает позицию кнопки, ее ширину и высоту, текст кнопки
    # self.render() - функция отрисовки кнопки
    # self.is_clicked() - функция проверки нажатия на кнопку
    # self.update_view() - функция анимации кнопки, путем увеличения длины и высоты
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


def main_menu(log=None):
    # цикл основного экрана игры

    # вызываем форму для регисрации/входа в аккаунт
    if log is None:
        log = login()

    screen.fill(BACKGROUND_COLOR)
    is_moved = False
    running = True
    men = Menu()
    men.render(screen)
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
    pygame.display.flip()
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
    # функция для отрисовки осровов на экране выбора уровня и их анимации
    try:
        image1 = load_image('data/level1.png', -1)
    except Exception as e:
        print('Файл с изображением карты не найден')
    if not updated1:
        try:
            image1 = pygame.transform.scale(image1, (250, 250))
            draw_text('Level 1', None, TEXT_COLOR, 125, 220, True, 38)
        except Exception as e:
            print('Ошибка при открытии файла изображения')
    else:
        try:
            image1 = pygame.transform.scale(image1, (270, 270))
            draw_text('Level 1', None, TEXT_COLOR, 125, 220, True, 44)
        except Exception as e:
            print('Ошибка при открытии файла изображения')
    try:
        image2 = load_image('data/level2.png', -1)
    except Exception as e:
        print('Ошибка при открытии файла изображения')
    if not updated2:
        try:
            image2 = pygame.transform.scale(image2, (250, 250))
            draw_text('Level 2', None, TEXT_COLOR, 450, 220, True, 38)
        except Exception as e:
            print('Ошибка при открытии файла изображения')
    else:
        try:
            image2 = pygame.transform.scale(image2, (270, 270))
            draw_text('Level 2', None, TEXT_COLOR, 450, 220, True, 44)
        except Exception as e:
            print('Ошибка при открытии файла изображения')
    screen.blit(image1, (70, 260))
    screen.blit(image2, (400, 260))


def play_view(log):
    # экран выбора уровня
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
                main_menu(log)
                INDIAN_SOUND.play()
        else:
            moved = True

        # проверяем нажатие на остров и запускаем цикл игры
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
    # Класс змейки с изображениями, отрисовкой и прочим. в __init__ указываем первые координаты
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        try:
            # задаем полям класса изображения с различным движением змейки
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
        except Exception as e:
            print('Изображения для отрисовки змейки не найдены')

        try:
            self.fail_cound = pygame.mixer.Sound('data/__kantouth__cartoon-bing-lo.wav')
            self.crunch_sound = pygame.mixer.Sound('data/poedanie-ukus-yabloka.wav')
        except Exception as e:
            print("Файлы звука откусывания яблока и прогрыша не найдены, пожалуйста, переметите их в папку с проектом")

    def draw_snake(self):
        # Функция отрисовки змеи "поблочно". Каждый блок следует за координатами
        # предыдущего, что в целостности даёт следование каждого блока за головой.
        # Здесь идёт обработка этой механики. Так же вставка изображений.
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

    def move_snake(self):
        # Функция для движения змейки. Движение и добавление нового блока в
        # наш "змеиный" список. Так же проверка флага, есть ли вообще
        # возможность добавить новый блок.
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
        # Просто флаг для указания чтобы добавить новый блок
        self.new_block = True

    def update_head_graph(self):
        # Функция проверяющая, когда картнику головы нужно сменить
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
        # Функция проверяющая, когда картнику хвост нужно сменить
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
        # играет музыку когда змея съедает фрукт
        try:
            self.crunch_sound.play()
        except Exception as e:
            print('Невозможно проиграть звук укуса')

    def play_fall_cound(self):
        # играет музыку когда происходит столкновение с препятствием
        try:
            self.fail_cound.play()
        except Exception as e:
            print('Невозможно проиграть звук проигрыша')


class Fruit:
    # Класс для фруктов, которые мы будем отрисовывать на поле
    def __init__(self, fn):
        self.fx = fn
        try:
            self.apple = pygame.transform.scale(load_image('data/apple.png', -1), (40, 40))
            self.clubnika = pygame.transform.scale(load_image('data/clubnika.png', -1), (40, 40))
            self.sliva = pygame.transform.scale(load_image('data/sliva.png', -1), (40, 40))
            self.arbuz = pygame.transform.scale(load_image('data/arbuz.png', -1), (40, 40))
            self.vishna = pygame.transform.scale(load_image('data/vishna.png', -1), (40, 40))
            self.banani = pygame.transform.scale(load_image('data/banani.png', -1), (40, 40))
            self.orange = pygame.transform.scale(load_image('data/orange.png', -1), (40, 40))
            self.limon = pygame.transform.scale(load_image('data/limon.png', -1), (40, 40))
            self.sp = [self.apple, self.clubnika, self.sliva, self.arbuz, self.vishna, self.banani, self.orange,
                       self.limon]
        except Exception as e:
            print('Не найдены изображения фруктов')
        self.randomise(self.fx)

    def draw_fruit(self):
        # Рисуем фрукт в рандомном месте и с рандомной картинкой
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.sp[self.vibor], fruit_rect)

    def randomise(self, sp):
        # Рандомно выбираем координаты фрукта из списка свободных ячеек
        n = sp[random.randint(0, len(sp) - 1)]
        self.x, self.y = n[0], n[1]
        self.pos = Vector2(self.x, self.y)
        self.vibor = random.randint(0, 7)


class Wall:
    # Класс для отрисовки стен
    def __init__(self):
        self.one = True
        try:
            self.wall1 = pygame.transform.scale(load_image('data/wall1.png'), (40, 40))
            self.wall2 = pygame.transform.scale(load_image('data/wall2.png'), (40, 40))
            self.wall3 = pygame.transform.scale(load_image('data/wall3.png'), (40, 40))
            self.lis = [self.wall1, self.wall3, self.wall2]
            self.walls = list()
            self.rand()
        except Exception as e:
            print('Невозможно открыть изображение стены')

    def draw_wall(self):
        # Рисует стенки из координат, заданных в списке
        self.map_generate()
        self.generate_place()
        for i in self.walls:
            wall_rect = pygame.Rect(i[0] * cell_size, i[1] * cell_size, cell_size, cell_size)
            screen.blit(self.lis[self.vibor], wall_rect)

    def map_generate(self):
        # Генерирует карту с координатами стен
        if self.one:
            matrix = [[0] * 20 for _ in range(20)]
            for i in range(20):
                for j in range(20):
                    matrix[i][j] = random.randint(0, 18)
            for e in range(0, 11):
                matrix[10][e] = 1
            self.m = matrix
            self.one = False

    def generate_place(self):
        # Добавляет координаты стен в список класса
        for j in range(len(self.m)):
            for i in range(0, len(self.m[j])):
                if self.m[j][i] == 0:
                    self.walls.append((i, j))

    def rand(self):
        # Рандомный выбор изображения для стен
        self.vibor = random.randint(0, 2)


def ending_screen():
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


class MAIN:
    # Главный класс игры
    def __init__(self, login, level):
        self.ending = False
        self.was_played = False
        try:
            self.icon = pygame.transform.scale(load_image('data/apple.png'), (25, 25))
        except Exception as e:
            print('Не найдено изображение яблока')
        self.snake = Snake()
        self.fruit = Fruit([(7, 10)])
        self.fruit1 = Fruit([(8, 10)])
        self.fruit2 = Fruit([(9, 10)])
        self.running = True
        self.level = level
        self.log = login
        if level != -1:
            self.wall = Wall()

    def update(self):
        # Обновляет игру, отрисовывая элементы класса змейки и осуществляя проверку
        if not self.ending:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        # Рисует все элементы игры, так же проверяет какой уровень установлен в игре,
        # в зависимости от этого отрисовывает стены или нет
        self.draw_grass()
        self.fruit1.draw_fruit()
        if self.level != -1:
            self.wall.draw_wall()
        self.fruit2.draw_fruit()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        if not self.ending:
            self.draw_score()
        if self.ending:
            self.draw_ending_screen()

    def check_collision(self):
        # Проверяет столкновение змеи с фруктами и отрисовывает фрукты заново
        self.f = [[0] * cell_number for _ in range(cell_number)]

        for i in range(cell_number):
            for j in range(cell_number):
                self.f[i][j] = (i, j)

        for el in range(len(self.f)):
            for m in range(len(self.f[el])):
                if self.f[el][m] != 0:
                    if Vector2(self.f[el][m][0], self.f[el][m][1]) in self.snake.body:
                        self.f[el][m] = 0
                    if self.level != -1:
                        if self.f[el][m] in self.wall.walls:
                            self.f[el][m] = 0

        for el in self.f:
            while 0 in el:
                el.remove(0)

        self.f = sum(self.f, [])

        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomise(self.f)
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.f.remove((self.fruit.x, self.fruit.y))
        elif self.fruit1.pos == self.snake.body[0]:
            self.fruit1.randomise(self.f)
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.f.remove((self.fruit1.x, self.fruit1.y))
        elif self.fruit2.pos == self.snake.body[0]:
            self.fruit2.randomise(self.f)
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.f.remove((self.fruit2.x, self.fruit2.y))

    def check_fail(self):
        # проверяет столкновение змеи со стенами или границами поля игры, собственным телом
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
        # Установка отрицательного флага
        self.ending = True
        self.draw_ending_screen()

    def draw_grass(self, color=(167, 209, 61)):
        # Рисует клетчатое игровое поле
        color = (167, 209, 61) if not self.ending else (127, 169, 21)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, color, grass_rect)

    def draw_score(self):
        # функция отображения счета игрока, если счет больше текущего рекорда пользователя,
        # обновляем рекорд, записываем его в базу данных
        score_text = str(len(self.snake.body) - 3)
        if len(self.snake.body) < 2:
            score_text = 0
        self.score = int(score_text)
        if int(self.score) >= WINNIG_SCORE:
            self.game_over()
        try:
            con = sqlite3.connect('data/snake_game.db')
            last_score = con.cursor().execute("SELECT result FROM info WHERE name=?", (self.log,)).fetchone()
            if int(last_score[0]) < int(score_text):
                con.cursor().execute("UPDATE info SET result=? WHERE name=?", (score_text, self.log))
                con.commit()
        except Exception as e:
            print("База данных не найдена, пожалуйста, переместите ее файл в папку с проектом")
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

    def draw_ending_screen(self):
        pygame.draw.rect(screen, WOOD_COLOR, (200, 200, 400, 400), 0, border_radius=20)
        try:
            con = sqlite3.connect('data/snake_game.db')
            res = con.cursor().execute("SELECT result FROM info WHERE name=?", (self.log,)).fetchone()
        except Exception as e:
            print('Нет файла базы данных')
            sys.exit()
        if self.score < WINNIG_SCORE:
            draw_text(f'Рекорд: {res[0]}', None, TEXT_COLOR, 285, 250, False, 34)
            draw_text(f'Ваш счёт: {self.score}', None, TEXT_COLOR, 285, 290, False, 34)
        else:
            draw_text(f'Вы победили! :)', None, TEXT_COLOR, 285, 250, False, 34)
            draw_text(f'Поздравляем Вас!', None, TEXT_COLOR, 285, 290, False, 34)
            if not self.was_played:
                winning_sound.play()
                self.was_played = True


SCREEN_UPDATE = pygame.USEREVENT

image = ''
apple = ''


def level_one_loop(log):
    # цикл первого уровня игры
    global image, apple
    clicked = False
    exit_button = Button(20, 20, 120, 45, "Exit")
    continue_button = Button(330, 450, 120, 45, "Continue")
    back_to_menu = Button(323, 505, 120, 45, "Back to menu")
    clock = pygame.time.Clock()
    try:
        image = load_image('data/apple.png')
    except Exception as e:
        print('Изображение яблока не найдено')
    apple = pygame.transform.scale(image, (40, 40))
    main_game = MAIN(log, -1)
    pygame.time.set_timer(SCREEN_UPDATE, 100)
    while main_game.running:
        pos = pygame.mouse.get_pos()

        if exit_button.is_clicked(pos):
            if clicked:
                play_view(log)
        elif continue_button.is_clicked(pos):
            if clicked:
                winning_sound.fadeout(300)
                level_one_loop(log)
        elif back_to_menu.is_clicked(pos):
            if clicked:
                winning_sound.fadeout(300)
                play_view(log)
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN and not main_game.ending:
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
        if main_game.ending:
            back_to_menu.render(screen)
            continue_button.render(screen)
        pygame.display.flip()
        clock.tick(60)


pygame.time.set_timer(SCREEN_UPDATE, 100)


def level_two_loop(log):
    # цикл второго уровня игры
    global image, apple
    clicked = False
    exit_button = Button(20, 20, 120, 45, "Exit")
    clock = pygame.time.Clock()
    continue_button = Button(330, 450, 120, 45, "Continue")
    back_to_menu = Button(323, 505, 120, 45, "Back to menu")
    try:
        image = load_image('data/apple.png')
    except Exception as e:
        print('Изображение яблока не найдено')
    apple = pygame.transform.scale(image, (40, 40))
    main_game = MAIN(log, 2)
    pygame.time.set_timer(SCREEN_UPDATE, 100)
    while main_game.running:
        pos = pygame.mouse.get_pos()

        if exit_button.is_clicked(pos):
            if clicked:
                play_view(log)
        elif continue_button.is_clicked(pos):
            if clicked:
                level_two_loop(log)
        elif back_to_menu.is_clicked(pos):
            if clicked:
                play_view(log)

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN and not main_game.ending:
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
        if main_game.ending:
            back_to_menu.render(screen)
            continue_button.render(screen)
        pygame.display.flip()
        clock.tick(70)


def options_view():
    # цикл изменения опций игры
    clicked = False
    men = Menu()
    exit_button = Button(20, 20, 120, 45, "Exit")
    ok_button = Button(525, 130, 155, 45, "Confirm")
    running = True
    string = ''
    active = True
    while running:
        pos = pygame.mouse.get_pos()

        if exit_button.is_clicked(pos):
            if clicked:
                running = False
        if ok_button.is_clicked(pos):
            if clicked:
                try:
                    if int(string) > 8 and int(string) < 21:
                        cell_number = int(string)
                except Exception as e:
                    pass

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    active = False
                if active:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        string = string[:-1]
                    else:
                        if event.unicode in '0123456789':
                            string += event.unicode
        try:
            if string and int(string) > 20:
                string = '20'
            if string.startswith('0'):
                string = '8'
        except Exception as e:
            pass
        men.render(screen)
        exit_button.render(screen)
        ok_button.render(screen)
        pygame.draw.rect(screen, WOOD_COLOR, pygame.Rect(460, 144, 45, 35), 3)
        draw_text('Размер поля клеток на клеток', None, TEXT_COLOR, 20, 143, True, 33)
        draw_text(string, None, TEXT_COLOR, 464, 147, True, 33)
        pygame.display.flip()
        pygame.display.flip()


def draw_scoreboard():
    # функция для отрисовки топ 10 пользователей по их рекордам
    pygame.draw.rect(screen, WOOD_COLOR, pygame.Rect(250, 75, 330, 50))
    draw_text("Place", None, TEXT_COLOR, 285, 85, True, 33)
    draw_text("Score", None, TEXT_COLOR, 430, 85, True, 33)
    try:
        con = sqlite3.connect('data/snake_game.db')
        res = con.cursor().execute("SELECT name, result FROM info ORDER BY -result").fetchmany(10)
        if res is not None:
            for i, j in enumerate(res):
                pygame.draw.rect(screen, WOOD_COLOR, pygame.Rect(250, 75 + (i + 1) * 50, 330, 50))
                draw_text(j[0], None, TEXT_COLOR, 285, 85 + (i + 1) * 50, True, 33)
                draw_text(str(j[1]), None, TEXT_COLOR, 460, 85 + (i + 1) * 50, True, 33)
    except Exception as e:
        print("Файл базы данных не найден, пожалуйста, переметите его в папку с проектом")


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
    # функция для проверки информации, введенной пользователем при попытке входа/регистрации
    # включает проверки: на неправильный ввод, на попытку регистрации идентичного аккаунта, на неправильный пароль
    # сообщает пользователе об ошибке в реальном времени
    # при регистрации новая информация записывается в базу данных
    global WAS_CLICKED
    screen.fill(BACKGROUND_COLOR)
    if not login or not password:
        draw_text("Please enter your login and password.", None, LOGIN_COLOR, 200, 375, True,
                  33)
    elif not all(i.islower() for i in login if i.isalpha()):
        draw_text("Please use ONLY small letters and numbers.", None, LOGIN_COLOR, 200, 375, True,
                  33)
    else:
        try:
            con = sqlite3.connect("data/snake_game.db")
            cursor = con.cursor()
            res = cursor.execute("SELECT * FROM info WHERE name = ? AND password = ?",
                                 (login, password)).fetchall()
        except Exception as e:
            print("Файл базы данных не найден, пожалуйста, переметите его в папку с проектом")
            sys.exit()

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
                try:
                    cursor.execute("INSERT INTO info (name, password) VALUES (?, ?)", (login, password))
                    con.commit()
                    pygame.time.set_timer(EXIT_LOGIN_EVENT_TYPE, 1000)
                except Exception as e:
                    print('Ошибка с поиском файла базы данных')


def login():
    # цикл регистрации
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
