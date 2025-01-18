import random


class PerlinNoise():
    """
    Одномерный генератор шума Перлина
    """
    def __init__(self, seed, amplitude=1, frequency=1, octaves=1):
        self.seed = random.Random(seed).random()
        self.amplitude = amplitude
        self.frequency = frequency
        self.octaves = octaves

        self.mem_x = dict()


    def __noise(self, x):
        if x not in self.mem_x:
            self.mem_x[x] = random.Random(self.seed + x).uniform(-1, 1)
        return self.mem_x[x]


    def __interpolated_noise(self, x):
        prev_x = int(x)
        next_x = prev_x + 1
        frac_x = x - prev_x 

        res = self.__linear_interp(self.__noise(prev_x), self.__noise(next_x), frac_x)

        return res


    def get(self, x):
        frequency = self.frequency
        amplitude = self.amplitude
        result = 0
        for _ in range(self.octaves):
            result += self.__interpolated_noise(x * frequency) * amplitude
            frequency *= 2
            amplitude /= 2

        return result


    def __linear_interp(self, a, b, x):
        return a + x * (b - a)