# notification_app/services/notification_service.py

from abc import ABC, abstractmethod

# 1. INTERFACE/PRODUTO ABSTRATO
class NotificationService(ABC):
    """Define a interface comum para todos os tipos de notificação."""
    @abstractmethod
    def send(self, recipient: str, content: str, **kwargs) -> str:
        pass

# 2. PRODUTOS CONCRETOS
class EmailNotificationService(NotificationService):
    """Implementa o envio de notificação por E-mail."""
    def send(self, recipient: str, content: str, **kwargs) -> str:
        subject = kwargs.get('subject', 'Assunto Padrão')
        print(f"ENVIANDO E-MAIL para {recipient} - Assunto: {subject} - Conteúdo: {content}")
        return f"E-mail enviado com sucesso para {recipient}."

class SmsNotificationService(NotificationService):
    """Implementa o envio de notificação por SMS."""
    def send(self, recipient: str, content: str, **kwargs) -> str:
        print(f"ENVIANDO SMS para {recipient} - Conteúdo: {content}")
        return f"SMS enviado com sucesso para {recipient}."

class PushNotificationService(NotificationService):
    """Implementa o envio de notificação Push."""
    def send(self, recipient: str, content: str, **kwargs) -> str:
        device_id = kwargs.get('device_id', 'Dispositivo Padrão')
        print(f"ENVIANDO PUSH para {recipient} (ID: {device_id}) - Conteúdo: {content}")
        return f"Push Notification enviada com sucesso para {recipient}."