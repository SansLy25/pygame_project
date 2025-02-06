from random import randint

import pygame

from engine.animation import Animation
from engine.objects import SolidObject, Tile
from engine.utils import find_max_rectangles
from engine.vectors import Speed
from game.enemies import Portal
from src.game.enemies import Spikes


class Room:
    def __init__(self, file_path, x, y, tile_size):
        self.tile_width = self.tile_height = tile_size

        self.x = x
        self.y = y
        self.tile_size = tile_size

        self.layout = self.load_room(file_path)
        self.objects = self.load_objects()

    def load_room(self, filename):
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))

        layout = [list(string) for string in level_map]

        return layout

    def choose_object(self, cell, neighbours):
        def get_neighbour(direction):
            return neighbours.get(direction, False)

        def air_condition(air_neighbours, filled_neighbours):
            directions = {'lu': 'left_up', 'um': 'up_mid', 'ru': 'right_up',
                          'lm': 'left_mid', 'rm': 'right_mid',
                          'ld': 'left_down', 'dm': 'down_mid', 'rd': 'right_down'}
            for neighbour in air_neighbours:
                if get_neighbour(directions[neighbour]) == '#':
                    return False

            for neighbour in filled_neighbours:
                if get_neighbour(directions[neighbour]) != '#':
                    return False

            return True

        sprite = None
        """
        Здесь исходя из соседей тайла выбирается нужный спрайт, к сожалению по другому это не сделать, да
        выглядит страшненько, но максимально сжато (основное вынес в 2 другие функции), и понятно
        """
        if cell == '.':
            return None
        elif cell == '#':
            if air_condition(['lm', 'um'], ['dm', 'rm']):
                rand = randint(0, 10)
                sprite = '../assets/tiles/Tile_01.png' if rand < 2 else '../assets/tiles/Tile_14.png'
            elif air_condition(['um'], ['lm', 'rm', 'dm']):
                rand = randint(0, 10)
                sprite = '../assets/tiles/Tile_03.png' if rand < 2 else '../assets/tiles/Tile_16.png'
            elif air_condition(['um', 'ru', 'rm'], ['dm', 'lm']):
                rand = randint(0, 10)
                sprite = '../assets/tiles/Tile_04.png' if rand < 2 else '../assets/tiles/Tile_17.png'
            elif air_condition(['um', 'lm', 'rm'], ['dm']):
                rand = randint(0, 10)
                sprite = '../assets/tiles/Tile_09.png' if rand < 2 else '../assets/tiles/Tile_44.png'
            elif air_condition(['lm'], ['um', 'rm', 'dm']):
                sprite = '../assets/tiles/Tile_10.png'
            elif air_condition(['rm'], ['um', 'dm', 'lm']):
                sprite = '../assets/tiles/Tile_13.png'
            elif air_condition(['lm', 'rm'], ['um', 'dm']):
                sprite = '../assets/tiles/Tile_18.png'
            elif air_condition(['lm', 'dm'], ['um', 'rm']):
                sprite = '../assets/tiles/Tile_19.png'
            elif air_condition(['dm'], ['lm', 'um', 'rm']):
                sprite = '../assets/tiles/Tile_21.png'
            elif air_condition(['rm', 'dm'], ['um', 'lm']):
                sprite = '../assets/tiles/Tile_22.png'
            elif air_condition(['lm', 'dm', 'um'], ['rm']):
                sprite = '../assets/tiles/Tile_23.png'
            elif air_condition(['um', 'dm'], ['rm', 'lm']):
                sprite = '../assets/tiles/Tile_25.png'
            elif air_condition(['um', 'dm', 'rm'], ['lm']):
                sprite = '../assets/tiles/Tile_26.png'
            elif air_condition(['lm', 'rm', 'dm'], ['um']):
                sprite = '../assets/tiles/Tile_27.png'
            elif air_condition(['rd'], ['lu', 'um', 'ru', 'rm', 'lm', 'ld', 'dm']):
                sprite = '../assets/tiles/Tile_28.png'
            elif air_condition(['ld'], ['lu', 'um', 'ru', 'rm', 'lm', 'rd', 'dm']):
                sprite = '../assets/tiles/Tile_29.png'
            elif air_condition(['ld', 'lu'], ['um', 'ru', 'rm', 'lm', 'rd', 'dm']):
                sprite = '../assets/tiles/Tile_30.png'
            elif air_condition(['lu', 'ru'], ['um', 'rm', 'lm', 'rd', 'dm', 'ld']):
                sprite = '../assets/tiles/Tile_31.png'
            elif air_condition(['lu', 'rd'], ['um', 'rm', 'lm', 'dm', 'ld', 'ru']):
                sprite = '../assets/tiles/Tile_32.png'
            elif air_condition(['um', 'rm', 'lm', 'dm'], []):
                sprite = '../assets/tiles/Tile_36.png'
            elif air_condition(['ru'], ['ld', 'lu', 'um', 'rm', 'lm', 'rd', 'dm']):
                sprite = '../assets/tiles/Tile_37.png'
            elif air_condition(['lu'], ['ld', 'ru', 'um', 'rm', 'lm', 'rd', 'dm']):
                sprite = '../assets/tiles/Tile_38.png'
            elif air_condition(['ld', 'rd'], ['ru', 'um', 'rm', 'lm', 'dm', 'lu']):
                sprite = '../assets/tiles/Tile_39.png'
            elif air_condition(['ru', 'rd'], ['um', 'rm', 'lm', 'dm', 'lu', 'ld']):
                sprite = '../assets/tiles/Tile_40.png'
            elif air_condition(['ru', 'ld'], ['um', 'rm', 'lm', 'dm', 'lu', 'rd']):
                sprite = '../assets/tiles/Tile_41.png'
            elif air_condition(['ru', 'ld'], ['um', 'rm', 'lm', 'dm', 'lu', 'rd']):
                sprite = '../assets/tiles/Tile_41.png'
            else:
                rand_num = randint(0, 1)
                if rand_num == 0:
                    sprite = '../assets/tiles/Tile_11.png'
                else:
                    sprite = '../assets/tiles/Tile_12.png'

            return Tile(0, 0, self.tile_width, self.tile_height,
                               sprite_path=sprite)
        elif cell == 's':
            return Spikes(0, 0, self.tile_width, self.tile_height * 0.2,
                               sprite_path='../assets/tiles/spikes.png')
        elif cell == 'p':
            animation = Animation([f'../assets/portal/{i}.png' for i in range(6)], 150)
            return Portal(0, 0, self.tile_width * 0.8, self.tile_height * 0.8,
                               sprite_path='../assets/portal/1.png', animation=animation)

    def load_objects(self):
        objects = []
        tiles_matrix = [[0 for _ in range(len(self.layout[0]))] for _ in range(len(self.layout))]

        for i in range(len(self.layout)):
            for j in range(len(self.layout[0])):
                object = self.choose_object(self.layout[i][j],
                                            self.get_neighbors(i, j))
                if not object is None:
                    if type(object) == Spikes:
                        object.y = i * self.tile_height + self.tile_size * 0.8
                        object.x = j * self.tile_width
                    elif type(object) == Portal:
                        object.y = i * self.tile_height + self.tile_height * 0.1
                        object.x = j * self.tile_width + self.tile_width * 0.1

                    else:
                        object.y = i * self.tile_height
                        object.x = j * self.tile_width

                    if type(object) == Tile:
                        tiles_matrix[i][j] = object
                    else:
                        tiles_matrix[i][j] = 0
                        objects.append(object)

        for tile_rect_list in find_max_rectangles(tiles_matrix):
            rectangle = self.get_merged_rectangle_tiles(tile_rect_list)
            objects.append(rectangle)

        del tiles_matrix
        return objects

    @staticmethod
    def get_merged_rectangle_tiles(tile_list: list):
        min_x = min(tile.x for tile in tile_list)
        min_y = min(tile.y for tile in tile_list)

        max_x = max(tile.x + tile.width for tile in tile_list)
        max_y = max(tile.y + tile.height for tile in tile_list)

        width = max_x - min_x
        height = max_y - min_y

        combined_sprite = pygame.Surface((width, height))
        combined_sprite.fill((0, 0, 0))
        for tile in tile_list:
            combined_sprite.blit(tile.sprite, (tile.x - min_x, tile.y - min_y))

        rectangle = SolidObject(min_x, min_y, width, height)
        rectangle.sprite = combined_sprite
        return rectangle

    def get_neighbors(self, row, col):
        neighbors = {}
        rows, cols = len(self.layout), len(self.layout[0])

        directions = {
            "left_up": (-1, -1), "up_mid": (-1, 0), "right_up": (-1, 1),
            "left_mid": (0, -1), "right_mid": (0, 1),
            "left_down": (1, -1), "down_mid": (1, 0), "right_down": (1, 1)
        }

        for key, (dr, dc) in directions.items():
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbors[key] = self.layout[new_row][new_col]

        return neighbors

    """
    Генерирует комнату из плана self.layout
    Все спрайты комнаты находятся в группе self.room_group
    """

    # def generate_room(self):
    #     for y in range(len(self.layout)):
    #         for x in range(len(self.layout[y])):
    #             if self.layout[y][x] == '.':
    #                 Tile(self, 'empty', x * self.tile_width + self.x,
    #                      y * self.tile_height + self.y)
    #             elif self.layout[y][x] == '#':
    #                 self.room_group.add(
    #                     Tile(self, 'wall', x * self.tile_width + self.x,
    #                          y * self.tile_height + self.y))
    #             elif self.layout[y][x] == '@':
    #                 Tile(self, 'empty', x * self.tile_width + self.x,
    #                      y * self.tile_height + self.y)
