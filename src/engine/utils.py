from engine.objects import Tile


def find_max_rectangles(matrix):
    """
    Функция для оптимизации, она используется для объединения объектов в группы,
    алгоритм ищет прямоугольники из объектов, после построения уровня мы объединяем их,
    таким образом мы обрабатываем меньше столкновений

    :param matrix:
    :return: rectangles
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    rectangles = []
    used = [[False for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            if type(matrix[i][j]) == Tile and not used[i][j]:
                width = 1
                height = 1

                while j + width < cols and type(matrix[i][j + width]) == Tile and not used[i][j + width]:
                    width += 1

                while i + height < rows:
                    can_expand = True
                    for w in range(width):
                        if type(matrix[i + height][j + w]) != Tile or used[i + height][j + w]:
                            can_expand = False
                            break
                    if not can_expand:
                        break
                    height += 1

                rectangle = []
                for h in range(height):
                    for w in range(width):
                        rectangle.append(matrix[i + h][j + w])
                        used[i + h][j + w] = True
                rectangles.append(rectangle)

    return rectangles
