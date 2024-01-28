from oop.Shape import shape
import math
class circle(shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius
        self.diameter = radius * 2
    @property
    def diameter(self):
        return self._diameter
    @diameter.setter
    def diameter(self, diameter):
        self._diameter = diameter
        self.radius = diameter / 2
    def area(self):
        return self.diameter * math.pi
    def __add__(self, other):
        return circle(self.color, self.radius + other.radius)
    def __lt__(self, other):
        return self.radius < other.radius
    def __gt__(self, other):
        return self.radius > other.radius
    def __str__(self):
        return super().__str__() + "Circle properties:\n" + "radius: " + str(self.radius)