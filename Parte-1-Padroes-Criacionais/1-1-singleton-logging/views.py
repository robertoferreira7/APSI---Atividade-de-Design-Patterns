# logging_app/views.py

from django.http import JsonResponse
# Importa a instância Singleton que criamos no final do logger_service.py
from .services.logger_service import logger 

def get_logs_view(request):
    """
    Endpoint REST para consultar os logs (GET /logs/)
    """
    
    # Exemplo de uso do Singleton em outra parte da aplicação:
    logger.info(f"Requisição GET recebida para {request.path}")
    
    recent_logs = logger.get_recent_logs()
    
    # Retorna o JSON com a lista de logs
    return JsonResponse(recent_logs, safe=False)