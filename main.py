import pygame
import sys
import os

SCREEN = WIDTH, HEIGHT = 800, 800
FPS = 60
BACKGROUND_COLOR = (13, 242, 97)
WOOD_COLOR = (149, 99, 13)
TEXT_COLOR = (239, 239, 239)


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
    INDIAN_SOUND = pygame.mixer.Sound('data/click-for-game-menu-131903.mp3')
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


def play_view():
    men = Menu()
    clicked = False
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


def score_view():
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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    main_menu()
