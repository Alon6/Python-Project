from oop.Circle import circle
from oop.Rectangle import rectangle
if __name__ == "__main__":
    rec1 = rectangle("green", 2, 6)
    rec2 = rectangle("green", 7, 5)
    print(rec1 + rec2)
    circle1 = circle("red", 5)
    circle2 = circle("red", 2)
    print(circle1 + circle2)
    print(circle1 > circle2)
    print(circle1 < circle2)