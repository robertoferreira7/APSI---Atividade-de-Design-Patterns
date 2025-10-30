from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.catalog import ProductFactory, ProductBuilder, save_product, restock, get_product
from .services.observers import SMSObserver, EmailObserver, DashboardObserver
from .services.signals import subscribe as sub
from .services.cart import SingleItem, Bundle
from .services.discounts import STRAT, combine
from .services.shipping import SHIP
from .services.chain import build_pipeline
from .services.payments import CreditCardProcessor, PaypalProcessor, BankTransferProcessor
from .services.facade import PaymentFacade
import asyncio

_OBS = {"sms": SMSObserver, "email": EmailObserver, "dash": DashboardObserver}

@api_view(["POST"])
def product_create(request):
    data = request.data or {}
    ptype = data.get("type")
    try:
        if ptype == "physical":
            p = ProductBuilder().name(data["name"]).price(data["price"]).stock(data.get("stock", 0)).weight(data.get("weight", 0)).build_physical()
        elif ptype == "digital":
            p = ProductBuilder().name(data["name"]).price(data["price"]).stock(data.get("stock", 0)).downloadUrl(data.get("downloadUrl")).build_digital()
        else:
            return Response({"error": "unknown type"}, status=status.HTTP_400_BAD_REQUEST)
        save_product(p)
        return Response(p, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def subscribe(request):
    pid = request.data.get("productId")
    typ = request.data.get("type")
    if not pid or typ not in _OBS:
        return Response({"error": "invalid"}, status=status.HTTP_400_BAD_REQUEST)
    sub(pid, typ, _OBS[typ]())
    return Response({"ok": True})

@api_view(["POST"])
def product_restock(request):
    pid = request.data.get("productId")
    qty = int(request.data.get("qty", 0))
    try:
        p = restock(pid, qty)
        return Response(p)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def cart_price(request):
    body = request.data or {}
    items = body.get("items", [])
    discounts = body.get("discounts", [])
    ship = body.get("shipping", {"type": "fixed"})
    # Composite
    nodes = []
    total_weight = 0.0
    for it in items:
        prod = get_product(it["productId"])
        if not prod:
            return Response({"error": "product not found"}, status=status.HTTP_400_BAD_REQUEST)
        nodes.append(SingleItem(prod, it.get("qty", 1)))
        if prod.get("kind") == "physical":
            total_weight += float(prod.get("weight", 0)) * it.get("qty", 1)
    cart = Bundle(nodes)
    total = cart.price()
    # Strategy + Decorator (descontos)
    fn_list = []
    for d in discounts:
        fn_list.append(lambda a, d=d: STRAT.get(d["type"], lambda x, **k: x)(a, **(d.get("params", {}))))
    if fn_list:
        total = combine(*[lambda x, fn=fn: fn(x)])(total)
    # Frete (Strategy)
    total = SHIP.get(ship.get("type", "fixed"), lambda a, **k: a)(total, **({"weightKg": total_weight} | ship.get("params", {})))
    return Response({"total": round(total, 2), "weightKg": round(total_weight, 3)})

@api_view(["POST"])
def checkout(request):
    body = request.data or {}
    items = body.get("items", [])
    discounts = body.get("discounts", [])
    ship = body.get("shipping", {"type": "fixed"})
    payment = body.get("payment", {"method": "credit", "info": {}})
    # Pricing preliminar (reuso do cálculo)
    nodes = []
    total_weight = 0.0
    for it in items:
        prod = get_product(it["productId"])
        if not prod:
            return Response({"error": "product not found"}, status=status.HTTP_400_BAD_REQUEST)
        nodes.append(SingleItem(prod, it.get("qty", 1)))
        if prod.get("kind") == "physical":
            total_weight += float(prod.get("weight", 0)) * it.get("qty", 1)
    total = Bundle(nodes).price()
    fn_list = [lambda a, d=d: STRAT.get(d["type"], lambda x, **k: x)(a, **(d.get("params", {}))) for d in discounts]
    if fn_list:
        total = combine(*[lambda x, fn=fn: fn(x)])(total)
    total = SHIP.get(ship.get("type", "fixed"), lambda a, **k: a)(total, **({"weightKg": total_weight} | ship.get("params", {})))
    # Chain para pedido
    chain = build_pipeline()
    ctx = {"items": items, "discount_factor": 1.0, "subtotal": total, "total": total}
    processed = chain.handle(ctx)
    if processed.get("error"):
        return Response(processed, status=status.HTTP_400_BAD_REQUEST)
    # Template Method (pagamentos)
    method = payment.get("method", "credit")
    info = payment.get("info", {})
    info["amount"] = processed["total"]
    if method == "credit":
        proc = CreditCardProcessor()
    elif method == "paypal":
        proc = PaypalProcessor()
    elif method == "bank":
        proc = BankTransferProcessor()
    else:
        return Response({"error": "unknown payment method"}, status=status.HTTP_400_BAD_REQUEST)
    pay_result = proc.process(info)
    # Facade + Adapter para liquidar com gateway externo
    facade = PaymentFacade()
    gw = asyncio.run(facade.settle(processed["total"], {"orderId": processed.get("orderId")}))
    return Response({"order": processed, "payment": pay_result, "gateway": gw})
