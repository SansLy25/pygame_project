import math

import pygame
from pygame import Rect

from animation import Animation
from commons import *
from vectors import Speed, Acceleration
from vectors import Vector


def hover_check(event):
    if event.type == pygame.MOUSEMOTION:
        app.play_button.check_hover(event.pos)
        app.resume_button.check_hover(event.pos)
        app.exit_button.check_hover(event.pos)
        app.settings_button.check_hover(event.pos)
        app.back1_button.check_hover(event.pos)


class App:
    def __init__(self):
        self.is_menu_music = True
        self.music_volume = 100
        self.sfx_volume = 100
        self.menu_sprites = pygame.sprite.Group()
        self.play_button = Button(50, 275, 160, 85, 'Play', '../../assets/Default.png')
        self.background_sprite = pygame.transform.scale(pygame.image.load('../../assets/menu_background.jpg'),
                                                        (800, 600))
        self.resume_button = Button(300, 140, 200, 80, 'Resume', '../../assets/Default.png')
        self.settings_button = Button(300, 260, 200, 80, 'Settings', '../../assets/Default.png')
        self.exit_button = Button(300, 380, 200, 80, 'Exit', '../../assets/Default.png')
        self.logo_sprite = pygame.transform.scale(pygame.image.load('../../assets/Logo.png'), (1835 // 3, 751 // 3))
        self.vol1_slider = Slider(100, 210, 350, 20, 0, 100, 1, start_value=self.music_volume)
        self.vol2_slider = Slider(100, 310, 350, 20, 0, 100, 1, start_value=self.sfx_volume)
        self.back1_button = Button(300, 450, 200, 80, 'Back', '../../assets/Default.png')
        self.settings_text1 = Text("Music volume", 36, 520, 170, 100, 100, (255, 255, 255))
        self.settings_text2 = Text("SFX volume", 36, 510, 270, 100, 100, (255, 255, 255))

    def start_screen(self):
        if not self.is_menu_music:
            pygame.mixer.music.load('../../assets/menuLoop.mp3')
            pygame.mixer.music.play(-1)
            self.is_menu_music = True
        screen.blit(self.background_sprite, (0, 0))
        screen.blit(self.logo_sprite, (0, 0))
        self.play_button.draw()

    def pause(self):
        app.resume_button.draw()
        app.settings_button.draw()
        app.exit_button.draw()

    def settings(self):
        self.vol1_slider.update(events)
        self.settings_text1.draw()
        self.settings_text2.draw()
        self.vol2_slider.update(events)
        self.vol1_slider.draw()
        self.vol2_slider.draw()
        self.back1_button.draw()
        self.music_volume = self.vol1_slider.get_value()
        pygame.mixer.music.set_volume(self.music_volume / 100)
        self.sfx_volume = self.vol2_slider.get_value()


class Text:
    def __init__(self, text, size, x, y, width, height, color, font=None):
        self.text = text

        self.size = size

        self.x = x
        self.y = y

        self.color = color

        self.widht = width
        self.height = height

        self.rect = Rect(self.x, self.y, self.widht, self.height)
        self.font = pygame.font.Font(None, self.size)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self):
        screen.blit(self.text_surface, self.text_rect)


class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, step, start_value=None):
        self.rect = pygame.Rect(x, y + height // 4, width, height // 2)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = start_value if start_value is not None else min_value
        self.handle_radius = height // 2
        self.handle_pos = x + (self.value - min_value) / (max_value - min_value) * width
        self.dragging = False

    def draw(self):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.circle(screen, (0, 255, 0), (int(self.handle_pos), self.rect.centery), self.handle_radius)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                distance = math.sqrt((mouse_x - self.handle_pos) ** 2 + (mouse_y - self.rect.centery) ** 2)
                if distance <= self.handle_radius:
                    self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.handle_pos = max(self.rect.left, min(event.pos[0], self.rect.right))
                self.value = self.min_value + (self.handle_pos - self.rect.left) / self.rect.width * (
                        self.max_value - self.min_value)
                self.value = round(self.value / self.step) * self.step
                self.handle_pos = self.rect.left + (self.value - self.min_value) / (
                        self.max_value - self.min_value) * self.rect.width

    def get_value(self):
        return self.value


class Button:
    def __init__(self, x, y, width, height, text, image_path):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.text = text

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hovered = False

    def draw(self):
        current_image = self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)


