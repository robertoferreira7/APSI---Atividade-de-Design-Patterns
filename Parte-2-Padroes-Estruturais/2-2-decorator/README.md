# APSI – Parte 2.2: Padrão Estrutural – Decorator (Exportação Dinâmica)

---

## Exercício — Descrição

### Descrição

O sistema de exportação de dados requer suporte a múltiplos formatos (JSON, XML) e a aplicação dinâmica de transformações (compressão e criptografia).

### Padrão Aplicado

**Decorator**.

Este padrão permite envolver um componente base (`JsonExporter` ou `XmlExporter`) com um ou mais decoradores (`CompressionDecorator`, `EncryptionDecorator`). Isso adiciona responsabilidades de forma transparente e flexível em tempo de execução, sem modificar o componente base.

### Estrutura do Exercício

* **Serviços / classes**:
    * **Componente**: Interface `DataExporter`.
    * **Componentes Concretos**: `JsonExporter`, `XmlExporter`.
    * **Decorator Base**: `DataExporterDecorator`.
    * **Decoradores Concretos**: `CompressionDecorator`, `EncryptionDecorator`.
* **Endpoints (se aplicável)**:
    * `/api/export/` (POST): Endpoint que atua como **Cliente**, lendo os parâmetros e montando a cadeia de exportação dinamicamente.
* **Testes unitários**:
    * 6 testes no `export_app/tests.py` validam a composição da cadeia, garantindo que os decoradores são aplicados na ordem correta (inner-to-outer).

### Como Rodar

Navegue para a pasta do exercício e ative o ambiente virtual:
```bash
cd Parte-2-Padroes-Estruturais/2-2-decorator-export
.\venv_decorator\Scripts\activate
