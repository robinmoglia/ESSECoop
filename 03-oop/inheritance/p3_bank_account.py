"""Problem 3: BankAccount / SavingsAccount"""

class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance = self.balance - amount
            return True
        else:
            return False

    def transfer(self, destination, amount):
        if self.withdraw(amount):
            destination.deposit(amount)
            return True
        else:
            return False


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.03):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance = self.balance * (1 + self.interest_rate)

    def check_balance(self):
        return self.balance


if __name__ == "__main__":
    a = BankAccount("FR001", 100)
    s = SavingsAccount("FR002", 1000, 0.05)
    print(a.transfer(s, 50))
    print(a.transfer(s, 500))
    s.add_interest()
    print(s.check_balance())
    print(a.balance)
