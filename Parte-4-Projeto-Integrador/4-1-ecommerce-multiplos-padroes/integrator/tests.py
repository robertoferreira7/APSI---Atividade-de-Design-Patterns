import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestIntegrator:
    def test_full_flow(self):
        c = APIClient()
        # cria produto
        r = c.post("/api/integrator/products/create", {"type":"physical","name":"Mouse","price":100,"stock":3,"weight":0.2}, format="json")
        assert r.status_code == 201
        pid = r.json()["id"]
        # inscreve
        assert c.post("/api/integrator/subscribe", {"productId":pid,"type":"sms"}, format="json").status_code == 200
        # restock
        assert c.post("/api/integrator/products/restock", {"productId":pid,"qty":2}, format="json").status_code == 200
        # price
        r = c.post("/api/integrator/cart/price", {"items":[{"productId":pid,"qty":2}],"discounts":[{"type":"percent","params":{"p":10}}],"shipping":{"type":"byWeight","params":{"weightKg":0.4}}}, format="json")
        assert r.status_code == 200
        # checkout
        r = c.post("/api/integrator/checkout", {
            "items":[{"productId":pid,"qty":2}],
            "discounts":[{"type":"percent","params":{"p":10}}, {"type":"fixed","params":{"v":10}}],
            "shipping":{"type":"byWeight","params":{"weightKg":0.4}},
            "payment":{"method":"credit","info":{"card_number":"1234567812345678"}}
        }, format="json")
        assert r.status_code == 200
        js = r.json()
        assert js["payment"]["status"] in ("success","failed","pending")
        assert "orderId" in js["order"]

