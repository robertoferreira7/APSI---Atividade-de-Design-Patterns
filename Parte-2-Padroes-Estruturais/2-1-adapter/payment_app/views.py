from django.shortcuts import render

# payment_app/views.py

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Importa a instância do Adapter (que se comporta como o LegacyPaymentProcessor)
from .services.payment_services import payment_adapter

@csrf_exempt
@require_http_methods(["POST"])
def process_payment(request):
    """
    Endpoint da API que atua como o CLIENTE, usando a interface legada (o Adapter).
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Requisição inválida. O corpo deve ser JSON."}, status=400)

    # O CLIENTE só conhece a interface LEGADA (order_id, amount)
    order_id = data.get('order_id')
    amount = data.get('amount')
    
    if not order_id or not isinstance(amount, (int, float)):
         return JsonResponse({"error": "Campos 'order_id' e 'amount' são obrigatórios e válidos."}, status=400)
    
    try:
        # AQUI O CLIENTE CHAMA A INTERFACE LEGADA (process_legacy_payment),
        # que é implementada pelo ADAPTER, traduzindo para o novo sistema.
        response_message = payment_adapter.process_legacy_payment(order_id, amount)
        
        return JsonResponse({"message": response_message}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Erro interno: {e}"}, status=500)
