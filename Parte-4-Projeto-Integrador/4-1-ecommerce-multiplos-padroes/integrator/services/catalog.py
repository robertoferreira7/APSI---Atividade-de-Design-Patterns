import uuid
from .signals import product_restocked

PRODUCTS = {}  # in-memory

class ProductFactory:
    @staticmethod
    def create(ptype: str, **opts):
        base = {"id": str(uuid.uuid4()), "name": opts.get("name"), "price": float(opts.get("price", 0)), "stock": int(opts.get("stock", 0))}
        if ptype == "digital":
            base.update({"kind": "digital", "downloadUrl": opts.get("downloadUrl")})
        elif ptype == "physical":
            base.update({"kind": "physical", "weight": float(opts.get("weight", 0))})
        else:
            raise ValueError("unknown product type")
        return base

class ProductBuilder:
    def __init__(self):
        self._p = {}
    def name(self, v): self._p["name"] = v; return self
    def price(self, v): self._p["price"] = float(v); return self
    def stock(self, v): self._p["stock"] = int(v); return self
    def weight(self, v): self._p["weight"] = float(v); return self
    def downloadUrl(self, v): self._p["downloadUrl"] = v; return self
    def build_physical(self):
        from .catalog import ProductFactory
        return ProductFactory.create("physical", **self._p)
    def build_digital(self):
        from .catalog import ProductFactory
        return ProductFactory.create("digital", **self._p)

def save_product(p: dict):
    PRODUCTS[p["id"]] = p
    return p

def get_product(pid: str):
    return PRODUCTS.get(pid)

def restock(pid: str, qty: int):
    p = get_product(pid)
    if not p:
        raise ValueError("product not found")
    p["stock"] = p.get("stock", 0) + qty
    product_restocked.send(sender=ProductFactory, product=p)
    return p
