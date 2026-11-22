"""Problem 6: Point2D compared by Euclidean distance from the origin"""

from functools import total_ordering
from math import sqrt


@total_ordering
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other):
        return self.distance() == other.distance()

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"


if __name__ == "__main__":
    a = Point2D(3, 4)
    b = Point2D(1, 1)
    c = Point2D(0, 5)
    print(a)
    print(a.distance())
    print(b < a)
    print(a > b)
    print(a <= c)
    print(a == c)
