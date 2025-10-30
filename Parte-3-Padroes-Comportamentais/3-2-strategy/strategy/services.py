from .strategies import PercentageDiscount, FixedDiscount, BuyXGetYDiscount

class PriceService:
    def __init__(self):
        self.current_strategy = None

    def select_strategy(self, name: str, **kwargs):
        match name:
            case "percent":
                self.current_strategy = PercentageDiscount(kwargs.get("percent", 10))
            case "fixed":
                self.current_strategy = FixedDiscount(kwargs.get("value", 5))
            case "buyxgety":
                self.current_strategy = BuyXGetYDiscount(
                    kwargs.get("x", 2),
                    kwargs.get("y", 1),
                    kwargs.get("price_per_item", 10)
                )
            case _:
                raise ValueError("Unknown strategy")
        return self.current_strategy

    def calculate(self, amount: float) -> float:
        if not self.current_strategy:
            raise ValueError("No discount strategy selected")
        return self.current_strategy.apply_discount(amount)

price_service = PriceService()
