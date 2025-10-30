from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import process_order

@api_view(["POST"])
def process(request):
    order = request.data
    result = process_order(order)
    return Response(result)
