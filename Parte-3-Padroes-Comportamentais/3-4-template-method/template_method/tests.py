import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestTemplateMethodAPI:
    def test_credit_card_payment(self):
        c = APIClient()
        data = {
            "method": "credit",
            "info": {"card_number": "1234567812345678", "amount": 150.0}
        }
        r = c.post("/api/template/process", data, format="json")
        assert r.status_code == 200
        assert r.data["status"] == "success"
        assert r.data["method"] == "credit_card"

    def test_invalid_payment(self):
        c = APIClient()
        data = {"method": "credit", "info": {"amount": 150.0}}  # falta card_number
        r = c.post("/api/template/process", data, format="json")
        assert r.status_code == 200
        assert r.data["status"] == "failed"
