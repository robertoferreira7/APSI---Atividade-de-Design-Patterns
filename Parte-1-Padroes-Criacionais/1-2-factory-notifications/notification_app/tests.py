# notification_app/tests.py

from .services.notification_factory import notification_factory # <-- VERIFIQUE SE ESTA LINHA EXISTE

from django.test import TestCase, Client
from django.urls import reverse

# O restante do código de importação deve estar assim:
from .services.notification_service import (
    EmailNotificationService,
    SmsNotificationService,
    PushNotificationService
)

# ... (restante do seu código de teste)