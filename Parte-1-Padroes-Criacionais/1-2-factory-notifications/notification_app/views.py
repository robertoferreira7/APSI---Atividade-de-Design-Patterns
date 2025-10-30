from django.shortcuts import render

# notification_app/views.py

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .services.notification_factory import notification_factory # Importa a Factory

@csrf_exempt
@require_http_methods(["POST"])
def send_notification(request):
    """
    Endpoint da API que usa o Factory Method para enviar notificações.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Requisição inválida. O corpo deve ser JSON."}, status=400)

    notification_type = data.get('type')
    recipient = data.get('recipient')
    content = data.get('content')

    if not notification_type or not recipient or not content:
        return JsonResponse({"error": "Campos 'type', 'recipient' e 'content' são obrigatórios."}, status=400)

    try:
        # 1. USO DA FACTORY: Cria o objeto de serviço correto (Factory Method)
        service = notification_factory.get_notification_service(notification_type)

        # 2. Executa a operação (Interface do Produto Abstrato)
        response_message = service.send(recipient, content, **data)

        return JsonResponse({"message": response_message}, status=200)

    except ValueError as e:
        # Captura o erro da Factory (tipo não suportado)
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Erro interno: {e}"}, status=500)

# Create your views here.
