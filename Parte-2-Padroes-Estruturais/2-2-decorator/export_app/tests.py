# 2-2-decorator-export/export_app/tests.py

from django.test import TestCase, Client
from django.urls import reverse
import base64

# Importa as classes do Decorator
from .services.export_services import (
    JsonExporter,
    XmlExporter,
    CompressionDecorator,
    EncryptionDecorator
)

# Dados de exemplo para os testes
TEST_DATA = {"user_id": 101, "status": "active"}

class DecoratorPatternTests(TestCase):
    """
    Testes unitários para validar a lógica de composição do Decorator.
    """
    
    def test_json_export_base(self):
        """Testa se o componente base (JsonExporter) funciona corretamente."""
        exporter = JsonExporter()
        result = exporter.export(TEST_DATA)
        self.assertIn("JSON DATA", result)
        self.assertIn("user_id", result)

    def test_xml_export_base(self):
        """Testa se o componente base (XmlExporter) funciona corretamente."""
        exporter = XmlExporter()
        result = exporter.export(TEST_DATA)
        self.assertIn("XML DATA", result)
        self.assertIn("<root>", result)
        
    def test_single_decorator_encryption(self):
        """Testa se a Criptografia é aplicada a um exportador JSON."""
        json_exporter = JsonExporter()
        encrypted_exporter = EncryptionDecorator(json_exporter)
        
        result = encrypted_exporter.export(TEST_DATA)
        self.assertIn("ENCRYPTED(", result)
        
        # Garante que o resultado base foi criptografado (e não está visível)
        self.assertNotIn("JSON DATA", result) 
        
    def test_multiple_decorators_chain(self):
        """
        Testa a cadeia de decorators: JSON -> Compressão -> Criptografia.
        As transformações devem ser aplicadas em ordem (inner-to-outer).
        """
        # Componente Base
        base_exporter = JsonExporter()
        
        # 1. Envolve com Compressão
        compressed_exporter = CompressionDecorator(base_exporter)
        
        # 2. Envolve com Criptografia (o EncryptionDecorator está no topo)
        final_exporter = EncryptionDecorator(compressed_exporter)
        
        result = final_exporter.export(TEST_DATA)
        
        # Verifica se o último decorador (Encryption) é o wrapper mais externo
        self.assertIn("ENCRYPTED(", result) 
        
        # Verifica se a compressão ocorreu antes da criptografia (o conteúdo interno é compactado)
        inner_content = result.split('(')[-1].strip(')')
        # Se a criptografia foi aplicada sobre a compressão, o Base64 deve ser válido
        # E o resultado final não deve conter o conteúdo JSON ou COMPRESSED (texto claro)
        self.assertNotIn("JSON DATA", result)
        self.assertNotIn("COMPRESSED", result)


class ExportApiIntegrationTests(TestCase):
    """
    Testes de integração para o endpoint REST que utiliza a cadeia de Decorators (o Cliente).
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('export_data') # Mapeado para /api/export/

    def test_api_json_only(self):
        """Testa a exportação JSON básica via API."""
        data = {
            'format': 'json',
            'content': {"name": "TestUser"}
        }
        response = self.client.post(self.url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('JSON DATA', response.json()['exported_data'])
        self.assertEqual(response.json()['decorators_applied'], [])

    def test_api_complex_chain(self):
        """Testa a exportação com XML, Criptografia e Compressão via API."""
        data = {
            'format': 'xml',
            # CORREÇÃO: Inverter a ordem. A Compressão deve vir antes da Criptografia.
            'decorators': ['compression', 'encryption'], 
            'content': {"name": "ProductX", "price": 10.99}
        }
        response = self.client.post(self.url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        exported_data = response.json()['exported_data']
        
        # Verifica se a Criptografia (o último aplicado na View) está no topo da saída
        self.assertIn('ENCRYPTED', exported_data)
        
        # Verifica se os dois decoradores foram aplicados
        self.assertEqual(set(response.json()['decorators_applied']), {'encryption', 'compression'})