class GameObject:
    def __init__(self, x, y, width, height, sprite_path=None, animation=None):
        """
        Для доступа к параметрам Rect использовать эти переменные, в данном
        случае это абстракция, для геометрического представления
        объекта используется класс Rect, через эти переменные с помощью property можно
        получать координаты, длину и ширину прямоугольника, 
        """

        self.rect = Rect(x, y, width, height)
        self.sprite = None
        self.animation = animation

        if sprite_path:
            self.sprite = pygame.image.load(sprite_path)

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def __get_rect_params(self):
        """
        Чисто внутренний метод для property
        """
        return [self.rect.left, self.rect.top,
                self.rect.width, self.rect.height]

    @x.setter
    def x(self, x):
        params = self.__get_rect_params()
        params[0] = x
        self.rect.update(*params)

    @y.setter
    def y(self, y):
        params = self.__get_rect_params()
        params[1] = y
        self.rect.update(*params)

    @width.setter
    def width(self, width):
        params = self.__get_rect_params()
        params[2] = width
        self.rect.update(*params)

    @height.setter
    def height(self, height):
        params = self.__get_rect_params()
        params[3] = height
        self.rect.update(*params)

    def change_position(self, x, y):
        """
        Полная смена позиции
        :param x: int
        :param y: int
        :return: None
        """
        self.rect.x = x
        self.rect.y = y

    def check_collide(self, other):
        """
        Проверка столкновения с другим объектом
        :param other: GameObject
        :return: bool
        """
        return self.rect.colliderect(other.rect)

    def check_collide_list(self, others):
        """
        Возвращает список индексов в списке обьектов с которыми столкнулся self
        :param others: list[GameObject]
        :return: list[bool]
        """
        return self.rect.collidelistall([other.rect for other in others])

    def set_sprite(self, sprite_path):
        """
        В случае отсутствия спрайта используется заглушка в виде
        прямоугольника
        :param sprite_path: str
        :return: None
        """
        try:
            sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(sprite,
                                                 (self.width, self.height))
        except pygame.error as e:
            print(f'Ошибка загрузки спрайта {e}')

    def draw(self, screen):
        """
        Основной метод для отрисовки
        :param screen: pygame.Surface
        """
        if self.animation:
            self.animation.update()
            self.sprite = self.animation.get_current_frame()

        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))
        else:
            new_rect = Rect(self.x, self.y, self.width, self.height)
            new_rect.y -= 38
            pygame.draw.rect(screen, (0, 255, 0), new_rect)

    def update(self):
        """
        Обновление состояния, этот метод нужно переопределить в дочерних классах
        """
        pass


class VelocityObject(GameObject):
    """
    Класс для обьекта со скоростью
    """

    def __init__(self, x, y, width, height,
                 v0=Speed(0, Vector(0, 0)),
                 sprite_path=None, animation=None):
        super().__init__(x, y, width, height, sprite_path, animation)
        self.speed = v0

    def move(self):
        self.x += self.speed.get_x_projection()
        self.y += self.speed.get_y_projection()


class AcceleratedObject(VelocityObject):
    """
    Класс для обьекта с ускорением
    """

    def __init__(self, x, y, width, height,
                 v0=Speed(0, Vector(0, 0)),
                 a0=Acceleration(0, Vector(0, 0)),
                 sprite_path=None, animation=None):

        super().__init__(x, y, width, height, v0, sprite_path, animation)
        self.acceleration = a0

    def move(self):
        super().move()
        self.speed = self.speed + self.acceleration
        self.speed.magnitude = self.speed.magnitude * 0.91
        if self.animation:
            if self.speed.magnitude < 3:
                self.animation.frame_duration = 10 ** 10
            else:
                self.animation.frame_duration = 500 * (1 / self.speed.magnitude)

        """
        В данном случае self 0.90 это коэффициент сопротивления воздуха, чтобы
        сущность не разгонялась до бесконечности, вынести в константу бы
        """

    def resolve_collision(self, *other):
        """
        Реакция на столкновения с различными обьектами,
        может быть переопределен в дочерних классах, выглядит страшно,
        но надо деле просто 4 случае обрабатывается (верхнее, нижнее, правое и левое столкн)
        :param other: list[GameObject]
        """
        for obj in other:
            if self.check_collide(obj):
                overlap_y = min(self.y + self.height,
                                obj.y + obj.height) - max(self.y, obj.y)
                overlap_x = min(self.x + self.width, obj.x + obj.width) - max(
                    self.x, obj.x)

                if overlap_y < overlap_x:
                    if self.y + self.height > obj.y > self.y:
                        self.y = obj.y - self.height
                        self.speed = Speed(self.speed.magnitude,
                                           Vector(self.speed.direction.x, 0))
                    elif self.y < obj.y + obj.height < self.y + self.height:
                        self.y = obj.y + obj.height
                        self.speed = Speed(self.speed.magnitude,
                                           Vector(self.speed.direction.x, 0))
                else:
                    if self.x + self.width > obj.x > self.x:
                        self.x = obj.x - self.width
                        self.speed = Speed(self.speed.magnitude,
                                           Vector(0, self.speed.direction.y))
                    elif self.x < obj.x + obj.width < self.x + self.width:
                        self.x = obj.x + obj.width
                        self.speed = Speed(self.speed.magnitude,
                                           Vector(0, self.speed.direction.y))


