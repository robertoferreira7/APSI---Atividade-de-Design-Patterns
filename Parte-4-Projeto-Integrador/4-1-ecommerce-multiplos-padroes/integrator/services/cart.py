class Item:
    def price(self) -> float:
        raise NotImplementedError

class SingleItem(Item):
    def __init__(self, product: dict, qty: int = 1):
        self.product = product
        self.qty = qty
    def price(self) -> float:
        return float(self.product["price"]) * int(self.qty)

class Bundle(Item):
    def __init__(self, children=None):
        self.children = children or []
    def add(self, child: Item):
        self.children.append(child)
    def price(self) -> float:
        return sum(c.price() for c in self.children) * 0.9  # 10% de desconto em bundles
