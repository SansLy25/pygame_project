from math import cos, sin, radians


class Vector:
    """
    Класс векторов, поддерживает основные операции с векторами
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def change(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)

        return Vector(self.x / mag, self.y / mag)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other.x, +self.y * other.y)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def scale(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    @classmethod
    def unit_from_angle(cls, angle):
        """
        Метод создает одиночный вектор из угла(параметр direction для скорости)
        полезно чтобы не высчитывать его вручную, использовать
        его при указании direction
        :param angle:
        :return:
        """
        angle_in_radians = radians(angle)
        return Vector(round(cos(angle_in_radians), 2), round(sin(angle_in_radians), 2))


class Speed:
    def __init__(self, magnitude: float, direction: Vector, name=None):
        self.magnitude = magnitude
        self.direction = direction
        self.name = name

    def change_direction(self, direction: Vector):
        self.direction = direction

    def get_vector(self):
        return self.direction.scale(self.magnitude)

    def get_x_projection(self):
        return round(self.magnitude * self.direction.x, 4)

    def get_y_projection(self):
        return round(self.magnitude * self.direction.y, 4)

    def __add__(self, other):
        """
        Метод сложенения, можно использовать как Speed() + Speed()
        так и Speed() + Acceleration() метод универсален, для изменения скорости
        использовать его
        :param other: Speed | Acceleration
        :return: Speed
        """
        summ_vector = self.get_vector() + other.get_vector()

        magnitude = summ_vector.magnitude()
        direction = summ_vector if magnitude == 0 else summ_vector.normalize()
        return Speed(magnitude, direction)

    def __mul__(self, other):
        return Speed(self.magnitude * other, self.direction)

    def __str__(self):
        return f"Speed({self.magnitude}, {self.direction})"


class Acceleration(Speed):
    def __add__(self, other):
        speed_object = Speed.__add__(self, other)
        return Acceleration(speed_object.magnitude, speed_object.direction)

    def __str__(self):
        return f"Acceleration({self.magnitude}, {self.direction})"
