"""Factory pattern: refactor a payment system"""

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> bool:
        pass

    @abstractmethod
    def fee(self, amount: float) -> float:
        pass

    @property
    @abstractmethod
    def method(self) -> str:
        pass

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": f"Invalid {self.method} details"}
        fee = round(self.fee(amount), 2)
        return {"success": True, "method": self.method, "amount": round(amount + fee, 2), "fee": fee}


class CreditCardProcessor(PaymentProcessor):
    method = "credit_card"

    def validate(self, details):
        card = details.get("card_number") or ""
        cvv = details.get("cvv") or ""
        return len(card) == 16 and len(cvv) == 3

    def fee(self, amount):
        return amount * 0.029


class BankTransferProcessor(PaymentProcessor):
    method = "bank_transfer"

    def validate(self, details):
        return len(details.get("iban") or "") >= 15

    def fee(self, amount):
        return 1.50


class PayPalProcessor(PaymentProcessor):
    method = "paypal"

    def validate(self, details):
        return "@" in (details.get("email") or "")

    def fee(self, amount):
        return amount * 0.034 + 0.30


class PaymentFactory:
    _processors = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        if payment_type not in self._processors:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return self._processors[payment_type]()

    @classmethod
    def register(cls, payment_type, processor_class):
        cls._processors[payment_type] = processor_class


if __name__ == "__main__":
    factory = PaymentFactory()

    processor = factory.get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

    processor = factory.get_processor("bank_transfer")
    print(processor.process(100.0, {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}))

    processor = factory.get_processor("paypal")
    print(processor.process(100.0, {"email": "robin@mail.com"}))
    print(processor.process(100.0, {"email": "wrong"}))

    class ApplePayProcessor(PaymentProcessor):
        method = "apple_pay"

        def validate(self, details):
            return bool(details.get("token"))

        def fee(self, amount):
            return amount * 0.015

    PaymentFactory.register("apple_pay", ApplePayProcessor)
    print(factory.get_processor("apple_pay").process(100.0, {"token": "abc"}))
