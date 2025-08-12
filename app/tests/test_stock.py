from asyncio import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.tests import reset_db

client = TestClient(app)

class TestStockCRUD:
    @classmethod
    def setup_class(cls):
        """
        Configuración inicial para la clase de pruebas.
        Se ejecuta una vez antes de todos los tests de la clase.
        Limpia la tabla de familias en la base de datos.
        """
        cls.db = SessionLocal()
        try:
            reset_db(cls.db)
            sleep(1)  # Esperar un segundo para asegurar que la base de datos esté limpia
        finally:
            cls.db.close()
        pass
        
    def setup_method(self, method):
        """
        Configuración antes de cada método de prueba.
        """
        self.db = SessionLocal()

    def teardown_method(self, method):
        """
        Limpieza después de cada método de prueba.
        """     
        self.db.close()

    @classmethod
    def teardown_class(cls):
        """
        Limpieza final para la clase de pruebas.
        Se ejecuta una vez después de todos los tests de la clase.
        """
        cls.db = SessionLocal()
        reset_db(cls.db)
        cls.db.close()

    
    def test_listar_stock(self):
        res = client.get("/stock/")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_listar_stock_bajo(self):
        res = client.get("/stock/", params={"bajo_stock": True})
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_listar_movimientos(self):
        res = client.get("/stock/movimiento/")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_obtener_stock_por_componente(self):
        # Primero, creamos un componente y su stock
        comp = client.post("/componente/", json={"nombre": "CompTest"}).json()
        # Usar el endpoint de movimiento para crear stock
        stock = client.post("/stock/movimiento", json={"tipo": "entrada", "cantidad": 10, "id_componente": comp["id"]}).json()
        res = client.get(f"/stock/componente/{comp['id']}")
        assert res.status_code == 200
        assert res.json()["id"] == stock["id"]
        assert res.json()["cantidad"] == 10

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

    def test_eliminar_movimiento(self):
        prod = client.post("/articulo/", json={"nombre": "ProdStock3", "tipo": "simple"}).json()
        mov = client.post("/stock/movimiento", json={"tipo": "entrada", "cantidad": 5, "id_producto_simple": prod["id"]})
        assert mov.status_code == 201
        stock_id = mov.json()["id"]
        res = client.delete(f"/stock/movimiento/{stock_id}")
        assert res.status_code == 200
        # Verificar que el stock existe pero ya no hay cantidad
        res = client.get(f"/stock/producto_simple/{prod['id']}")
        assert res.status_code == 200
        assert res.json()["cantidad"] == 0
        