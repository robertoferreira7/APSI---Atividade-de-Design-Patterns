import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestObserverSignals:
    def test_subscribe_price_unsubscribe(self):
        c = APIClient()
        assert c.post("/api/observer/subscribe", {"symbol": "PETR4", "type": "dash"}, format="json").status_code == 200
        assert c.post("/api/observer/price", {"symbol": "PETR4", "price": 39.7}, format="json").status_code == 200
        assert c.post("/api/observer/unsubscribe", {"symbol": "PETR4", "type": "dash"}, format="json").status_code == 200
