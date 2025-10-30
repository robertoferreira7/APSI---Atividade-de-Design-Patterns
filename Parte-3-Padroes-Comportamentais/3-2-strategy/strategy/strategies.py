from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        pass


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent
    def apply_discount(self, amount: float) -> float:
        return amount * (1 - self.percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, value: float):
        self.value = value
    def apply_discount(self, amount: float) -> float:
        return max(0, amount - self.value)


class BuyXGetYDiscount(DiscountStrategy):
    def __init__(self, x: int, y: int, price_per_item: float):
        self.x, self.y, self.price = x, y, price_per_item
    def apply_discount(self, amount: float) -> float:
        total_items = amount / self.price
        free_items = (total_items // (self.x + self.y)) * self.y
        return self.price * (total_items - free_items)
