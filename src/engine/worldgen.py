import random
from errors import IllegalDoorError, DoorNotFoundError

import pygame
import sys
import os


"""
Блок, из которого состоит подземелье
"""
class Tile(pygame.sprite.Sprite):
    def __init__(self, app, tile_type, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        tile_images = {
            'wall': app.load_image('box.png'),
            'empty': app.load_image('grass.png')
        }

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


"""
Комната подземелья
У каждой комнаты есть её план, который находитя по пути ./rooms (От корня проекта)
План - текстовый файл с тремя типами символов:
. - Пустота
# - Стена
D - Дверь (Соеденение между комнатами)
Дверь может находиться только на краю комнаты
На каждой стороне комнаты может быть только одна дверь
"""
class Room:
    def __init__(self, filename, x, y):
        self.room_group = pygame.sprite.Group()
        self.tile_width = self.tile_height = 50

        self.x = x
        self.y = y

        self.layout, self.doors = self.load_room(filename)

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('../../assets/', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            sys.exit()
            raise FileNotFoundError(f"Файл с изображением '{fullname}' не найден")
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image
    
    """
    Загружает комнату
    Возращает план в виде матрицы и двери в виде матрицы (x, y, Сторона двери)
    """
    def load_room(self, filename):
        doors = []

        filename = "../../rooms/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        layout = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        # Если дверь находится по углам (Не достигаемое расположение), возращаем ошибку
        if 'D' in [layout[0][0], layout[0][-1], layout[-1][0], layout[0][-1]]:
            raise IllegalDoorError

        if "D" in layout[0]:
            doors.append((layout[0].index("D") * self.tile_width + self.x, self.y, "N"))
        if "D" in layout[-1]:
            doors.append((layout[-1].index("D") * self.tile_width + self.x, (len(layout) - 1) * self.tile_height + self.y, "S"))

        for y in range(1, len(layout)-1):
                if 'D' in layout[y]:
                    # Если дверь находится в центре комнаты, возращаем ошибку
                    if layout[y][-1] != 'D' and layout[y][0] != 'D':
                        raise IllegalDoorError
                    if layout[y][0] == 'D':
                        doors.append((self.x, y * self.tile_height + self.y, "W"))
                    if layout[y][-1] == 'D':
                        doors.append((len(layout[y]) * self.tile_width + self.x, y * self.tile_height + self.y, "E"))
                    
        return layout, doors

    """
    Генерирует комнату из плана self.layout
    Все спрайты комнаты находятся в группе self.room_group
    """
    def generate_room(self):
        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                if self.layout[y][x] == '.':
                    Tile(self,'empty', x * self.tile_width + self.x, y * self.tile_height + self.y)
                elif self.layout[y][x] == '#':
                    self.room_group.add(Tile(self,'wall', x * self.tile_width + self.x, y * self.tile_height + self.y))
                elif self.layout[y][x] == '@':
                    Tile(self, 'empty', x * self.tile_width + self.x, y * self.tile_height + self.y)

class App: # TODO: Вынести App в отдельный файл
    def __init__(self):
        pygame.init()
        self.width, self.height = 2000, 900
        self.tile_width = self.tile_height = 50 # TODO: Добавить единую длину/ширину клетки
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pygame Rougelike')

        # self.rooms - Все комнаты в мире
        self.rooms = [Room("room_start", 10, 500)]
        # Загрузка первой комнаты (в которой находится игрок)
        self.rooms[0].generate_room()

        # Двери, не присоеденённые к комнате
        self.lonely_doors = [*self.rooms[0].doors]

        i = 10
        while i > 0:
            if self.lonely_doors == []:
                break
            if self.generate_room(random.choice(os.listdir("../../rooms")), random.choice(self.lonely_doors)): 
                # TODO: починить генерацию и придумать проверку на сталкивания комнат
                i -= 1


        self.fps = 50

    def terminate(self):
        pygame.quit()
        sys.exit()

    def generate_room(self, room, door):
        # Кандидат на загрузку в мир
        flag = False
        cand = self.scan_room(room)
        for i in range(len(cand[1])):
            if (cand[1][i][2] == 'W' and door[2] == 'E' or 
                cand[1][i][2] == 'E' and door[2] == 'W' or 
                cand[1][i][2] == 'N' and door[2] == 'S' or 
                cand[1][i][2] == 'S' and door[2] == 'N'):
                    cand_room = Room(room, door[0] + self.tile_width, door[1] - cand[1][i][1] * self.tile_width)
                    self.rooms.append(cand_room)
                    cand_room.generate_room()
                    self.lonely_doors.pop(0)
                    cand_room.doors.pop(i)  
                    self.lonely_doors += cand_room.doors
                    flag = True
        return flag

    """
    Сканирует комнату
    Возращает длину и ширину комнаты и двери в виде матрицы (x, y, Сторона двери)
    """
    def scan_room(self, filename):
        doors = []

        filename = "../../rooms/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        layout = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        if 'D' in [layout[0][0], layout[0][-1], layout[-1][0], layout[0][-1]]:
            raise IllegalDoorError

        if "D" in layout[0]:
            doors.append((layout[0].index("D"), 0, "N"))
        if "D" in layout[-1]:
            doors.append((layout[-1].index("D"), len(layout) - 1, "S"))

        for y in range(1, len(layout)-1):
                if 'D' in layout[y]:
                    # Если дверь находится в центре комнаты, возращаем ошибку
                    if layout[y][-1] != 'D' and layout[y][0] != 'D':
                        raise IllegalDoorError
                    if layout[y][0] == 'D':
                        doors.append((0, y, "W"))
                    if layout[y][-1] == 'D':
                        doors.append((len(layout[y]), y, "E"))
                    
        return (len(layout[y]), len(layout)), doors        

    def run_game(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            self.screen.fill(pygame.Color('blue'))

            for room in self.rooms:
                room.room_group.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.run_game()
