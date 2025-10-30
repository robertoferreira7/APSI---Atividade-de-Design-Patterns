# APSI – Parte 2.3: Padrão Estrutural – Facade (Processamento de Pedidos)

---

## Exercício — Descrição

### Descrição

O sistema possui múltiplos microsserviços para funcionalidades de e-commerce (clientes, produtos, pedidos, pagamentos). O objetivo é implementar uma interface simples e unificada para que clientes externos possam realizar uma operação complexa, como fazer um pedido.

### Padrão Aplicado

**Facade**.

O padrão Facade foi aplicado na classe `OrderFacade`, que fornece o método `placeOrder()` simplificado. Esta classe orquestra as chamadas sequenciais e complexas aos subsistemas (busca de cliente, verificação de estoque, reserva, processamento de pagamento e criação de pedido), isolando o Cliente da complexidade interna.

### Estrutura do Exercício

* **Serviços / classes**:
    * **Subsistemas (simulados)**: `CustomerService`, `InventoryService`, `PaymentService`, `OrderService`.
    * **Facade**: `OrderFacade`.
* **Endpoints (se aplicável)**:
    * `/api/order/place/` (POST): Endpoint que atua como **Cliente**, chamando apenas o método `place_order` da Facade.
* **Testes unitários**:
    * 7 testes no `order_app/tests.py` validam que a Facade orquestra o fluxo corretamente e interrompe a operação em caso de falhas em qualquer subsistema (ex: cliente não encontrado ou estoque insuficiente).

### Como Rodar

Navegue para a pasta do exercício e ative o ambiente virtual:
```bash
cd Parte-2-Padroes-Estruturais/2-3-facade-ecommerce
.\venv_facade\Scripts\activate
