from src.engine.objects import BackgroundObject


class Background:
    """
    Фон с параллаксом
    """

    def __init__(self, layers_paths, width, height):
        self.layers = []
        self.width = width
        self.height = height
        for layer_path in layers_paths:
            self.layers.append(
                BackgroundObject(0, 0, width, height, sprite_path=layer_path)
            )

    def update(self, screen, player_x, player_y):
        for i, layer in enumerate(self.layers):
            if i != len(self.layers) - 1:
                layer.x = i * ((player_x - self.width) // 2 + self.width // 2) * 0.05
                layer.y = i * ((player_y - self.height) // 2 + self.height // 2) * 0.01
            layer.update(screen, [])