class Player(AcceleratedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'right'
        self.target_orientation = 'right'
        self.hp = 100

    def draw(self, screen):
        if self.animation:
            self.sprite = self.animation.get_current_frame()
            self.animation.update()
            if self.orientation == 'left':
                self.sprite = pygame.transform.flip(self.sprite, True, False)

        if self.target_orientation != self.orientation:
            self.orientation = self.target_orientation
            self.sprite = pygame.transform.flip(self.sprite, True, False)

        screen.blit(self.sprite, (self.x, self.y))


class Enemy(AcceleratedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'left'
        self.target_orientation = 'left'

    def draw(self, screen):
        if self.animation:
            self.sprite = self.animation.get_current_frame()
            self.animation.update()

        if self.target_orientation != self.orientation:
            self.orientation = self.target_orientation

        screen.blit(self.sprite, (self.x, self.y))


if __name__ == "__main__":
    pygame.init()

    screen_width = WIDTH
    screen_height = HEIGHT
    app = App()
    pygame.mixer.music.load('../../assets/menuLoop.mp3')
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("GameObject Example")

    game_object_animation = Animation(
        [f'../../assets/adventurer-run2-0{i + 1}.png' for i in
         range(5)], 100)

    game_object = Player(100, 100, 100, 100,
                         sprite_path="../../assets/adventurer-idle-00.png",
                         a0=Acceleration(1,
                                         Vector.unit_from_angle(
                                             90)), animation=game_object_animation)

    surface = GameObject(0, 200, 1000, 1000)
    running = True
    clock = pygame.time.Clock()
    flag = True
    game_started = False
    is_paused = False
    is_settings = False

    while running:
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if not game_started and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.play_button.is_hovered:
                game_started = True
                is_paused = False
                pygame.mixer.music.stop()
                app.is_menu_music = False
                pygame.mixer.music.load('../../assets/stage1.mp3')
                pygame.mixer.music.play(-1)
            if not is_settings:
                if is_paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.resume_button.is_hovered:
                    is_paused = not is_paused
                if is_paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.exit_button.is_hovered:
                    game_started = False
                if is_paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.settings_button.is_hovered:
                    is_settings = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.back1_button.is_hovered:
                    is_settings = False
            hover_check(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_paused = not is_paused
                is_settings = False

        if game_started:
            screen.fill((0, 0, 0))
            if not is_paused:
                if keys[pygame.K_SPACE]:
                    if flag:
                        flag = False
                        game_object.speed = game_object.speed + Speed(12,
                                                                      Vector.unit_from_angle(
                                                                          270))
                else:
                    flag = True

                if keys[pygame.K_RIGHT]:
                    game_object.speed = game_object.speed + Speed(0.6,
                                                                  Vector.unit_from_angle(
                                                                      0))
                    game_object.target_orientation = 'right'

                if keys[pygame.K_LEFT]:
                    game_object.speed = game_object.speed + Speed(0.6,
                                                                  Vector.unit_from_angle(
                                                                      180))
                    game_object.target_orientation = 'left'

                game_object.resolve_collision(surface)
                game_object.draw(screen)
                surface.draw(screen)
                game_object.move()
            else:
                """game_object.resolve_collision(surface)
                game_object.draw(screen)
                surface.draw(screen)
                camera.update(game_object)"""
                if not is_settings:
                    app.pause()
                else:
                    app.settings()

        else:
            app.start_screen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
