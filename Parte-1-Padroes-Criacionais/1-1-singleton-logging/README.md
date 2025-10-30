# ⚙️ APSI – Parte 1.1: Padrão Criacional – Singleton

Equipe: [coloque o nome da equipe / integrantes aqui]
Link do GitHub Classroom: [coloque aqui o link do repositório no classroom]

## Descrição do Problema

A aplicação necessita de um serviço centralizado para o registro de eventos (*logging*). É fundamental garantir que, independentemente de onde o log seja solicitado na aplicação, **apenas uma e única instância** desse serviço de log seja utilizada. Isso previne a criação de múltiplos *arrays* de logs e garante a consistência e o controle de acesso ao histórico.

## Solução Implementada

A solução foi desenvolvida em Django e Python, utilizando o padrão **Singleton** para garantir que a classe `LoggerService` possua apenas uma instância global.

### Estrutura Aplicada

| Papel | Implementação |
|-------|----------------|
| Classe Singleton | `LoggerService` (Gerencia o histórico de logs) |
| Mecanismo de Unicidade | Uso do método `__new__` para controlar a criação de instâncias. |
| Estrutura de Dados | Lista interna (`logs`) com limite de 100 registros. |
| API REST | `/api/log/` (POST) e `/api/logs/` (GET) |

## Instruções para Execução

1.  Clonar o repositório e preparar o ambiente:
    *(Assumindo que você está no diretório raiz do projeto: `Parte-1-Padroes-Criacionais`)*

    ```bash
    cd 1-1-singleton-logging
    .\venv\Scripts\activate
    ```
    *(Caso ainda não tenha instalado o Django: `pip install django`)*

2.  Migrar e rodar o servidor:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Testes via API (Exemplo cURL)

1.  **Registrar um novo log (POST):**
    ```bash
    curl -X POST [http://127.0.0.1:8000/api/log/](http://127.0.0.1:8000/api/log/) \
    -H "Content-Type: application/json" \
    -d '{"level": "INFO", "message": "Inicialização do Serviço"}'
    ```

2.  **Obter o histórico de logs (GET):**
    ```bash
    curl [http://127.0.0.1:8000/api/logs/](http://127.0.0.1:8000/api/logs/)
    ```

## Testes Unitários

O arquivo `logging_app/tests.py` contém todos os testes que validam a unicidade e o comportamento do Singleton.

```python
# Trecho do Teste de Unicidade:
def test_singleton_unicity(self):
    instance1 = LoggerService()
    instance2 = LoggerService()
    # Deve ser a mesma instância na memória
    self.assertIs(instance1, instance2)
