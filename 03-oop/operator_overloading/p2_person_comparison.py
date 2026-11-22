"""Problem 2: Person compared by age with >"""

class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        return self.age > other.age


if __name__ == "__main__":
    p1 = Person("Ana", 20, "F")
    p2 = Person("Tom", 18, "M")
    print(p1 > p2)
    print(p2 > p1)
