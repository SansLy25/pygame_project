from engine.objects import GameObject, BackgroundNotScaledObject

class Spikes(GameObject):
    pass

class Portal(GameObject):
    pass

class BigTree(BackgroundNotScaledObject):
    pass

class Tree(BackgroundNotScaledObject):
    pass

class Box(BackgroundNotScaledObject):
    pass

class SmallBox(BackgroundNotScaledObject):
    pass

class Chest(BackgroundNotScaledObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_opened = False