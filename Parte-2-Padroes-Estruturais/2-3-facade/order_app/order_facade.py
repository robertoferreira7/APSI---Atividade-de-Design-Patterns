# order_app/services/order_facade.py

from .subsystems.ecommerce_subsystems import (
    CustomerService,
    InventoryService,
    PaymentService,
    OrderService
)

class OrderFacade:
    """
    A Facade fornece uma interface simplificada para um subsistema complexo.
    Orquestra a criação de um pedido, desde a validação até o pagamento.
    """
    def __init__(self):
        # A Facade conhece e gerencia as instâncias dos Subsistemas
        self.customer_service = CustomerService()
        self.inventory_service = InventoryService()
        self.payment_service = PaymentService()
        self.order_service = OrderService()

    def place_order(self, customer_id: str, products: list, total_amount: float) -> dict:
        """
        Método unificado e simplificado para fazer um pedido (a interface esperada pelo Cliente).
        """
        print("\n--- FAÇADE: Iniciando operação placeOrder() ---")
        
        # 1. Validação do Cliente (CustomerService)
        try:
            customer_data = self.customer_service.find_customer(customer_id)
        except ValueError as e:
            return {"success": False, "message": str(e)}

        # 2. Verificação de Estoque e Reserva (InventoryService)
        for item in products:
            product_id = item['id']
            quantity = item['quantity']
            if not self.inventory_service.check_stock(product_id, quantity):
                return {"success": False, "message": f"Estoque insuficiente para Produto {product_id}."}
            self.inventory_service.reserve_stock(product_id, quantity)

        # 3. Processamento do Pagamento (PaymentService)
        try:
            transaction_id = self.payment_service.process_transaction(total_amount, customer_id)
        except ValueError as e:
            return {"success": False, "message": f"Falha no Pagamento: {e}"}

        # 4. Criação do Pedido (OrderService)
        order_id = self.order_service.create_order(customer_id, products, transaction_id)

        print("--- FAÇADE: Pedido processado com sucesso! ---")
        return {
            "success": True,
            "message": f"Pedido {order_id} criado para {customer_data['name']}.",
            "order_id": order_id,
            "transaction_id": transaction_id
        }

# Instância da Facade para ser usada na View (Cliente)
order_facade = OrderFacade()