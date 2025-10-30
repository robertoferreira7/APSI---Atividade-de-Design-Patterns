def fixed(amount: float, **_):
    return amount + 20.0

def by_weight(amount: float, weightKg: float = 1.0):
    return amount + 5.0 * float(weightKg)

SHIP = {"fixed": fixed, "byWeight": by_weight}
