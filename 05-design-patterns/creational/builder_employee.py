"""Builder pattern: HR employee onboarding system"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: Optional[str] = None
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: Optional[str] = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self):
        self._data = {}

    def with_name(self, first_name, last_name):
        self._data["first_name"] = first_name
        self._data["last_name"] = last_name
        return self

    def with_email(self, email):
        self._data["email"] = email
        return self

    def with_job(self, department, position, salary):
        self._data.update(department=department, position=position, salary=salary)
        return self

    def with_start_date(self, start_date):
        self._data["start_date"] = start_date
        return self

    def with_manager(self, manager_id):
        self._data["manager_id"] = manager_id
        return self

    def with_contact(self, phone=None, address=None, emergency_contact=None):
        self._data.update(phone=phone, address=address, emergency_contact=emergency_contact)
        return self

    def with_equipment(self, laptop=False, parking=False):
        self._data.update(has_laptop=laptop, has_parking=parking)
        return self

    def with_access(self, vpn=False, admin=False):
        self._data.update(has_vpn_access=vpn, has_admin_rights=admin)
        return self

    def with_office(self, office_location):
        self._data["office_location"] = office_location
        return self

    def with_contract(self, contract_type):
        self._data["contract_type"] = contract_type
        return self

    def build(self) -> Employee:
        if not self._data.get("first_name") or not self._data.get("last_name"):
            raise ValueError("Name is required")
        if "@" not in self._data.get("email", ""):
            raise ValueError("Valid email is required")
        if self._data.get("salary", 0) < 0:
            raise ValueError("Salary cannot be negative")
        return Employee(**self._data)


class DeveloperBuilder(EmployeeBuilder):
    def __init__(self, first_name, last_name, email):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job("Engineering", "Senior Developer", 75000)
             .with_equipment(laptop=True)
             .with_access(vpn=True, admin=True)
             .with_office("Paris HQ"))


class InternBuilder(EmployeeBuilder):
    def __init__(self, first_name, last_name, email, department):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job(department, "Intern", 15000)
             .with_equipment(laptop=True)
             .with_office("Paris HQ")
             .with_contract("internship"))


if __name__ == "__main__":
    employee = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .build()
    )
    print(employee)

    dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
    print(dev.position, dev.has_admin_rights)

    intern = InternBuilder("Jane", "Smith", "jane.smith@company.com", "Marketing").with_manager(42).build()
    print(intern.position, intern.contract_type, intern.manager_id)
