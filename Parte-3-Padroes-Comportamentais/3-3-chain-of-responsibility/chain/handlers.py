from abc import ABC, abstractmethod

class OrderHandler(ABC):
    def __init__(self, next_handler=None):
        self.next = next_handler

    @abstractmethod
    def handle(self, order: dict):
        pass

    def call_next(self, order):
        if self.next:
            return self.next.handle(order)
        return order


class InventoryValidator(OrderHandler):
    def handle(self, order):
        if order.get("items_in_stock", True):
            order["inventory_ok"] = True
            return self.call_next(order)
        order["status"] = "Failed: Out of stock"
        return order


class FraudDetector(OrderHandler):
    def handle(self, order):
        if order.get("user_flagged", False):
            order["status"] = "Failed: Fraud detected"
            return order
        order["fraud_check"] = "Passed"
        return self.call_next(order)


class PricingCalculator(OrderHandler):
    def handle(self, order):
        total = sum(item["price"] * item.get("qty", 1) for item in order.get("items", []))
        order["total"] = total
        return self.call_next(order)


class DiscountApplier(OrderHandler):
    def handle(self, order):
        discount = order.get("discount", 0)
        order["total_after_discount"] = order["total"] * (1 - discount)
        return self.call_next(order)


class OrderPersister(OrderHandler):
    def handle(self, order):
        order["status"] = "Success"
        order["saved"] = True
        return order
