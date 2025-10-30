
## Descrição do Problema

Um sistema de **monitoramento de mercado financeiro** deve permitir que usuários se inscrevam para receber **alertas sobre mudanças no preço de ações** específicas.  
Quando uma ação muda de valor, todos os observadores interessados precisam ser notificados automaticamente.

O desafio é criar um backend capaz de:
- Gerenciar inscrições de observadores (por tipo e símbolo da ação);
- Emitir eventos de mudança de preço;
- Notificar os observadores corretos.

---

## Solução Implementada

A solução foi construída em **Django 5 + Django REST Framework**, utilizando **Django Signals** para implementar o padrão **Observer**.

### Fluxo geral:

1. O usuário inscreve um observador (ex.: SMS, Email, Dashboard) para um determinado símbolo (ex.: `PETR4`).  
2. O `StockMarket` (Subject) atualiza o preço e emite o sinal `price_changed`.  
3. O receiver (`_dispatch_to_observers`) recebe o evento e notifica todos os observadores registrados para aquele símbolo.  
4. O usuário pode se descadastrar ou alterar a lista de observadores via API.

---

## Padrão Aplicado: Observer

### Definição
O padrão **Observer** permite que múltiplos objetos (observadores) sejam notificados automaticamente sempre que o estado de outro objeto (o sujeito) muda.

### Aplicação no Projeto
| Elemento | Implementação |
|-----------|----------------|
| **Subject (Observable)** | `StockMarket` em `services.py` |
| **Observers** | `SMSObserver`, `EmailObserver`, `DashboardObserver` |
| **Sistema de Eventos** | `price_changed` definido em `signals.py` |
| **Registro de inscrições** | Dicionário `_registry` em `signals.py` |
| **Mecanismo de notificação** | Função `_dispatch_to_observers` decorada com `@receiver` |

**Por que usar Django Signals?**  
Os *signals* do Django funcionam como um sistema de “eventos e ouvintes” nativo do framework, simplificando a implementação do Observer sem precisar criar infraestrutura manual de listeners.

---

## Instruções para Executar o Projeto

### Clonar e preparar o ambiente
```bash
git clone <link-do-seu-repositorio>
cd apsi-observer
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
```

### Instalar dependências
```bash
pip install -e .[dev]
```

### Migrar e iniciar o servidor
```bash
python manage.py migrate
python manage.py runserver
```

### Testar os endpoints

#### Inscrever observador
```bash
curl -X POST http://localhost:8000/api/observer/subscribe   -H "Content-Type: application/json"   -d '{"symbol":"PETR4","type":"sms"}'
```

#### Atualizar preço
```bash
curl -X POST http://localhost:8000/api/observer/price   -H "Content-Type: application/json"   -d '{"symbol":"PETR4","price":39.7}'
```

#### Remover observador
```bash
curl -X POST http://localhost:8000/api/observer/unsubscribe   -H "Content-Type: application/json"   -d '{"symbol":"PETR4","type":"sms"}'
```

---

## Testes Unitários

Os testes estão em `observer/tests.py` e usam `pytest-django` com `APIClient`.

```python
@pytest.mark.django_db
class TestObserverSignals:
    def test_subscribe_price_unsubscribe(self):
        c = APIClient()
        assert c.post("/api/observer/subscribe", {"symbol": "PETR4", "type": "dash"}, format="json").status_code == 200
        assert c.post("/api/observer/price", {"symbol": "PETR4", "price": 39.7}, format="json").status_code == 200
        assert c.post("/api/observer/unsubscribe", {"symbol": "PETR4", "type": "dash"}, format="json").status_code == 200
```

### Como rodar os testes
```bash
pytest -v --maxfail=1 --disable-warnings
```
## Conclusão

O projeto demonstra o uso do padrão **Observer** dentro do ecossistema Django de forma simples e funcional. 

