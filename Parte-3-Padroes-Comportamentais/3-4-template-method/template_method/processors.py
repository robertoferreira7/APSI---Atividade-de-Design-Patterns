from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    def process_payment(self, info: dict) -> dict:
        if not self.validate(info):
            return {"status": "failed", "reason": "validation error"}
        result = self.execute(info)
        self.notify(info, result)
        return result

    @abstractmethod
    def validate(self, info: dict) -> bool:
        pass

    @abstractmethod
    def execute(self, info: dict) -> dict:
        pass

    @abstractmethod
    def notify(self, info: dict, result: dict):
        pass


class CreditCardProcessor(PaymentProcessor):
    def validate(self, info):
        return "card_number" in info and len(str(info["card_number"])) == 16 and "amount" in info

    def execute(self, info):
        return {"status": "success", "method": "credit_card", "amount": info["amount"]}

    def notify(self, info, result):
        print(f"Email: pagamento via cartão confirmado, valor {info['amount']}")


class PayPalProcessor(PaymentProcessor):
    def validate(self, info):
        return "paypal_email" in info and "@" in info["paypal_email"] and "amount" in info

    def execute(self, info):
        return {"status": "success", "method": "paypal", "amount": info["amount"]}

    def notify(self, info, result):
        print(f"Webhook PayPal: pagamento de {info['amount']} processado")


class BankTransferProcessor(PaymentProcessor):
    def validate(self, info):
        return "account_number" in info and len(str(info["account_number"])) >= 5 and "amount" in info

    def execute(self, info):
        return {"status": "success", "method": "bank_transfer", "amount": info["amount"]}

    def notify(self, info, result):
        print(f"SMS: transferência de {info['amount']} confirmada")
