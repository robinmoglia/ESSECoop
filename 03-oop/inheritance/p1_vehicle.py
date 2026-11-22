"""Problem 1: Vehicle / Car / Bicycle, method overriding"""

class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self):
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


if __name__ == "__main__":
    for v in [Vehicle(), Car(), Bicycle()]:
        print(v.drive())


    print(isinstance(Car(), Vehicle))
    print(issubclass(Bicycle, Car))
