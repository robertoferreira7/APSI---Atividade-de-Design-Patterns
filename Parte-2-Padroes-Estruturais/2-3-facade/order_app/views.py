from django.shortcuts import render

# order_app/views.py

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Importa a instância da Facade (o único ponto de contato do Cliente)
from .services.order_facade import order_facade

@csrf_exempt
@require_http_methods(["POST"])
def place_order_api(request):
    """
    Endpoint da API que atua como o CLIENTE, usando apenas o método simplificado da Facade.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Requisição inválida. O corpo deve ser JSON."}, status=400)

    customer_id = data.get('customer_id')
    products = data.get('products', [])
    total_amount = data.get('total_amount')
    
    if not customer_id or not products or not isinstance(total_amount, (int, float)):
         return JsonResponse({"error": "Campos 'customer_id', 'products' e 'total_amount' são obrigatórios."}, status=400)
    
    # O CLIENTE só interage com o método simplificado da FACADE!
    result = order_facade.place_order(customer_id, products, total_amount)
    
    if result['success']:
        return JsonResponse(result, status=201)
    else:
        return JsonResponse(result, status=400)
