from django.dispatch import Signal, receiver

product_restocked = Signal()  # args: product

_registry = {}  # productId -> set of observers by type

def subscribe(product_id: str, obs_type: str, observer):
    if product_id not in _registry:
        _registry[product_id] = {"sms": set(), "email": set(), "dash": set()}
    _registry[product_id][obs_type].add(observer)

def unsubscribe_all(product_id: str, obs_type: str | None = None):
    if product_id not in _registry:
        return
    if obs_type is None:
        for k in _registry[product_id]:
            _registry[product_id][k].clear()
    else:
        _registry[product_id].get(obs_type, set()).clear()

@receiver(product_restocked)
def _notify(sender, **kwargs):
    p = kwargs.get("product")
    reg = _registry.get(p.get("id"), {})
    evt = {"productId": p.get("id"), "name": p.get("name"), "stock": p.get("stock")}
    for t in ("sms", "email", "dash"):
        for o in reg.get(t, []):
            try:
                o(evt)
            except Exception:
                pass
