#APSI – Parte 1.2: Padrão Criacional – Factory Method (Sistema de Notificações)

## Descrição do Problema

O sistema de backend precisa enviar notificações através de múltiplos canais (E-mail, SMS, Push). O código de controle (Controller/View) não deve ter que decidir ou saber qual classe de notificação específica deve instanciar. É necessário um mecanismo que delegue a criação do objeto apropriado, mantendo o sistema aberto para novos canais no futuro.

## Solução Implementada

A solução foi desenvolvida em Django, utilizando o padrão **Factory Method** para desacoplar a criação de objetos de notificação do código que os utiliza. A `NotificationFactory` é responsável por retornar o objeto de serviço correto (E-mail, SMS ou Push) com base no tipo solicitado pela API.

### Estrutura Aplicada

| Papel | Implementação |
|-------|----------------|
| Interface do Produto | `NotificationService` (Classe Abstrata com método `send`) |
| Produtos Concretos | `EmailNotificationService`, `SmsNotificationService`, `PushNotificationService` |
| Criador (Factory) | `NotificationFactory` (Implementa o método `get_notification_service`) |
| Cliente | `send_notification` (View do Django que utiliza a Factory) |

## Instruções para Execução

1.  Navegar para a pasta e ativar o ambiente virtual:
    ```bash
    cd 1-2-factory-notifications
    .\venv_fac\Scripts\activate
    ```

2.  Migrar e rodar o servidor:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Testes via API (Exemplo cURL)

Para testar o envio de uma **Notificação por E-mail (POST)**, o Factory Method cria o `EmailNotificationService`:

```bash
curl -X POST [http://127.0.0.1:8000/notify/](http://127.0.0.1:8000/notify/) \
-H "Content-Type: application/json" \
-d '{"type": "email", "recipient": "user@example.com", "subject": "Nova Fatura", "content": "Sua fatura está pronta."}'

## Testes Unitários

Arquivo: notification_app/tests.py

Os testes validam a criação correta de cada objeto pela Factory e a integração da API.

Executar testes:

Bash

python manage.py test notification_app
Resultado esperado:
