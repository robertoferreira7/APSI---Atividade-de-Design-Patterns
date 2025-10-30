from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import process_payment

@api_view(["POST"])
def process(request):
    method = request.data.get("method")
    info = request.data.get("info", {})
    if not method or not isinstance(info, dict):
        return Response({"error": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        result = process_payment(method, info)
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
