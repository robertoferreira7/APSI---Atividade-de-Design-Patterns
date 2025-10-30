from django.dispatch import Signal, receiver

price_changed = Signal()  # args: symbol, old, price

_registry = {}

def _ensure_symbol(symbol: str):
    if symbol not in _registry:
        _registry[symbol] = {"sms": set(), "email": set(), "dash": set()}
    return _registry[symbol]

def subscribe(symbol: str, obs_type: str, observer):
    r = _ensure_symbol(symbol)
    r[obs_type].add(observer)

def unsubscribe_all(symbol: str, obs_type: str | None = None):
    r = _ensure_symbol(symbol)
    if obs_type:
        r[obs_type].clear()
    else:
        for k in r:
            r[k].clear()

@receiver(price_changed)
def _dispatch_to_observers(sender, **kwargs):
    symbol = kwargs.get("symbol")
    evt = {"symbol": symbol, "old": kwargs.get("old"), "price": kwargs.get("price")}
    r = _registry.get(symbol, {})
    for t in ("sms", "email", "dash"):
        for o in r.get(t, []):
            try:
                o(evt)
            except Exception:
                pass
