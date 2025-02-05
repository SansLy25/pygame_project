from objects import SolidObject


class Room:
    def __init__(self, file_path, x, y, tile_size):
        self.tile_width = self.tile_height = 50

        self.x = x
        self.y = y
        self.tile_size = tile_size

        self.layout = self.load_room(file_path)
        self.objects_layout = self.load_objects()

    def load_room(self, filename):
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))

        layout = [list(string) for string in
                  list(map(lambda x: x.ljust(max_width, '.'), level_map))]

        return layout

    def choose_object(self, neighbours):


        return obj

    def load_objects(self):
        for i in range(len(self.layout)):
            for j in range(len(self.layout)):
                object = self.choose_object(self.get_neighbors(i, j))

        return []

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


a = Room('../../rooms/room1.txt', 10, 40, 13)
