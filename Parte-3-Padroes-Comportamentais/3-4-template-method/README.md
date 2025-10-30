# APSI – Parte 3: Padrão Comportamental – Template Method
Equipe: [coloque o nome da equipe / integrantes aqui]
Link do GitHub Classroom: [coloque aqui o link do repositório no classroom]

## Descrição do Problema
O sistema precisa processar pagamentos de diferentes métodos (cartão de crédito, PayPal, transferência bancária),
cada um com etapas específicas, mas seguindo um mesmo fluxo geral: validação, processamento e notificação.

## Solução Implementada
Foi utilizado o padrão Template Method. A classe abstrata `PaymentProcessor` define o template method `process_payment(info)`,
com as etapas: `validate(info)`, `execute(info)` e `notify(info, result)`. As subclasses concretas implementam as etapas específicas.

## Classes
- `PaymentProcessor` (abstrata)
- `CreditCardProcessor`
- `PayPalProcessor`
- `BankTransferProcessor`

## Fluxo Geral
1. Validação dos dados
2. Execução do pagamento
3. Notificação

## Exemplo de API
`POST /api/template/process`
```json
{
  "method": "credit",
  "info": {"card_number": "1234567812345678", "amount": 150.0}
}
```

Resposta:
```json
{"status": "success", "method": "credit_card", "amount": 150.0}
```

## Benefícios
- Estrutura fixa com etapas flexíveis por método.
- Reaproveitamento de código e padronização do fluxo.
- Facilidade para adicionar novos tipos de pagamento.

## Como executar
1. Criar e ativar ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
2. Instalar dependências (Django e DRF estão no projeto):
```bash
pip install Django>=5.0 djangorestframework>=3.15
```
3. Migrar e subir o servidor:
```bash
cd apsi-template
python manage.py migrate
python manage.py runserver
```
4. Testar o endpoint:
```bash
curl -X POST http://localhost:8000/api/template/process   -H "Content-Type: application/json"   -d '{"method":"credit","info":{"card_number":"1234567812345678","amount":150.0}}'
```

## Testes
Executar com:
```bash
pytest -v
```
