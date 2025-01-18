from vectors import Vector
from vectors import Speed, Acceleration
from pygame import Rect
from animation import Animation
from worldgen import PerlinNoise
import pygame
import random


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

        if self.orientation == 'right':
            self.sprite = pygame.transform.flip(self.sprite, True, False)

        screen.blit(self.sprite, (self.x, self.y))


if __name__ == "__main__":
    pygame.init()

    screen_width = 800
    screen_height = 600
    world_width = 50 # Длина мира (в блоках)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("GameObject Example")
    noise = PerlinNoise(random.randint(1000000, 99999999))
    world = [] # Массив, включающий в себя все блоки мира

    game_object_animation = Animation(
                            [f'../../assets/merchant_{i}.png' for i in
                             range(10)], 80)

    game_object = Enemy(100, 100, 100, 100,
                        sprite_path="../../assets/sprite.png",
                        a0=Acceleration(1,
                                        Vector.unit_from_angle(
                                            90)),
                        animation=game_object_animation)

    h = pygame.display.get_surface().get_height()
    for x in range(world_width):
        for y in range(round(noise.get(x / 10) * 10) + 9):
            world.append(GameObject(x * 25, h - (y * 25), 25, 25))

    running = True
    clock = pygame.time.Clock()
    flag = True

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        screen.fill((0, 0, 0))
        game_object.draw(screen)
        for block in world:
            game_object.resolve_collision(block)
            block.draw(screen)
        game_object.move()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
