# logging_app/services/logger_service.py
from datetime import datetime

class LoggerService:
    # Variável de classe para armazenar a única instância (Singleton)
    _instance = None
    MAX_LOGS = 100 # Requisito: armazenar os últimos 100 logs em memória

    def __new__(cls):
        # Implementação do padrão Singleton: garante que apenas uma instância seja criada.
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            # Inicializa a lista de logs na primeira criação
            cls._instance.logs = [] 
            
        return cls._instance

    def _log(self, level, message):
        """
        Cria a entrada de log com timestamp, nível e mensagem.
        """
        entry = {
            'timestamp': datetime.now().isoformat(), # Requisito: incluir timestamp
            'level': level,                          # Requisito: incluir nível
            'message': message                       # Requisito: incluir mensagem
        }
        
        self.logs.append(entry)
        
        # Lógica para manter apenas os 100 logs mais recentes
        if len(self.logs) > self.MAX_LOGS:
            self.logs.pop(0)  # Remove o log mais antigo (índice 0)

    # Métodos para diferentes níveis de log
    def info(self, message):
        self._log('info', message)

    def warn(self, message):
        self._log('warn', message)

    def error(self, message):
        self._log('error', message)

    # Método para consultar os logs, usado pelo endpoint REST
    def get_recent_logs(self):
        return self.logs
        
# A instância Singleton global que será importada e usada em toda a aplicação
logger = LoggerService()