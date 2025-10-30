#  Parte 2: Padrões Estruturais (Adapter, Decorator, Facade)

## 2.1. Padrão Estrutural – Adapter (Sistema de Pagamento Legado)

### Exercício — Descrição

**Descrição:** A empresa está migrando de um sistema de pagamento legado para uma nova plataforma, mas precisa manter a compatibilidade com o código existente durante a transição.

### Padrão Aplicado

**Adapter**.

O `PaymentAdapter` permite que o código cliente (legado), que espera a interface `LegacyPaymentProcessor`, utilize o novo sistema (`NewPaymentSystem`) que possui uma interface incompatível. O Adapter traduz as chamadas de método e a estrutura de dados (de `orderId` e `amount` para `PaymentRequest`).

### Estrutura do Exercício

* **Pasta:** `2-1-adapter-payment`
* **Serviços / classes**:
    * **Target (Interface Legada):** `LegacyPaymentProcessor`.
    * **Adaptee (Novo Sistema):** `NewPaymentSystem`.
    * **Adapter:** `PaymentAdapter`.
* **Endpoints (se aplicável)**:
    * `/api/payment/legacy/` (POST): Simula a chamada do código legado, que interage unicamente com o Adapter.
* **Testes unitários**:
    * 5 testes no `payment_app/tests.py` validam que o Adapter está traduzindo corretamente as chamadas do formato legado para o novo sistema.

## 2.2. Padrão Estrutural – Decorator (Exportação de Dados Dinâmica)

### Exercício — Descrição

**Descrição:** Desenvolver um serviço de exportação de dados que suporte diferentes formatos (JSON, XML) e que permita adicionar funcionalidades (compressão, criptografia) de forma dinâmica e flexível.

### Padrão Aplicado

**Decorator**.

O padrão Decorator é usado para estender a funcionalidade de um objeto em tempo de execução, sem modificar sua estrutura base. As classes `CompressionDecorator` e `EncryptionDecorator` envolvem (wrap) o componente base (`JsonExporter` ou `XmlExporter`) ou outros decoradores, aplicando transformações sequenciais na exportação de dados.

### Estrutura do Exercício

* **Pasta:** `2-2-decorator-export`
* **Serviços / classes**:
    * **Componente (Interface Base):** `DataExporter`.
    * **Componentes Concretos (Exportadores):** `JsonExporter`, `XmlExporter`.
    * **Decoradores Concretos:** `CompressionDecorator`, `EncryptionDecorator`.
* **Endpoints (se aplicável)**:
    * `/api/export/` (POST): O **Cliente** (View) lê a lista de decoradores na requisição e monta a cadeia de decoração dinamicamente.
* **Testes unitários**:
    * 6 testes no `export_app/tests.py` validam a composição da cadeia, garantindo que os decoradores são aplicados na ordem correta.

## 2.3. Padrão Estrutural – Facade (Processamento de Pedidos em E-commerce)

### Exercício — Descrição

**Descrição:** Simplificar a interação de clientes externos com a complexa arquitetura de microsserviços de um sistema de e-commerce (clientes, inventário, pagamento, pedidos).

### Padrão Aplicado

**Facade**.

A `OrderFacade` atua como um ponto de entrada simplificado, fornecendo o método `place_order` para esconder a complexidade dos subsistemas. A Facade orquestra o fluxo de criação do pedido: 1. Busca de Cliente, 2. Verificação/Reserva de Estoque, 3. Processamento de Pagamento e 4. Criação do Pedido.

### Estrutura do Exercício

* **Pasta:** `2-3-facade-ecommerce`
* **Serviços / classes**:
    * **Subsistemas (Simulados):** `CustomerService`, `InventoryService`, `PaymentService`, `OrderService`.
    * **Facade:** `OrderFacade` (orquestra as chamadas aos subsistemas).
* **Endpoints (se aplicável)**:
    * `/api/order/place/` (POST): O **Cliente** interage unicamente com este endpoint, que chama apenas o método simplificado da Facade.
* **Testes unitários**:
    * 7 testes no `order_app/tests.py` validam o fluxo de orquestração da Facade, incluindo o "caminho feliz" e as interrupções de fluxo devido a falhas nos subsistemas (ex: estoque insuficiente).

---
