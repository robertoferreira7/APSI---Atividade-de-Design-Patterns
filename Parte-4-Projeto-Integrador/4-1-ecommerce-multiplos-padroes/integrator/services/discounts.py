def percent(amount: float, p: float = 0.0) -> float:
    return amount * (1 - p/100.0)

def fixed(amount: float, v: float = 0.0) -> float:
    return max(0.0, amount - v)

STRAT = {
    "percent": lambda a, **k: percent(a, k.get("p", 0.0)),
    "fixed": lambda a, **k: fixed(a, k.get("v", 0.0)),
}

def combine(*funcs):
    def _apply(amount: float) -> float:
        for fn in funcs:
            amount = fn(amount)
        return amount
    return _apply
