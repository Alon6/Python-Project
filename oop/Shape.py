from abc import abstractmethod
class shape:
    def __init__(self, color):
        self.color = color
    @abstractmethod
    def area(self):
        pass
    def __str__(self):
        return "Shape properties:\n" + "Color: " + self.color + "\n"
