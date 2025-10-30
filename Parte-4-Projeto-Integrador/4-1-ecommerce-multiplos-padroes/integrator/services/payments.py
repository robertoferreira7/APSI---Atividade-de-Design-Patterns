from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    def process(self, info: dict) -> dict:
        if not self.validate(info):
            return {"status": "failed", "reason": "validation"}
        res = self.execute(info)
        self.notify(info, res)
        return res
    @abstractmethod
    def validate(self, info: dict) -> bool: ...
    @abstractmethod
    def execute(self, info: dict) -> dict: ...
    @abstractmethod
    def notify(self, info: dict, result: dict): ...

class CreditCardProcessor(PaymentProcessor):
    def validate(self, info): return "card_number" in info and len(str(info["card_number"])) == 16 and "amount" in info
    def execute(self, info): return {"status": "success", "method": "credit", "amount": info["amount"]}
    def notify(self, info, result): print(f"Email: cartão aprovado {info['amount']}")

class PaypalProcessor(PaymentProcessor):
    def validate(self, info): return "paypal_email" in info and "@" in info["paypal_email"] and "amount" in info
    def execute(self, info): return {"status": "success", "method": "paypal", "amount": info["amount"]}
    def notify(self, info, result): print(f"Webhook: paypal pago {info['amount']}")

class BankTransferProcessor(PaymentProcessor):
    def validate(self, info): return "account_number" in info and "amount" in info
    def execute(self, info): return {"status": "pending", "method": "bank", "amount": info["amount"]}
    def notify(self, info, result): print(f"SMS: transferência {info['amount']}")
