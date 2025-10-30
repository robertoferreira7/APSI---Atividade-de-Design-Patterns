from .handlers import (
    InventoryValidator,
    FraudDetector,
    PricingCalculator,
    DiscountApplier,
    OrderPersister,
)

def build_chain():
    return InventoryValidator(
        FraudDetector(
            PricingCalculator(
                DiscountApplier(
                    OrderPersister()
                )
            )
        )
    )

def process_order(order_data):
    chain = build_chain()
    return chain.handle(order_data)
