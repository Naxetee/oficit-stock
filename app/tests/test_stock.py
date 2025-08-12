from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestStockCRUD:
    def test_listar_stock(self):
        res = client.get("/stock/")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_movimiento_entrada_y_stock(self):
        prod = client.post("/articulo/", json={"nombre": "ProdStock", "tipo": "simple"}).json()
        mov = client.post("/stock/movimiento", json={"tipo": "entrada", "cantidad": 10, "id_producto_simple": prod['id']})
        # Si la respuesta es error, muestra el detalle para depuración
        if mov.status_code not in (200, 201):
            print("Error detalle:", mov.json())
        assert mov.status_code == 201
        stock = mov.json()
        assert stock is not None and isinstance(stock, dict)
        assert stock["cantidad"] == 10
        res = client.get(f"/stock/producto_simple/{prod['id']}")
        assert res.status_code == 200
        assert res.json()["cantidad"] == 10

    def test_movimiento_salida_stock_insuficiente(self):
        prod = client.post("/articulo/", json={"nombre": "ProdStock2", "tipo": "simple"}).json()
        mov = client.post("/stock/movimiento", json={"tipo": "entrada", "cantidad": 5, "id_producto_simple": prod["id"]})
        assert mov.status_code == 201
        mov2 = client.post("/stock/movimiento", json={"tipo": "salida", "cantidad": 10, "id_producto_simple": prod["id"]})
        # Si la respuesta es error, muestra el detalle para depuración
        if mov2.status_code not in (400, 422):
            print("Error detalle:", mov2.json())
        assert mov2.status_code == 400 or mov2.status_code == 422
