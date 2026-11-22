"""Decorator pattern: order pricing system"""

from abc import ABC, abstractmethod


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self.base_price = base_price

    def get_cost(self):
        return self.base_price

    def get_description(self):
        return f"Base price: {self.base_price}€"


class OrderDecorator(OrderComponent):
    def __init__(self, order: OrderComponent):
        self._order = order

    def get_cost(self):
        return self._order.get_cost()

    def get_description(self):
        return self._order.get_description()


class ExpressShippingDecorator(OrderDecorator):
    def get_cost(self):
        return self._order.get_cost() + 15.00

    def get_description(self):
        return self._order.get_description() + "\nExpress shipping: +15.0€"


class InsuranceDecorator(OrderDecorator):
    def _insurance(self):
        order = self._order
        while isinstance(order, OrderDecorator):
            order = order._order
        return round(order.get_cost() * 0.05, 2)

    def get_cost(self):
        return self._order.get_cost() + self._insurance()

    def get_description(self):
        return self._order.get_description() + f"\nInsurance (5%): +{self._insurance()}€"


class GiftWrapDecorator(OrderDecorator):
    def get_cost(self):
        return self._order.get_cost() + 5.00

    def get_description(self):
        return self._order.get_description() + "\nGift wrap: +5.0€"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order, percent):
        super().__init__(order)
        self.percent = percent

    def _discount(self):
        return round(self._order.get_cost() * self.percent / 100, 2)

    def get_cost(self):
        return round(self._order.get_cost() - self._discount(), 2)

    def get_description(self):
        return self._order.get_description() + f"\nDiscount ({self.percent}%): -{self._discount()}€"


class PremiumMemberDecorator(OrderDecorator):
    def _discount(self):
        return round(self._order.get_cost() * 0.10, 2)

    def get_cost(self):
        return round(self._order.get_cost() - self._discount(), 2)

    def get_description(self):
        return self._order.get_description() + f"\nPremium member (10%): -{self._discount()}€"


if __name__ == "__main__":
    simple = BaseOrder(100.00)
    print(simple.get_description())
    print(f"Total: {simple.get_cost()}€")

    print("\n---\n")

    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    print(order.get_description())
    print(f"Total: {order.get_cost()}€")
