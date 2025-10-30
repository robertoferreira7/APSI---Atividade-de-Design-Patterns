from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import price_service

@api_view(["POST"])
def select_strategy(request):
    name = request.data.get("name")
    params = request.data.get("params", {})
    try:
        price_service.select_strategy(name, **params)
        return Response({"ok": True, "strategy": name})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def calculate(request):
    amount = request.data.get("amount")
    if not isinstance(amount, (int, float)):
        return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        result = price_service.calculate(float(amount))
        return Response({"final_price": result})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
