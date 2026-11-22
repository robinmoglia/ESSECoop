# Hospital management system

Patients post health problems online. The organizer (also the administrator) reviews each problem and consults a doctor, the doctor writes a prescription, the organizer sends it to the patient, the patient pays (cash, check or credit card) and the organizer forwards the payment to the doctor.

## Class diagram

```mermaid
classDiagram
    class User {
        <<abstract>>
        -user_id: int
        -name: str
        -email: str
        +login()
        +logout()
    }
    class Patient {
        -address: str
        +post_problem(description) HealthProblem
        +receive_prescription(prescription)
        +pay(prescription, payment) Payment
    }
    class Doctor {
        -speciality: str
        -balance: float
        +write_prescription(problem, medications, price) Prescription
        +receive_payment(amount)
    }
    class Organizer {
        +review_problem(problem)
        +consult_doctor(doctor, problem, medications, price) Prescription
        +send_prescription(prescription, patient)
        +forward_payment(prescription)
    }
    class HealthProblem {
        -problem_id: int
        -description: str
        -created_at: datetime
        -status: ProblemStatus
    }
    class ProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class Prescription {
        -prescription_id: int
        -medications: list~str~
        -price: float
    }
    class Payment {
        <<abstract>>
        -amount: float
        -paid_at: datetime
        +process()*
    }
    class Cash
    class Check {
        -check_number: str
    }
    class CreditCard {
        -card_last4: str
    }

    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- CreditCard

    Patient "1" *-- "0..*" HealthProblem : posts
    HealthProblem "1" *-- "0..1" Prescription : leads to
    Prescription "1" --> "0..1" Payment : paid by
    Doctor "1" --> "0..*" Prescription : writes
    Organizer "1" --> "0..*" HealthProblem : reviews
    Organizer "1..*" --> "1..*" Doctor : consults
    HealthProblem ..> ProblemStatus
```

## Design choices

- **Inheritance**: `Patient`, `Doctor` and `Organizer` share id, name, email, login and logout, so they inherit from an abstract `User`.
- **Composition** (filled diamond): a `HealthProblem` cannot exist without its `Patient`, and a `Prescription` cannot exist without the `HealthProblem` it answers.
- **Association**: a `Doctor` writes prescriptions and an `Organizer` reviews problems, but both exist independently.
- **Payment types**: `Payment` is an abstract class with an abstract `process()` method. `Cash`, `Check` and `CreditCard` each implement it. This is polymorphism, and the Strategy pattern: the patient pays the same way whatever the method.
- **Status**: an enumeration tracks each problem (pending, in-review, resolved).

## Sequence diagram: from problem to payment

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor
    P->>O: post_problem(description)
    O->>O: review_problem(problem)
    O->>D: consult_doctor(problem)
    D-->>O: prescription
    O->>P: send_prescription(prescription)
    P->>O: pay(prescription, payment)
    O->>D: forward_payment(prescription)
```

## Run

```bash
python3 hospital.py
```
