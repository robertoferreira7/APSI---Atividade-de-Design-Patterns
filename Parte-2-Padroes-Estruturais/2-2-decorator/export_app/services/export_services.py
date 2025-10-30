# export_app/services/export_services.py

from abc import ABC, abstractmethod
import base64
import zlib

# --- 1. COMPONENT (INTERFACE BASE) ---
class DataExporter(ABC):
    """Interface Componente Base para todos os exportadores e decoradores."""
    @abstractmethod
    def export(self, data: dict) -> str:
        pass


# --- 2. CONCRETE COMPONENTS (EXPORTADORES BASE) ---

class JsonExporter(DataExporter):
    """Exportador Concreto: Exporta dados em formato JSON (simulado)."""
    def export(self, data: dict) -> str:
        return f"JSON DATA: {data}"

class XmlExporter(DataExporter):
    """Exportador Concreto: Exporta dados em formato XML (simulado)."""
    def export(self, data: dict) -> str:
        # Simulação simples de conversão para XML
        xml_content = "".join([f"<{k}>{v}</{k}>" for k, v in data.items()])
        return f"XML DATA: <root>{xml_content}</root>"

# Adicionar mais exportadores se necessário (ex: CSVExporter)


# --- 3. BASE DECORATOR (DECORADOR ABSTRATO) ---
class DataExporterDecorator(DataExporter, ABC):
    """
    Classe Base para todos os Decoradores.
    Mantém uma referência ao objeto DataExporter e delega o trabalho a ele.
    """
    def __init__(self, wrapped: DataExporter):
        self._wrapped = wrapped

    def export(self, data: dict) -> str:
        # Delega a responsabilidade ao componente embrulhado
        return self._wrapped.export(data)


# --- 4. CONCRETE DECORATORS (DECORADORES CONCRETOS) ---

class CompressionDecorator(DataExporterDecorator):
    """Adiciona compressão (simulada) aos dados exportados."""
    def export(self, data: dict) -> str:
        # 1. Obtém o resultado do componente interno (Exportador ou outro Decorador)
        exported_data = super().export(data)
        
        # 2. Adiciona a nova responsabilidade (Compressão)
        compressed_bytes = zlib.compress(exported_data.encode('utf-8'))
        compressed_data = base64.b64encode(compressed_bytes).decode('utf-8')
        
        return f"COMPRESSED({compressed_data})"

class EncryptionDecorator(DataExporterDecorator):
    """Adiciona criptografia (simulada) aos dados exportados."""
    def export(self, data: dict) -> str:
        # 1. Obtém o resultado do componente interno
        exported_data = super().export(data)
        
        # 2. Adiciona a nova responsabilidade (Criptografia)
        # Simulação: Criptografa o resultado com Base64 para demonstração
        encrypted_data = base64.b64encode(exported_data.encode('utf-8')).decode('utf-8')
        
        return f"ENCRYPTED({encrypted_data})"

# Dicionário de Factories para a View usar (para fácil lookup)
EXPORTERS = {
    'json': JsonExporter,
    'xml': XmlExporter,
}

DECORATORS = {
    'compression': CompressionDecorator,
    'encryption': EncryptionDecorator,
}