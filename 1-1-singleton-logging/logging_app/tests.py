# logging_app/tests.py
from django.test import TestCase, Client
# Importamos a classe para testar o padrão e a instância logger
from logging_app.services.logger_service import LoggerService, logger

class SingletonTest(TestCase):
    
    def setUp(self):
        # Limpa os logs antes de cada teste para isolamento
        logger.logs = [] 

    # 1. TESTE DO PADRÃO SINGLETON (UNICIDADE)
    def test_logger_is_a_singleton(self):
        """Verifica se duas "instanciações" retornam o mesmo objeto."""
        
        logger1 = LoggerService()
        logger2 = LoggerService()
        
        # O Singleton deve garantir que os dois objetos são idênticos
        self.assertIs(logger1, logger2)

class LoggerLogicTest(TestCase):
    
    def setUp(self):
        self.logger = LoggerService()
        self.logger.logs = [] 

    # 2. TESTE DOS REQUISITOS DE CONTEÚDO (timestamp, nível, mensagem)
    def test_log_methods_and_content(self):
        """Verifica se os métodos de log funcionam e se o conteúdo está correto."""
        
        test_message = "Teste de log de erro"
        self.logger.error(test_message)
        
        logs = self.logger.get_recent_logs()
        
        self.assertEqual(len(logs), 1)
        log_entry = logs[0]
        
        # Verifica os requisitos de conteúdo
        self.assertIn('timestamp', log_entry)
        self.assertEqual(log_entry['level'], 'error')
        self.assertEqual(log_entry['message'], test_message)

    # 3. TESTE DO LIMITE DE 100 LOGS
    def test_logger_respects_100_logs_limit(self):
        """Verifica se o serviço armazena apenas os últimos 100 logs em memória."""
        
        MAX_LOGS = self.logger.MAX_LOGS 
        EXCESS_COUNT = 5
        TOTAL_TO_ADD = MAX_LOGS + EXCESS_COUNT
        
        # Adiciona 105 logs
        for i in range(1, TOTAL_TO_ADD + 1):
            self.logger.info(f"Log número {i}")
        
        logs = self.logger.get_recent_logs()
        
        # Verifica se o tamanho final é exatamente 100
        self.assertEqual(len(logs), MAX_LOGS)
        
        # Verifica se o log mais antigo (índice 0) é o log número 6 (os 5 primeiros foram removidos)
        self.assertEqual(logs[0]['message'], 'Log número 6')
        
        # Verifica se o log mais recente (índice 99) é o log número 105
        self.assertEqual(logs[MAX_LOGS - 1]['message'], 'Log número 105')


class LogAPIViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.logger = logger # A instância global
        self.logger.logs = [] # Limpa para o teste
        
    # 4. TESTE DO ENDPOINT REST
    def test_get_logs_endpoint(self):
        """Verifica se o endpoint REST retorna os logs corretamente."""
        
        # 1. Este log é adicionado ao Singleton ANTES da chamada da API
        self.logger.warn("Teste de API") 
        
        # 2. Usa o Cliente de Teste do Django para acessar o endpoint
        response = self.client.get('/logs/')
        
        self.assertEqual(response.status_code, 200)
        
        content = response.json()
        
        # O log da requisição GET (adicionado pela view) e o log acima, totalizando 2 logs
        self.assertEqual(len(content), 2) 
        
        # CORREÇÃO: O log 'Teste de API' está na posição 0
        self.assertEqual(content[0]['message'], 'Teste de API')
        self.assertEqual(content[0]['level'], 'warn')
        
        # Verifica o log adicionado PELA VIEW (índice 1)
        self.assertIn('Requisição GET recebida', content[1]['message'])