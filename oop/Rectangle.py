from oop.Shape import shape
class rectangle(shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
    def __add__(self, other):
        return rectangle(self.color, self.width + other.width, self.height + other.height)
    def __str__(self):
        return super().__str__() + "Rectangle properties:\n" + "width: " + str(self.width) + "\n" + "height: " + str(self.height)
