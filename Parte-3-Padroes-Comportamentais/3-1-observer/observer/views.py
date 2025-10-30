from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import market, SMSObserver, EmailObserver, DashboardObserver, subscribe as sub, unsubscribe as unsub

_VALID = {"sms": SMSObserver, "email": EmailObserver, "dash": DashboardObserver}

@api_view(["POST"])
def subscribe(request):
    symbol = request.data.get("symbol")
    obs_type = request.data.get("type")
    if not symbol or obs_type not in _VALID:
        return Response({"error": "invalid params"}, status=status.HTTP_400_BAD_REQUEST)
    obs_cls = _VALID[obs_type]
    sub(symbol, obs_type, obs_cls())
    return Response({"ok": True})

@api_view(["POST"])
def unsubscribe(request):
    symbol = request.data.get("symbol")
    obs_type = request.data.get("type")  # opcional
    if not symbol:
        return Response({"error": "invalid params"}, status=status.HTTP_400_BAD_REQUEST)
    if obs_type and obs_type not in _VALID:
        return Response({"error": "invalid type"}, status=status.HTTP_400_BAD_REQUEST)
    unsub(symbol, obs_type)
    return Response({"ok": True})

@api_view(["POST"])
def price(request):
    symbol = request.data.get("symbol")
    price = request.data.get("price")
    if not symbol or not isinstance(price, (int, float)):
        return Response({"error": "invalid params"}, status=status.HTTP_400_BAD_REQUEST)
    market.set_price(symbol, float(price))
    return Response({"ok": True, "symbol": symbol, "price": float(price)})
