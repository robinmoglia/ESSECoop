"""Problem 5: Circle, all comparison operators based on radius"""

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __gt__(self, other):
        return self.radius > other.radius

    def __eq__(self, other):
        return self.radius == other.radius

    def __ne__(self, other):
        return self.radius != other.radius

    def __le__(self, other):
        return self.radius <= other.radius

    def __ge__(self, other):
        return self.radius >= other.radius


if __name__ == "__main__":
    c_small = Circle(2)
    c_big = Circle(5)
    c_same = Circle(2)
    print(c_small < c_big)
    print(c_small > c_big)
    print(c_small == c_same)
    print(c_small != c_big)
    print(c_small <= c_same)
    print(c_big >= c_small)
