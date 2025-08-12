from time import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.services.familia_service import FamiliaService
from sqlalchemy import text

from app.tests import reset_db

client = TestClient(app)

class TestEmptyFamiliaDB:
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

    
    def test_listar_familias_vacias(self):
        """
        Test para obtener una lista de familias vacía
        """
        response = client.get("/familia/")

        assert response.status_code == 200
        familias = response.json()
        familia_service = FamiliaService(self.db)
        assert len(familias) == familia_service.contar()

    def test_obtener_familia_no_existente(self):
        """
        Test para obtener una familia que no existe
        """
        response = client.get("/familia/9999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Familia no encontrada"}

    def test_actualizar_familia_no_existente(self):
        """
        Test para actualizar una familia que no existe
        """
        update_data = {
            "nombre": "Actualizada",
            "descripcion": "Descripción actualizada"
        }
        response = client.put("/familia/9999", json=update_data)

        assert response.status_code == 404

class TestFamiliaCRUD:
    def test_crear_familia(self):
        nueva_familia = {
            "nombre": "Madera",
            "descripcion": "Familia de productos de madera"
        }
        res = client.post("/familia/", json=nueva_familia)
        assert res.status_code == 201
        data = res.json()
        assert data["nombre"] == nueva_familia["nombre"]
        assert data["descripcion"] == nueva_familia["descripcion"]
        self.familia_id = data["id"]

    def test_crear_familia_con_nombre_invalido(self):
        """
        Test para crear una familia con un nombre inválido (vacío)
        """
        nueva_familia = {
            "nombre": "",
            "descripcion": "Familia con nombre vacío"
        }
        res = client.post("/familia/", json=nueva_familia)
        assert res.status_code == 422

    def test_obtener_familia_por_id(self):
        nueva_familia = {
            "nombre": "FamiliaX",
            "descripcion": "Desc X"
        }
        res = client.post("/familia/", json=nueva_familia)
        fam_id = res.json()["id"]
        res = client.get(f"/familia/{fam_id}")
        assert res.status_code == 200
        assert res.json()["id"] == fam_id

    def test_actualizar_familia(self):
        nueva_familia = {
            "nombre": "FamiliaY",
            "descripcion": "Desc Y"
        }
        res = client.post("/familia/", json=nueva_familia)
        fam_id = res.json()["id"]
        update_data = {
            "nombre": "Modificada",
            "descripcion": "Desc Mod"
        }
        res = client.put(f"/familia/{fam_id}", json=update_data)
        assert res.status_code == 200
        assert res.json()["nombre"] == "Modificada"
        assert res.json()["descripcion"] == "Desc Mod"

    def test_eliminar_familia(self):
        nueva_familia = {
            "nombre": "FamiliaZ",
            "descripcion": "Desc Z"
        }
        res = client.post("/familia/", json=nueva_familia)
        fam_id = res.json()["id"]
        res = client.delete(f"/familia/{fam_id}")
        assert res.status_code == 200
        res = client.get(f"/familia/{fam_id}")
        assert res.status_code == 404