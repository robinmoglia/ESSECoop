"""UML exercise 1: online hospital management system (slide 68)"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


class ProblemStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in-review"
    RESOLVED = "resolved"


class User(ABC):
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.logged_in = False

    def login(self):
        self.logged_in = True

    def logout(self):
        self.logged_in = False


class Patient(User):
    def __init__(self, user_id, name, email, address):
        super().__init__(user_id, name, email)
        self.address = address
        self.problems = []
        self.prescriptions = []

    def post_problem(self, description):
        problem = HealthProblem(len(self.problems) + 1, description, self)
        self.problems.append(problem)
        return problem

    def receive_prescription(self, prescription):
        self.prescriptions.append(prescription)

    def pay(self, prescription, payment):
        payment.process()
        prescription.payment = payment
        return payment


class Doctor(User):
    def __init__(self, user_id, name, email, speciality):
        super().__init__(user_id, name, email)
        self.speciality = speciality
        self.balance = 0

    def write_prescription(self, problem, medications, price):
        prescription = Prescription(problem.problem_id, medications, price, self, problem)
        problem.prescription = prescription
        return prescription

    def receive_payment(self, amount):
        self.balance += amount


class Organizer(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.reviewed = []

    def review_problem(self, problem):
        problem.status = ProblemStatus.IN_REVIEW
        self.reviewed.append(problem)

    def consult_doctor(self, doctor, problem, medications, price):
        return doctor.write_prescription(problem, medications, price)

    def send_prescription(self, prescription, patient):
        patient.receive_prescription(prescription)
        prescription.problem.status = ProblemStatus.RESOLVED

    def forward_payment(self, prescription):
        prescription.doctor.receive_payment(prescription.payment.amount)


class HealthProblem:
    def __init__(self, problem_id, description, patient):
        self.problem_id = problem_id
        self.description = description
        self.patient = patient
        self.created_at = datetime.now()
        self.status = ProblemStatus.PENDING
        self.prescription = None


class Prescription:
    def __init__(self, prescription_id, medications, price, doctor, problem):
        self.prescription_id = prescription_id
        self.medications = medications
        self.price = price
        self.doctor = doctor
        self.problem = problem
        self.payment = None


class Payment(ABC):
    def __init__(self, amount):
        self.amount = amount
        self.paid_at = None

    @abstractmethod
    def process(self):
        pass


class Cash(Payment):
    def process(self):
        self.paid_at = datetime.now()
        return f"Paid {self.amount} EUR in cash"


class Check(Payment):
    def __init__(self, amount, check_number):
        super().__init__(amount)
        self.check_number = check_number

    def process(self):
        self.paid_at = datetime.now()
        return f"Paid {self.amount} EUR by check n°{self.check_number}"


class CreditCard(Payment):
    def __init__(self, amount, card_last4):
        super().__init__(amount)
        self.card_last4 = card_last4

    def process(self):
        self.paid_at = datetime.now()
        return f"Paid {self.amount} EUR by card ending {self.card_last4}"


if __name__ == "__main__":
    patient = Patient(1, "Ana", "ana@mail.com", "Paris")
    doctor = Doctor(2, "Dr House", "house@mail.com", "General medicine")
    organizer = Organizer(3, "Admin", "admin@mail.com")

    problem = patient.post_problem("Headache for 3 days")
    print(problem.status)

    organizer.review_problem(problem)
    print(problem.status)

    prescription = organizer.consult_doctor(doctor, problem, ["Paracetamol 1g"], 30)
    organizer.send_prescription(prescription, patient)
    print(problem.status, patient.prescriptions[0].medications)

    payment = patient.pay(prescription, CreditCard(30, "4242"))
    print(payment.process())

    organizer.forward_payment(prescription)
    print(doctor.balance)
