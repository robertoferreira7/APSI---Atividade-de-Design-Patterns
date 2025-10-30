# APSI – Parte 3: Padrão Comportamental – Chain of Responsibility
Equipe: [coloque o nome da equipe / integrantes aqui]
Link do GitHub Classroom: [coloque aqui o link do repositório no classroom]

## Descrição do Problema
O sistema de e-commerce precisa processar pedidos por meio de várias validações e transformações.
Cada etapa deve poder interromper o processamento caso encontre um problema (ex: fraude, estoque insuficiente).

## Solução Implementada
A solução foi desenvolvida em Django 5 + Django REST Framework utilizando o padrão Chain of Responsibility.
Cada "handler" executa uma etapa específica e passa o pedido adiante.

## Handlers Implementados
- InventoryValidator → verifica se há estoque.
- FraudDetector → checa fraude.
- PricingCalculator → soma preços.
- DiscountApplier → aplica descontos.
- OrderPersister → finaliza e salva o pedido.

## Exemplo de API
POST /api/chain/process  
```json
{
  "items_in_stock": true,
  "user_flagged": false,
  "discount": 0.1,
  "items": [
    {"name": "Book", "price": 50, "qty": 2},
    {"name": "Pen", "price": 10, "qty": 3}
  ]
}
```

### Resposta:
```json
{
  "inventory_ok": true,
  "fraud_check": "Passed",
  "total": 130.0,
  "total_after_discount": 117.0,
  "status": "Success",
  "saved": true
}
```

## Benefícios
- Cada etapa é independente e fácil de adicionar/remover.
- O fluxo é configurável sem alterar a lógica de cada handler.
- Boa aderência ao princípio aberto/fechado (OCP).

## Testes
Executar com:
```bash
pytest -v
```
