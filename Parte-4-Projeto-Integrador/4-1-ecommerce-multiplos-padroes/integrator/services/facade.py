from .adapters import GatewayAdapter

class PaymentFacade:
    def __init__(self, adapter: GatewayAdapter | None = None):
        self.adapter = adapter or GatewayAdapter()
    async def settle(self, amount: float, meta: dict | None = None):
        return await self.adapter.charge(amount, meta or {})
