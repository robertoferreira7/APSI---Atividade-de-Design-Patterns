#  APSI – Parte 1: Padrões Criacionais (Singleton e Factory Method)

Este repositório contém as soluções para os Exercícios 1.1 (Singleton) e 1.2 (Factory Method), implementados em Django 5 + Django REST Framework.

---

##  Exercício 1.1 - Padrão Singleton (Serviço de Logging)

### Descrição do Problema

A aplicação necessita de um serviço centralizado para o registro de eventos (*logging*). É fundamental garantir que, independentemente de onde o log seja solicitado, **apenas uma e única instância** desse serviço (`LoggerService`) seja utilizada em toda a aplicação. Isso garante a consistência e o controle de acesso ao histórico de logs.

### Solução Implementada

A solução foi desenvolvida em Django e Python, utilizando o padrão **Singleton** para garantir a unicidade da instância do serviço.

#### Estrutura Aplicada

| Papel | Implementação |
|-------|----------------|
| Classe Singleton | `LoggerService` (Gerencia o histórico de logs em uma lista interna) |
| Mecanismo de Unicidade | Uso do método `__new__` para controlar a criação de instâncias. |
| API REST (Endpoints) | `/api/log/` (POST para registrar) e `/api/logs/` (GET para consultar) |

#### Instruções para Execução

1.  Navegar para a pasta do projeto e ativar o ambiente virtual:
    ```bash
    cd 1-1-singleton-logging
    .\venv\Scripts\activate
    ```
2.  Execução dos Testes Unitários:
    ```bash
    python manage.py test logging_app
    ```
3.  Iniciar o Servidor (para teste manual):
    ```bash
    python manage.py runserver
    ```

#### Teste via API (Exemplo cURL)

Para registrar um log (POST):
```bash
curl -X POST [http://127.0.0.1:8000/api/log/](http://127.0.0.1:8000/api/log/) \
-H "Content-Type: application/json" \
-d '{"level": "INFO", "message": "Log de teste via API"}'


------------------------------------------------------


# APSI – Parte 2.1: Padrão Estrutural – Adapter (Integração de Pagamento Legado)

Equipe: [coloque o nome da equipe / integrantes aqui]
Link do GitHub Classroom: [coloque aqui o link do repositório no classroom]

---

## Descrição do Problema

O sistema de e-commerce moderno precisa processar pagamentos usando uma nova interface padrão (`NewPaymentGateway`). No entanto, o backend da empresa ainda depende de um **sistema de processamento de pagamentos legado (`LegacyPaymentProcessor`)** que não pode ser modificado e que possui métodos e formatos de dados incompatíveis.

O desafio é fazer com que o código moderno use o sistema legado **sem alterar nenhuma das suas classes**.

## Solução Implementada

A solução foi desenvolvida em Django, utilizando o padrão **Adapter** para criar uma camada intermediária que traduz a interface do sistema legado para a interface esperada pelo cliente moderno.

### Estrutura Aplicada

| Papel | Implementação |
| :--- | :--- |
| **Alvo (Target)** | `NewPaymentGateway` (Interface moderna que o cliente espera) |
| **Cliente** | `PaymentView` (O código que processa o pagamento via a interface Alvo) |
| **Adaptee (Incompatível)** | `LegacyPaymentProcessor` (A classe Legada/Incompatível) |
| **Adapter (Adaptador)** | `LegacyPaymentAdapter` (A classe que implementa o Alvo e traduz as chamadas para o Adaptee) |
| **API REST (Endpoint)** | `/api/pay/` (POST para processar o pagamento) |

### Justificativa e Benefícios

* **Reuso de Código Legado:** Permite reutilizar a lógica de um sistema antigo (`LegacyPaymentProcessor`) sem a necessidade de reescrevê-lo, economizando tempo e garantindo a estabilidade.
* **Decoupling:** O Cliente (a View) permanece totalmente desacoplado do sistema legado. Ele interage apenas com a interface padrão (`NewPaymentGateway`).
* **Flexibilidade:** Se o sistema legado for substituído no futuro, basta criar um novo Adaptador ou um novo Gateway, sem modificar o Cliente.

---

## Instruções para Execução

1.  Navegar para a pasta do projeto e ativar o ambiente virtual:
    ```bash
    cd 2-1-adapter-payment
    .\venv_adapter\Scripts\activate
    ```

2.  Execução dos Testes Unitários:
    ```bash
    python manage.py test payment_app
    ```

3.  Iniciar o Servidor (para teste manual):
    ```bash
    python manage.py runserver
    ```

## Testes via API (Exemplo cURL)

Para processar um pagamento (POST) usando o Adapter:

```bash
curl -X POST [http://127.0.0.1:8000/api/pay/](http://127.0.0.1:8000/api/pay/) \
-H "Content-Type: application/json" \
-d '{"amount": 150.75, "card_number": "4111...", "expiry": "12/25"}'
