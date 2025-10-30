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


#  APSI – Parte 2.1: Padrão Estrutural – Adapter (Integração de Pagamento Legado)

Equipe: [coloque o nome da equipe / integrantes aqui]
Link do GitHub Classroom: [coloque aqui o link do repositório no classroom]

---

## Descrição do Problema

O sistema de e-commerce moderno precisa processar pagamentos seguindo uma nova interface padrão, chamada `NewPaymentGateway`. No entanto, a infraestrutura da empresa depende de um **sistema de processamento de pagamentos legado (`LegacyPaymentProcessor`)** que é incompatível com a nova interface (diferentes nomes de métodos e formato de dados) e que **não pode ser modificado**.

O desafio é fazer com que o código moderno use o sistema legado **sem alterar as classes existentes**, implementando o novo padrão no Django.

## Solução Implementada

A solução foi desenvolvida em Python e Django, aplicando o padrão **Adapter** para criar uma camada intermediária que faz a tradução bidirecional entre a interface nova (Alvo) e a classe antiga (Adaptee).

### Estrutura Aplicada

| Papel | Implementação | Observação |
| :--- | :--- | :--- |
| **Alvo (Target)** | `NewPaymentGateway` (Interface/Contrato) | É o contrato que o Cliente espera usar. |
| **Adaptee (Legado)** | `LegacyPaymentProcessor` (O sistema antigo) | Não deve ser modificado. |
| **Adapter (Adaptador)** | `LegacyPaymentAdapter` | Classe que implementa o **Alvo** e contém uma instância do **Adaptee**, traduzindo as chamadas. |
| **Cliente** | `PaymentView` (View do Django) | Interage apenas com o Alvo (o `LegacyPaymentAdapter`). |
| **API REST** | `/api/pay/` (POST) | Endpoint para processar a requisição de pagamento via Adapter. |

### Instruções para Execução

1.  Navegar para a pasta do projeto e ativar o ambiente virtual:
    ```bash
    cd 2-1-adapter-payment
    .\venv_adapter\Scripts\activate
    ```

2.  Migrar o banco de dados (se necessário) e rodar o servidor:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

3.  Execução dos Testes Unitários:
    ```bash
    python manage.py test payment_app
    ```

## Testes via API (Exemplo cURL)

Para testar o processamento de um pagamento (POST), que será manipulado internamente pelo Adapter:

```bash
curl -X POST [http://127.0.0.1:8000/api/pay/](http://127.0.0.1:8000/api/pay/) \
-H "Content-Type: application/json" \
-d '{"amount": 150.75, "card_number": "4111...", "expiry": "12/25"}'
