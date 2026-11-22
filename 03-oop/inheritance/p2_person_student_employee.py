"""Problem 2: Person / Student / Employee, super() and overriding"""

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old, I live in {self.address}."


class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self):
        return super().introduce() + f" I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return super().introduce() + f" I work at {self.company}."


if __name__ == "__main__":
    people = [
        Person("Ana", 20, "Paris"),
        Student("Tom", 19, "Cergy", "Data Science"),
        Employee("Lea", 30, "Lyon", "BNP"),
    ]
    for p in people:
        print(p.introduce())
