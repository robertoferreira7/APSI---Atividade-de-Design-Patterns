from django.test import TestCase

# 2-1-adapter-payment/payment_app/tests.py

from django.test import TestCase, Client
from django.urls import reverse

# Importa as classes do padrão e a instância do Adapter
from .services.payment_services import (
    LegacyPaymentAdapter,
    NewPaymentSystem,
    LegacyPaymentProcessor,
    payment_adapter
)

class AdapterPatternTests(TestCase):
    """
    Testes unitários para validar a lógica do Padrão Adapter.
    """
    
    def setUp(self):
        # Cria uma nova instância do Novo Sistema e do Adapter para isolamento
        self.new_system = NewPaymentSystem()
        self.adapter = LegacyPaymentAdapter(self.new_system)

    def test_adapter_implements_target_interface(self):
        """Testa se o Adapter herda corretamente da interface Legada (Target)."""
        self.assertIsInstance(self.adapter, LegacyPaymentProcessor)
        
    def test_successful_payment_translation(self):
        """
        Testa se a chamada legada é traduzida para o formato do Novo Sistema 
        e retorna uma mensagem de sucesso.
        """
        order_id = "ORDER-123"
        amount = 50.00
        
        # A chamada é feita usando o método legado (Target)
        result = self.adapter.process_legacy_payment(order_id, amount)
        
        # Verifica se a mensagem de sucesso do novo sistema foi retornada
        self.assertIn("Pagamento moderno processado", result)
        self.assertIn("Sucesso!", result)
        
    def test_failed_payment_translation(self):
        """
        Testa se o Adapter consegue traduzir uma falha (ex: valor zero) 
        do sistema legado para o novo sistema e retorna a mensagem de falha.
        """
        order_id = "ORDER-456"
        amount = 0.00 # Um valor inválido/falho, dependendo da nossa lógica simples
        
        result = self.adapter.process_legacy_payment(order_id, amount)
        
        self.assertIn("Falha!", result)
        self.assertIn("Dados de pagamento inválidos", result)


class PaymentApiIntegrationTests(TestCase):
    """
    Testes de integração para o endpoint REST que utiliza o Adapter (o Cliente).
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('process_payment') # Mapeado para /api/pay/

    def test_api_success(self):
        """Testa o processamento de pagamento bem-sucedido via API (Cliente)."""
        data = {
            'order_id': 'API-ORDER-001', 
            'amount': 99.50
        }
        response = self.client.post(self.url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sucesso!', response.json()['message'])
        
    def test_api_invalid_data(self):
        """Testa se a API retorna 400 para dados faltantes."""
        data = {
            'order_id': 'API-ORDER-002', 
            # 'amount' está faltando
        }
        response = self.client.post(self.url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('são obrigatórios', response.json()['error'])
