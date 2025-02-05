import pygame
import random
from pygame import Rect

from .animation import Animation
from .vectors import Speed, Acceleration
from .vectors import Vector


class GameObject:
    all_game_objects = []

    def __init__(self, x, y, width, height, sprite_path=None, animation=None):
        """
        Для доступа к параметрам Rect использовать эти переменные, в данном
        случае это абстракция, для геометрического представления
        объекта используется класс Rect, через эти переменные с помощью property можно
        получать координаты, длину и ширину прямоугольника, 
        """
        GameObject.all_game_objects.append(self)
        self.rect = Rect(x, y, width, height)
        self.sprite = None
        self.start_sprite = None
        self.animation = animation

        if sprite_path:
            sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(sprite, (width, height))
            self.start_sprite = self.sprite.copy()

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
        if round(x, 0) != params[0]:
            params[0] = x
        self.rect.update(*params)

    @y.setter
    def y(self, y):
        params = self.__get_rect_params()
        if round(y, 0) != params[1]:
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
            self.sprite = pygame.transform.scale(
                self.animation.get_current_frame(), (self.width, self.height))

        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))
        else:
            new_rect = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, (0, 255, 0), new_rect)

    def resolve_physic(self, obj):
        """
        Физическое разрешение столкновения
        :param other:
        :return:
        """
        overlap_y = min(self.y + self.height,
                        obj.y + obj.height) - max(self.y, obj.y)
        overlap_x = min(self.x + self.width, obj.x + obj.width) - max(
            self.x, obj.x)

        if overlap_y < overlap_x:
            if self.y + self.height > obj.y > self.y:
                self.y = obj.y - self.height
                if self.speed.direction.y > 0:
                    self.speed = Speed(self.speed.magnitude,
                                       Vector(self.speed.direction.x,
                                              0))

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

    def resolve_collisions(self, others: list):
        """
        Реакция на столкновения с различными обьектами,
        может быть переопределен в дочерних классах, выглядит страшно,
        но надо деле просто 4 случае обрабатывается (верхнее, нижнее, правое и левое столкн)
        :param others: list[GameObject]
        """
        for obj in others:
            if self.check_collide(obj):
                if type(obj) == SolidObject:
                    self.resolve_physic(obj)

    def update(self, screen, game_objects: list):
        if hasattr(self, 'move'):
            self.move()
        self.resolve_collisions(game_objects)
        self.draw(screen)


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
        """
        В данном случае self 0.91 это коэффициент сопротивления воздуха, чтобы
        сущность не разгонялась до бесконечности, вынести в константу бы
        """


class SolidObject(GameObject):
    pass

class Item(GameObject):
    def __init__(self, x, y, width, height, damage, attack_speed, crit_damage, crit_chance, sprite_path=None):
        super().__init__(x, y, width, height, sprite_path)
        self.damage = damage
        self.attack_speed = attack_speed
        self.crit_damage = crit_damage
        self.crit_chance = crit_chance
        self.player = None
        self.is_found = False


