# APSI – Parte 4: Projeto Integrador (E-commerce com Múltiplos Padrões)
Equipe: [coloque o nome da equipe / integrantes aqui]
Link do GitHub Classroom: [coloque aqui o link do repositório no classroom]

## Objetivo
Implementar um backend de e-commerce aplicando diversos padrões de projeto:
- Catálogo: Factory + Builder + Observer (notificação de reabastecimento)
- Carrinho: Composite (itens e bundles) + Strategy (frete)
- Pedidos: Chain of Responsibility (validações) + Template Method (pagamentos)
- Descontos: Strategy (regras) + Decorator (combinação de descontos)
- Integrações: Adapter (gateway externo) + Facade (interface simplificada)

## Endpoints
- POST `/api/integrator/products/create` – cria produto (Factory/Builder)
- POST `/api/integrator/subscribe` – inscreve observador de estoque `{productId, type: sms|email|dash}`
- POST `/api/integrator/products/restock` – reabastece e dispara notificação (Observer)
- POST `/api/integrator/cart/price` – calcula total com Composite + descontos (Strategy/Decorator) + frete (Strategy)
- POST `/api/integrator/checkout` – executa pipeline (Chain) e pagamento (Template Method via Facade/Adapter)

## Como executar
1) Ambiente:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
2) Instalar dependências mínimas:
```bash
pip install Django>=5.0 djangorestframework>=3.15 pytest pytest-django
```
3) Rodar:
```bash
cd apsi-integrator
python manage.py migrate
python manage.py runserver
```

## Exemplos
Criar produto físico:
```bash
curl -X POST http://localhost:8000/api/integrator/products/create   -H "Content-Type: application/json"   -d '{"type":"physical","name":"Teclado","price":200,"stock":5,"weight":0.8}'
```

Inscrever observador e reabastecer:
```bash
curl -X POST http://localhost:8000/api/integrator/subscribe   -H "Content-Type: application/json"   -d '{"productId":"<ID>","type":"sms"}'

curl -X POST http://localhost:8000/api/integrator/products/restock   -H "Content-Type: application/json"   -d '{"productId":"<ID>","qty":10}'
```

Calcular preço do carrinho:
```bash
curl -X POST http://localhost:8000/api/integrator/cart/price   -H "Content-Type: application/json"   -d '{"items":[{"productId":"<ID>","qty":2}], "discounts":[{"type":"percent","params":{"p":10}}], "shipping":{"type":"fixed"}}'
```

Checkout (com pagamento cartão):
```bash
curl -X POST http://localhost:8000/api/integrator/checkout   -H "Content-Type: application/json"   -d '{
    "items":[{"productId":"<ID>","qty":2}],
    "discounts":[{"type":"percent","params":{"p":10}}, {"type":"fixed","params":{"v":20}}],
    "shipping":{"type":"byWeight","params":{"weightKg":1.6}},
    "payment":{"method":"credit","info":{"card_number":"1234567812345678","amount":0}}
  }'
```

## Testes
Execute:
```bash
pytest -v
```
