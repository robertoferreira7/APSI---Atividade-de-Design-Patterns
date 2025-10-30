# notification_app/services/notification_factory.py

from .notification_service import (
    NotificationService,
    EmailNotificationService,
    SmsNotificationService,
    PushNotificationService
)

class NotificationFactory:
    """
    Implementa o método de fábrica para criar objetos de notificação.
    """
    def get_notification_service(self, notification_type: str) -> NotificationService:
        """Método de fábrica que decide qual classe concreta instanciar."""
        notification_type = notification_type.lower()

        if notification_type == 'email':
            return EmailNotificationService()
        elif notification_type == 'sms':
            return SmsNotificationService()
        elif notification_type == 'push':
            return PushNotificationService()
        else:
            raise ValueError(f"Tipo de notificação '{notification_type}' não suportado.")

notification_factory = NotificationFactory()