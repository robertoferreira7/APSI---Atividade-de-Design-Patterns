# APSI – Parte 3: Padrão Comportamental – Strategy
Equipe: [coloque o nome da equipe / integrantes aqui]
Link do GitHub Classroom: [coloque aqui o link do repositório no classroom]

## Descrição do Problema

O sistema de pagamento precisa suportar múltiplas estratégias de desconto para diferentes promoções.
Cada tipo de desconto deve ser aplicável de forma independente, permitindo alternar a estratégia em tempo de execução.

## Solução Implementada

A solução foi desenvolvida em Django 5 + Django REST Framework, utilizando o padrão Strategy para permitir a troca dinâmica de algoritmos de desconto.

### Estrutura Aplicada

| Papel | Implementação |
|-------|----------------|
| Interface da estratégia | DiscountStrategy (classe abstrata) |
| Estratégias concretas | PercentageDiscount, FixedDiscount, BuyXGetYDiscount |
| Contexto | PriceService (define e executa a estratégia ativa) |
| API REST | /api/strategy/select e /api/strategy/calculate |

## Instruções para Execução

1. Clonar o repositório e preparar o ambiente:
```bash
git clone <link-do-seu-repositorio>
cd apsi-strategy
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2. Instalar dependências:
```bash
pip install -e .[dev]
```

3. Migrar e rodar o servidor:
```bash
python manage.py migrate
python manage.py runserver
```

## Testes via API

1. Selecionar estratégia de desconto:
```bash
curl -X POST http://localhost:8000/api/strategy/select   -H "Content-Type: application/json"   -d '{"name":"percent","params":{"percent":15}}'
```

2. Calcular o preço final:
```bash
curl -X POST http://localhost:8000/api/strategy/calculate   -H "Content-Type: application/json"   -d '{"amount":200}'
```

Resposta esperada:
```json
{"final_price": 170.0}
```

## Testes Unitários

Arquivo: strategy/tests.py

```python
@pytest.mark.django_db
class TestStrategyAPI:
    def test_select_and_calculate_percent(self):
        c = APIClient()
        r = c.post("/api/strategy/select", {"name": "percent", "params": {"percent": 20}}, format="json")
        assert r.status_code == 200
        r = c.post("/api/strategy/calculate", {"amount": 100}, format="json")
        assert r.data["final_price"] == 80.0
```

Executar testes:
```bash
pytest -v --maxfail=1 --disable-warnings
```

## Justificativa e Benefícios

- Substituição de algoritmos sem alterar o código principal.
- Facilidade de extensão com novas estratégias de desconto.
- Código limpo, modular e aberto para extensão (princípio OCP).

## Conclusão

O padrão Strategy permite alternar facilmente entre diferentes cálculos de desconto sem modificar o serviço principal,
mantendo o sistema flexível e de fácil manutenção.
