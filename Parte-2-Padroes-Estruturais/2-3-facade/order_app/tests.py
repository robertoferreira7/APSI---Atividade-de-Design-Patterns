from django.test import TestCase

# 2-3-facade-ecommerce/order_app/tests.py

from django.test import TestCase, Client
from django.urls import reverse

# Importa as classes do padrão e a instância da Facade
from .services.order_facade import OrderFacade, order_facade
from .services.subsystems.ecommerce_subsystems import (
    CustomerService, 
    InventoryService, 
    PaymentService, 
    OrderService
)

class FacadePatternTests(TestCase):
    """
    Testes unitários para validar a lógica de orquestração da Facade.
    """
    
    def setUp(self):
        # A Facade é o único ponto de entrada para a orquestração
        self.facade = OrderFacade()
        self.valid_customer_id = "C101" # Cliente que existe no subsistema simulado
        self.valid_products = [{"id": "P500", "quantity": 2}] # Produto com estoque
        self.valid_amount = 50.00
        self.invalid_customer_id = "C999"

        # Mocking Básico: Para este teste, vamos garantir que a Facade está usando os subsistemas corretos
        # e verificamos as saídas, mas não é necessário fazer mocks complexos em Django, pois as simulações
        # já estão nas classes dos subsistemas.

    def test_successful_order_placement(self):
        """Testa o caminho feliz: cliente, estoque, pagamento e pedido criados com sucesso."""
        result = self.facade.place_order(
            self.valid_customer_id, 
            self.valid_products, 
            self.valid_amount
        )
        
        # Verifica se o resultado final da Facade é de sucesso
        self.assertTrue(result['success'])
        self.assertIn("Pedido", result['message'])
        self.assertIsNotNone(result['order_id'])
        self.assertIsNotNone(result['transaction_id'])
        
    def test_order_placement_failed_customer_lookup(self):
        """Testa falha quando o cliente não é encontrado (primeira etapa da Facade)."""
        result = self.facade.place_order(
            self.invalid_customer_id, # Cliente Inválido
            self.valid_products, 
            self.valid_amount
        )
        
        # Verifica se o processo foi interrompido na busca do cliente
        self.assertFalse(result['success'])
        self.assertIn("Cliente C999 não encontrado", result['message'])

    def test_order_placement_failed_inventory(self):
        """Testa falha quando o estoque é insuficiente (segunda etapa da Facade)."""
        products_out_of_stock = [{"id": "P500", "quantity": 11}] # Mais de 10 unidades
        
        result = self.facade.place_order(
            self.valid_customer_id, 
            products_out_of_stock, 
            self.valid_amount
        )
        
        # Verifica se o processo foi interrompido na verificação de estoque
        self.assertFalse(result['success'])
        self.assertIn("Estoque insuficiente", result['message'])

    def test_order_placement_failed_payment(self):
        """Testa falha quando o pagamento é negado (terceira etapa da Facade)."""
        invalid_amount = -10.00 # Pagamento que falha na simulação
        
        result = self.facade.place_order(
            self.valid_customer_id, 
            self.valid_products, 
            invalid_amount
        )
        
        # Verifica se o processo foi interrompido no pagamento
        self.assertFalse(result['success'])
        self.assertIn("Pagamento negado", result['message'])


class OrderApiIntegrationTests(TestCase):
    """
    Testes de integração para o endpoint REST que utiliza a Facade (o Cliente).
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('place_order') # Mapeado para /api/order/place/

    def test_api_success(self):
        """Testa a criação de pedido bem-sucedida via API (Cliente)."""
        data = {
            'customer_id': 'C101', 
            'products': [{"id": "P500", "quantity": 1}],
            'total_amount': 25.00
        }
        response = self.client.post(self.url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['success'])
        self.assertIn('criado para Alice', response.json()['message'])
        
    def test_api_failure_on_missing_data(self):
        """Testa se a API retorna 400 para dados faltantes."""
        data = {
            'customer_id': 'C101', 
            'products': [{"id": "P500", "quantity": 1}],
            # 'total_amount' faltando
        }
        response = self.client.post(self.url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('são obrigatórios', response.json()['error'])
        
    def test_api_failure_orchestration(self):
        """Testa se a API propaga uma falha orquestrada pela Facade (ex: cliente inválido)."""
        data = {
            'customer_id': 'C999', # Cliente que falha na Facade
            'products': [{"id": "P500", "quantity": 1}],
            'total_amount': 1.00
        }
        response = self.client.post(self.url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['success'])
        self.assertIn("não encontrado", response.json()['message'])
