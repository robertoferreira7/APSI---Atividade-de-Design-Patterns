# APSI – Parte 2.1: Padrão Estrutural – Adapter (Integração de Pagamento Legado)

## Descrição
O sistema está em migração, e precisa que o novo sistema de pagamento (`NewPaymentSystem`) seja acessível pelo código legado, que espera uma interface antiga (`LegacyPaymentProcessor`).

## Padrão Aplicado

**Adapter**.

O Adapter é aplicado para criar uma **camada de tradução** (`LegacyPaymentAdapter`) que converte os métodos e parâmetros da interface legada (Target) para o formato exigido pelo novo sistema (Adaptee).

## Estrutura do Exercício
- Serviços / classes: 
   * **Alvo (Target)**: Interface `LegacyPaymentProcessor`.
    * **Adaptee (Incompatível)**: Classe `NewPaymentSystem`.
    * **Adapter**: Classe `LegacyPaymentAdapter` que implementa o Alvo e traduz a chamada para o Adaptee.
- Endepoints: * `/api/pay/` (POST): Endpoint que atua como **Cliente**, chamando o Adapter através da interface Legada.
- Testes unitários: * 5 testes no `payment_app/tests.py` validam a implementação da interface e a correta tradução das chamadas de sucesso e falha.

  
## Como Rodar

Navegue para a pasta do exercício e ative o ambiente virtual:
```bash
cd Parte-2-Padroes-Estruturais/2-1-adapter-payment
.\venv_adapter\Scripts\activate

Executar testes:

Comando: python manage.py test payment_app
Resultado esperado: Ran 5 tests in 0.xxxs - OK

