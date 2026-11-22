"""Problem 1: complex numbers, overloading + and -"""

class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        new_real = self.real + other.real
        new_imag = self.imag + other.imag
        return Complex(new_real, new_imag)

    def __sub__(self, other):
        new_real = self.real - other.real
        new_imag = self.imag - other.imag
        return Complex(new_real, new_imag)

    def __repr__(self):
        return f"{self.real} + {self.imag}i"


if __name__ == "__main__":
    c1 = Complex(1, 2)
    c2 = Complex(3, 4)
    print(c1 + c2)
    print(c1 - c2)
