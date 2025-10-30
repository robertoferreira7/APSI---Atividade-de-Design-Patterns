# order_app/services/subsystems/ecommerce_subsystems.py

# Microsserviço Simulador de Cliente
class CustomerService:
    def find_customer(self, customer_id: str) -> dict:
        print(f"CustomerService: Buscando Cliente {customer_id}...")
        if customer_id == "C101":
            return {"id": customer_id, "name": "Alice"}
        raise ValueError(f"Cliente {customer_id} não encontrado.")

# Microsserviço Simulador de Inventário/Produto
class InventoryService:
    def check_stock(self, product_id: str, quantity: int) -> bool:
        print(f"InventoryService: Verificando estoque para Produto {product_id} (Qtde: {quantity})...")
        if product_id == "P500" and quantity <= 10:
            return True
        return False
    
    def reserve_stock(self, product_id: str, quantity: int):
        print(f"InventoryService: Reservando {quantity} unidades do Produto {product_id}.")

# Microsserviço Simulador de Pagamento
class PaymentService:
    def process_transaction(self, amount: float, customer_id: str) -> str:
        print(f"PaymentService: Processando R${amount:.2f} para Cliente {customer_id}...")
        if amount > 0:
            return f"TRANS-{customer_id}-{int(amount)}"
        raise ValueError("Pagamento negado.")

# Microsserviço Simulador de Pedidos
class OrderService:
    def create_order(self, customer_id: str, products: dict, transaction_id: str) -> str:
        print(f"OrderService: Criando pedido para {customer_id}. Transação: {transaction_id}")
        order_id = f"ORDER-{customer_id}-{transaction_id.split('-')[-1]}"
        print(f"OrderService: Pedido {order_id} salvo com sucesso.")
        return order_id