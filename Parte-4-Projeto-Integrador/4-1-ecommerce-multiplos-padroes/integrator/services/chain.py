from .catalog import get_product
DB_ORDERS = {}
_NEXT_ID = 1

class BaseHandler:
    def __init__(self, nxt=None):
        self._next = nxt
    def set_next(self, nxt):
        self._next = nxt
        return nxt
    def handle(self, ctx: dict):
        return self._next.handle(ctx) if self._next else ctx

class InventoryValidator(BaseHandler):
    def handle(self, ctx: dict):
        for it in ctx.get("items", []):
            p = get_product(it["productId"])
            if not p or p.get("stock", 0) < it.get("qty", 1):
                ctx["error"] = "Estoque insuficiente"
                return ctx
        return super().handle(ctx)

class FraudDetector(BaseHandler):
    def handle(self, ctx: dict):
        if ctx.get("total", 0) > 20000:
            ctx["error"] = "Suspeita de fraude"
            return ctx
        return super().handle(ctx)

class PricingCalculator(BaseHandler):
    def handle(self, ctx: dict):
        ctx["subtotal"] = sum(get_product(i["productId"])["price"] * i.get("qty", 1) for i in ctx.get("items", []))
        return super().handle(ctx)

class DiscountApplier(BaseHandler):
    def handle(self, ctx: dict):
        disc = ctx.get("discount_factor", 1.0)
        ctx["total"] = round(ctx["subtotal"] * disc, 2)
        return super().handle(ctx)

class OrderPersister(BaseHandler):
    def handle(self, ctx: dict):
        global _NEXT_ID
        if ctx.get("error"):
            return ctx
        oid = _NEXT_ID
        _NEXT_ID += 1
        DB_ORDERS[oid] = {"id": oid, **ctx}
        ctx["orderId"] = oid
        # debita do estoque
        for it in ctx.get("items", []):
            p = get_product(it["productId"])
            p["stock"] -= it.get("qty", 1)
        return super().handle(ctx)

def build_pipeline():
    inv = InventoryValidator()
    fraud = inv.set_next(FraudDetector())
    price = fraud.set_next(PricingCalculator())
    disc = price.set_next(DiscountApplier())
    save = disc.set_next(OrderPersister())
    return inv
