class IllegalDoorError(Exception):
    def __init__(self, message="Неправильное расположение двери"):
        self.message = message
        super().__init__(self.message)

class DoorNotFoundError(Exception):
    def __init__(self, message="Дверь не найдена"):
        self.message = message
        super().__init__(self.message)