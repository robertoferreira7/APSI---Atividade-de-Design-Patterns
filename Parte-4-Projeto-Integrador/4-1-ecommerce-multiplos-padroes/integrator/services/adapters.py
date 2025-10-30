class ExternalGateway:
    async def pay(self, payload: dict):
        return {"ok": True, "ref": f"GW-{round(payload.get('total', 0), 2)}"}

class GatewayAdapter:
    def __init__(self, gw: ExternalGateway | None = None):
        self.gw = gw or ExternalGateway()
    async def charge(self, amount: float, meta: dict | None = None):
        return await self.gw.pay({"total": amount, "details": meta or {}})