class Player(AcceleratedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'right'
        self.target_orientation = 'right'
        self.current_hp = 100
        self.max_hp = 100
        self.lvl = 1
        self.max_exp = 100
        self.current_exp = 0
        self.attack_range = 100
        self.damage = 25
        self.attack_speed = 1.5
        self.crit_damage = 2
        self.crit_chance = 1
        self.last_attack_time = 0
        self.is_jumped = False
        self.is_on_floor = False
        self.is_item_found = False
        self.found_item = None
        self.is_max_exp = False
        self.attack_speed_mod = 0
        self.damage_mod = 0
        self.crit_chance_mod = 0
        self.crit_damage_mod = 0
        self.jump_animation = Animation(
            [f'../assets/player/animations/jump/{i}.png' for i in range(4)],
            100)
        """self.attack_animation = Animation(
            [f'../assets/player/animations/attack/{i}.png' for i in range(8)],
            100)"""
        self.run_animation = Animation(
            [f'../assets/player/animations/run/{i}.png' for i in
             range(6)], 100)

    def _is_on_floor(self, objects):
        for obj in objects:
            if type(obj) == SolidObject:
                overlap_y = min(self.y + self.height,
                                obj.y + obj.height) - max(self.y, obj.y)
                overlap_x = min(self.x + self.width, obj.x + obj.width) - max(
                    self.x, obj.x)

                if overlap_y < overlap_x:
                    if self.y + self.height > obj.y - 1 > self.y:
                        return True

        return False

    def jump(self):
        if self.is_on_floor:
            self.speed = self.speed + Speed(17,
                                            Vector.unit_from_angle(
                                                270))
            self.is_jumped = True
            self.animation = self.jump_animation
            self.animation.current_frame = 0

    def resolve_collisions(self, others: list):
        self.is_on_floor = self._is_on_floor(others)
        if self.is_jumped and self.is_on_floor:
            self.is_jumped = False
            self.animation = self.run_animation
            self.animation.current_frame = 0

        super().resolve_collisions(others)

    def draw(self, screen):
        if self.animation:
            if -3 < self.speed.get_x_projection() < 3 and (not self.is_jumped):
                self.sprite = self.start_sprite
                self.animation.current_frame = 0
            else:
                if not self.is_jumped:
                    self.animation.frame_duration = 500 * (
                            1 / self.speed.magnitude)
                self.sprite = pygame.transform.scale(
                    self.animation.get_current_frame(),
                    (self.width, self.height))
                self.animation.update()

            if self.orientation == 'left':
                self.sprite = pygame.transform.flip(self.sprite, True, False)

        if self.target_orientation != self.orientation:
            self.orientation = self.target_orientation
            self.sprite = pygame.transform.flip(self.sprite, True, False)

        screen.blit(self.sprite, (self.x, self.y))

    def attack(self, enemies, current_time):
        attack_cooldown = int(60 / (self.attack_speed + self.attack_speed_mod))
        if current_time - self.last_attack_time >= attack_cooldown:
            print('attack')
            self.last_attack_time = current_time
            for i in enemies:
                if i.is_can_be_attacked:
                    if self.crit_chance + self.crit_chance_mod != 0:
                        if random.randint(1, 101) in range(1,
                                                           self.crit_chance + self.crit_chance_mod):
                            print('crit')
                            i.current_hp -= self.damage * (self.crit_damage + self.crit_damage_mod)
                        else:
                            i.current_hp -= (self.damage + self.damage_mod)
                    else:
                        i.current_hp -= (self.damage + self.damage_mod)
                    if i.hp_check():
                        self.current_exp += 25

    def max_exp_check(self):
        if self.current_exp >= self.max_exp:
            self.current_exp -= self.max_exp
            self.max_exp = int(self.max_exp * 1.2)
            self.lvl += 1
            self.is_max_exp = True

    def hp_check(self):
        if self.current_hp <= 0:
            print('dead')

    def item_found(self, objects):
        items = [obj for obj in objects if type(obj) is Item and self.check_collide(obj)]
        if items:
            self.found_item = items[-1]
            self.is_item_found = True

    def debug(self):
        print(self.crit_damage_mod)
        print(self.damage_mod)
        print(self.attack_speed_mod)
        print()

    def update(self, screen, game_objects: list):
        super().update(screen, game_objects)
        self.hp_check()
        self.max_exp_check()
        self.item_found(game_objects)


class Enemy(AcceleratedObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = None
        self.spawn_x = self.x
        self.spawn_y = self.y
        self.spawn_speed = self.speed
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.spawn_acceleration = self.acceleration
        self.attack_range = 100
        self.damage = 25
        self.attack_speed = 1.5
        self.last_attack_time = 0
        self.orientation = 'left'
        self.target_orientation = 'left'
        self.vision_range = 200
        self.is_following = False
        self.max_vision_range = 500
        self.is_can_be_attacked = False
        self.destroyed = False
        self.is_can_attack = False

    def draw(self, screen):
        if not self.destroyed:
            if self.animation:
                self.sprite = self.animation.get_current_frame()
                self.animation.update()

            if self.target_orientation != self.orientation:
                self.orientation = self.target_orientation

            screen.blit(self.sprite, (self.x, self.y))

    def set_target(self, player):
        self.player = player

    def move(self):
        if not self.destroyed:
            super().move()
            distance_x = abs(self.player.x - self.x)
            if distance_x >= self.player.attack_range:
                if distance_x <= self.vision_range:
                    self.is_following = True
                    if self.player.x < self.x:
                        self.speed = self.speed + Speed(0.3,
                                                        Vector.unit_from_angle(
                                                            180))
                    elif self.player.x > self.x:
                        self.speed = self.speed + Speed(0.3,
                                                        Vector.unit_from_angle(
                                                            0))
                elif self.is_following:
                    distance_x = abs(self.player.x - self.x)
                    if distance_x <= self.max_vision_range:
                        if self.player.x < self.x:
                            self.speed = self.speed + Speed(0.3,
                                                            Vector.unit_from_angle(
                                                                180))
                        elif self.player.x > self.x:
                            self.speed = self.speed + Speed(0.3,
                                                            Vector.unit_from_angle(
                                                                0))
                    else:
                        self.is_following = False

    def can_be_attacked(self):
        if not self.destroyed:
            distance_x = self.player.x - self.x
            distance_y = abs(self.player.y - self.y)
            if self.player.orientation == 'right' and 0 >= distance_x >= -self.player.attack_range and distance_y <= 100:
                self.is_can_be_attacked = True
            elif self.player.orientation == 'left' and 0 <= distance_x <= self.player.attack_range and distance_y <= 100:
                self.is_can_be_attacked = True
            else:
                self.is_can_be_attacked = False
        else:
            self.is_can_be_attacked = False

    def can_attack(self):
        if not self.destroyed:
            distance_x = self.player.x - self.x
            distance_y = abs(self.player.y - self.y)
            if self.player.orientation == 'right' and 0 >= distance_x >= -self.attack_range and distance_y <= 100:
                self.is_can_attack = True
            elif self.player.orientation == 'left' and 0 <= distance_x <= self.attack_range and distance_y <= 100:
                self.is_can_attack = True
            else:
                self.is_can_attack = False
        else:
            self.is_can_attack = False

    def attack(self, current_time):
        attack_cooldown = int(60 / self.attack_speed)
        if current_time - self.last_attack_time >= attack_cooldown:
            print('attacked')
            self.last_attack_time = current_time
            self.player.current_hp -= self.damage
            if self.player.hp_check():
                pass

    def hp_check(self):
        if self.current_hp <= 0:
            self.destroy()
            return True

    def destroy(self):
        self.destroyed = True

    def respawn(self):
        self.destroyed = False
        self.current_hp = self.max_hp
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.speed = self.spawn_speed
        self.acceleration = self.spawn_acceleration

    def update(self, screen, game_objects: list):
        super().update(screen, game_objects)
        self.hp_check()
        self.can_attack()
        self.can_be_attacked()
