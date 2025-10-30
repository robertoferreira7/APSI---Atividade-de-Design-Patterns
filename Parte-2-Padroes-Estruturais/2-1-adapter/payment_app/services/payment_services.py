# payment_app/services/payment_services.py

from abc import ABC, abstractmethod

# --- 1. TARGET (ALVO - LEGADO) ---
# Interface que o código existente espera
class LegacyPaymentProcessor(ABC):
    """
    Interface Legada que o código existente espera.
    """
    @abstractmethod
    def process_legacy_payment(self, order_id: str, amount: float) -> str:
        """Processa o pagamento usando a estrutura Legada (Target)."""
        pass


# --- 2. ADAPTEE (INCOMPATÍVEL - NOVO SISTEMA) ---
# O novo sistema que tem uma interface incompatível
class NewPaymentSystem:
    """
    O sistema de pagamento moderno com interface incompatível.
    Não pode ser modificado.
    """
    def execute_payment(self, request_data: dict) -> dict:
        """
        Executa o pagamento usando a nova estrutura (Adaptee).
        """
        if request_data.get('status') == 'valid':
            print(f"NOVO SISTEMA (Adaptee): Executando pagamento de R${request_data['valor']:.2f} para Ordem {request_data['transacao_id']}")
            return {"result": "successful", "message": f"Pagamento moderno processado para {request_data['transacao_id']}"}
        else:
             return {"result": "failed", "message": "Dados de pagamento inválidos no novo sistema."}


# --- 3. ADAPTER (O TRADUTOR) ---
class LegacyPaymentAdapter(LegacyPaymentProcessor):
    """
    Adapter que implementa a interface LEGADA e traduz a chamada para o Novo Sistema (Adaptee).
    """
    def __init__(self, new_system: NewPaymentSystem):
        # O Adaptador mantém uma referência à instância do Adaptee (o novo sistema)
        self._new_system = new_system

    def process_legacy_payment(self, order_id: str, amount: float) -> str:
        """
        Implementa o método Legado e TRADUZ a chamada para o Novo Sistema.
        """
        print(f"ADAPTER: Traduzindo chamada Legada (Ordem: {order_id}, Valor: {amount})")

        # 1. Mapeamento de Parâmetros (A chave do Adapter)
        # Converte os parâmetros posicionais Legados em um dicionário de Request do Novo Sistema
        request_data = {
            "transacao_id": order_id,
            "valor": amount,
            "status": "valid" if amount > 0 else "invalid" # Lógica de validação básica
        }
        
        # 2. Delega a chamada ao Adaptee
        response = self._new_system.execute_payment(request_data)
        
        # 3. Mapeamento de Resposta
        if response['result'] == 'successful':
            return f"Sucesso! {response['message']}"
        else:
            return f"Falha! {response['message']}"

# Instanciamos o Adaptador para que a View (o Cliente) possa usá-lo diretamente
new_system_instance = NewPaymentSystem()
payment_adapter = LegacyPaymentAdapter(new_system_instance)