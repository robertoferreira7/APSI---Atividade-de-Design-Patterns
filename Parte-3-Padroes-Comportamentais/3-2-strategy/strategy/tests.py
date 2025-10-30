import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestStrategyAPI:
    def test_select_and_calculate_percent(self):
        c = APIClient()
        r = c.post("/api/strategy/select", {"name": "percent", "params": {"percent": 20}}, format="json")
        assert r.status_code == 200
        r = c.post("/api/strategy/calculate", {"amount": 100}, format="json")
        assert r.status_code == 200
        assert abs(r.data["final_price"] - 80.0) < 0.001
