"""UML exercise 2: ABCD Records, mail-order CDs and tapes (slide 68)"""

from abc import ABC, abstractmethod
from datetime import date


class Item(ABC):
    def __init__(self, code, title, price, stock):
        self.code = code
        self.title = title
        self.price = price
        self.stock = stock

    def is_available(self, quantity=1):
        return self.stock >= quantity


class CD(Item):
    pass


class Tape(Item):
    pass


class Member(ABC):
    def __init__(self, member_id, name, address):
        self.member_id = member_id
        self.name = name
        self.address = address

    @abstractmethod
    def discount_rate(self):
        pass

    def can_order_unavailable(self):
        return False

    def place_order(self, order_id):
        return Order(order_id, self)


class RegularMember(Member):
    def discount_rate(self):
        return 0


class RoyalMember(Member):
    def discount_rate(self):
        return 0.10

    def can_order_unavailable(self):
        return True


class MembershipApplication:
    def __init__(self, applicant_name, address):
        self.applicant_name = applicant_name
        self.address = address
        self.sent_on = date.today()


class OrderLine:
    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity
        self.backordered = False

    def subtotal(self):
        return self.item.price * self.quantity


class Order:
    def __init__(self, order_id, member):
        self.order_id = order_id
        self.member = member
        self.order_date = date.today()
        self.lines = []
        self.status = "new"
        self.payment = None

    def add_item(self, item, quantity=1):
        self.lines.append(OrderLine(item, quantity))

    def total(self):
        gross = sum(line.subtotal() for line in self.lines if not line.backordered)
        return round(gross * (1 - self.member.discount_rate()), 2)


class Invoice:
    def __init__(self, order):
        self.order = order
        self.amount = order.total()

    def print(self):
        return f"Invoice order {self.order.order_id}: {self.amount} EUR"


class ShippingList:
    def __init__(self, order):
        self.order = order
        self.items = [line.item.title for line in order.lines if not line.backordered]

    def print(self):
        return f"Ship to {self.order.member.address}: {', '.join(self.items)}"


class Payment(ABC):
    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def describe(self):
        pass


class Cash(Payment):
    def describe(self):
        return f"{self.amount} EUR in cash"


class Check(Payment):
    def __init__(self, amount, check_number):
        super().__init__(amount)
        self.check_number = check_number

    def describe(self):
        return f"{self.amount} EUR by check n°{self.check_number}"


class BankDraft(Payment):
    def __init__(self, amount, bank):
        super().__init__(amount)
        self.bank = bank

    def describe(self):
        return f"{self.amount} EUR by bank draft from {self.bank}"


class DailyRecordsFile:
    def __init__(self):
        self.orders = []

    def save(self, order):
        self.orders.append(order)


class OrderProcessingClerk:
    def __init__(self, name, members, records):
        self.name = name
        self.members = members
        self.records = records

    def verify_membership(self, person_id):
        return person_id in self.members

    def send_membership_application(self, name, address):
        return MembershipApplication(name, address)

    def process_order(self, order):
        for line in order.lines:
            if not line.item.is_available(line.quantity):
                if order.member.can_order_unavailable():
                    line.backordered = True
                else:
                    raise ValueError(f"{line.item.title} is not available")
            else:
                line.item.stock -= line.quantity
        order.status = "processed"
        self.records.save(order)
        return Invoice(order), ShippingList(order)


class CollectionDepartmentClerk:
    def __init__(self, name):
        self.name = name

    def collect_payment(self, order, payment):
        order.payment = payment
        order.status = "paid"
        return payment.describe()


if __name__ == "__main__":
    records = DailyRecordsFile()
    royal = RoyalMember(1, "Ana", "12 rue de Paris")
    clerk = OrderProcessingClerk("Tom", {royal.member_id: royal}, records)
    collector = CollectionDepartmentClerk("Lea")

    print(clerk.verify_membership(99))
    print(clerk.send_membership_application("Bob", "Lyon").applicant_name)

    abbey_road = CD("CD01", "Abbey Road", 20, stock=5)
    rare_cd = CD("CD02", "Rare Live", 30, stock=0)

    order = royal.place_order(1001)
    order.add_item(abbey_road)
    order.add_item(rare_cd)

    invoice, shipping = clerk.process_order(order)
    print([line.backordered for line in order.lines])
    print(invoice.print())
    print(shipping.print())
    print(collector.collect_payment(order, Check(invoice.amount, "0042")))
    print(len(records.orders), order.status)
