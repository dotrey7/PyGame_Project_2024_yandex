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
    # login()
    screen.fill((0, 0, 0))
    frog_sound = pygame.mixer.Sound('data/eating-sound-effect-36186.mp3')
    is_moved = False
    running = True
    men = Menu()
    frog_sprite = pygame.sprite.Group()
    frog = Animation(65, 415)
    frog_sprite.add(frog)
    button1 = Button(35, 45, 225, 50, "Play")
    button2 = Button(35, 125, 225, 50, "Options")
    button3 = Button(35, 205, 225, 50, "Scoreboard")
    button4 = Button(112, 610, 100, 110, "")
    click = False
    updated = False
    clock = pygame.time.Clock()
    while running:
        pos = pygame.mouse.get_pos()
        updated = False

        if button1.is_clicked(pos):
            if click:
                play_view()
            else:
                updated = True
                button1.update_view(screen)
                if is_moved:
                    INDIAN_SOUND.play()
                    is_moved = False
        elif button2.is_clicked(pos):
            if click:
                options_view()
            else:
                updated = True
                button2.update_view(screen)
                if is_moved:
                    INDIAN_SOUND.play()
                    is_moved = False

        elif button3.is_clicked(pos):
            if click:
                score_view()
            else:
                updated = True
                button3.update_view(screen)
                if is_moved:
                    INDIAN_SOUND.play()
                    is_moved = False
        else:
            is_moved = True

        if button4.is_clicked(pos):
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
        button1.render(screen)
        button2.render(screen)
        button3.render(screen)
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


def play_view():
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
                level_one_loop()
        elif image_rect2.collidepoint(pos):
            updated_2 = True
            if moved_2:
                SLIDE_IN.play()
                moved_2 = False
            if clicked:
                level_two_loop()
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


class Fruit:
    def __init__(self):
        self.randomise()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomise(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.running = True

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # print('snack')
            # переместить фрукт в другую ячейку и создать новый блок в змее
            self.fruit.randomise()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

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


SCREEN_UPDATE = pygame.USEREVENT

image = ''
apple = ''


def level_one_loop():
    global image, apple
    clicked = False
    exit_button = Button(20, 20, 120, 45, "Exit")
    running = True
    clock = pygame.time.Clock()
    image = load_image('data/apple.png')
    apple = pygame.transform.scale(image, (40, 40))
    main_game = MAIN()
    game_font = pygame.font.Font(None, 25)
    pygame.time.set_timer(SCREEN_UPDATE, 150)
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


def level_two_loop():
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


DONE = False


def check_info(login, password, screen, reg_clicked, login_clicked):
    global DONE
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
                if not DONE:
                    pygame.time.set_timer(EXIT_LOGIN_EVENT_TYPE, 1000)
                    DONE = True
        if reg_clicked:
            draw_text("Записываем Ваши данные",
                      None, LOGIN_COLOR, 200, 375, True, 33)
            if len(res) == 0:
                cursor.execute("INSERT INTO info (name, password) VALUES (?, ?)", (login, password))
                con.commit()
                pygame.time.set_timer(EXIT_LOGIN_EVENT_TYPE, 1000)


def login():
    user_text = ""
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
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
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

        check_info(user_text, user_password, screen, reg_clicked, login_clicked)
        draw_text('Пароль должен содержать ТОЛЬКО строчные', None, LOGIN_COLOR, 20, 20, True, 38)
        draw_text('буквы и цифры', None, LOGIN_COLOR, 20, 80, True, 38)
        draw_text('Login ', None, LOGIN_COLOR, 120, 250, True, 33)
        draw_text('Password', None, LOGIN_COLOR, 120, 310, True, 33)
        text_surface = font.render(user_text, True, (255, 255, 255))
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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    main_menu()
