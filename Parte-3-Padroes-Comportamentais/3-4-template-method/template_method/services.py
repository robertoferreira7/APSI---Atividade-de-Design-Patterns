from .processors import CreditCardProcessor, PayPalProcessor, BankTransferProcessor

def get_processor(method: str):
    match method:
        case "credit":
            return CreditCardProcessor()
        case "paypal":
            return PayPalProcessor()
        case "bank":
            return BankTransferProcessor()
        case _:
            raise ValueError("Unknown payment method")

def process_payment(method: str, info: dict):
    processor = get_processor(method)
    return processor.process_payment(info)
