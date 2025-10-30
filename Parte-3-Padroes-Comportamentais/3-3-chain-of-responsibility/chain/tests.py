import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestChainAPI:
    def test_order_success(self):
        c = APIClient()
        order = {
            "items_in_stock": True,
            "user_flagged": False,
            "discount": 0.1,
            "items": [
                {"name": "Book", "price": 50, "qty": 2},
                {"name": "Pen", "price": 10, "qty": 3},
            ]
        }
        r = c.post("/api/chain/process", order, format="json")
        assert r.status_code == 200
        assert r.data["status"] == "Success"

    def test_out_of_stock(self):
        c = APIClient()
        order = {"items_in_stock": False, "items": []}
        r = c.post("/api/chain/process", order, format="json")
        assert r.data["status"].startswith("Failed")
