from asyncio import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.services import get_ColorService
from app.tests import reset_db

client = TestClient(app)

class TestColorCRUD:

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

    
    def test_listar_colores(self):
        res = client.get("/color/")
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        colores_service = get_ColorService()(self.db)
        assert len(res.json()) == colores_service.contar()
    
    def test_crear_color(self):
        fam = client.post("/familia/", json={"nombre": "FamColor"}).json()
        data = {"nombre": "Rojo", "hex": "#FF0000", "id_familia": fam["id"]}
        res = client.post("/color/", json=data)
        assert res.status_code == 201
        color = res.json()
        assert color["nombre"] == "Rojo"
        assert color["id_familia"] == fam["id"]

    def test_obtener_color_por_id(self):
        fam = client.post("/familia/", json={"nombre": "FamColor2"}).json()
        color = client.post("/color/", json={"nombre": "Azul", "id_familia": fam["id"]}).json()
        color_id = color["id"]
        res = client.get(f"/color/{color_id}")
        assert res.status_code == 200
        assert res.json()["id"] == color_id

    def test_actualizar_color(self):
        fam = client.post("/familia/", json={"nombre": "FamColor3"}).json()
        color = client.post("/color/", json={"nombre": "Verde", "id_familia": fam["id"]}).json()
        color_id = color["id"]
        res = client.put(f"/color/{color_id}", json={"nombre": "VerdeOscuro"})
        assert res.status_code == 200
        assert res.json()["nombre"] == "VerdeOscuro"

    def test_eliminar_color(self):
        fam = client.post("/familia/", json={"nombre": "FamColor4"}).json()
        color = client.post("/color/", json={"nombre": "Amarillo", "id_familia": fam["id"]}).json()
        color_id = color["id"]
        res = client.delete(f"/color/{color_id}")
        assert res.status_code == 200
        res = client.get(f"/color/{color_id}")
        assert res.status_code == 404
