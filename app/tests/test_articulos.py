from time import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.schemas.articuloDTO import ArticuloCreate, ArticuloUpdate
from app.services.articulo_service import ArticuloService
from sqlalchemy import text

from app.tests import reset_db

client = TestClient(app)

class TestEmptyArticulosDB:
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

    
    def test_listar_articulos_vacias(self):
        """
        Test para obtener una lista de familias vacía
        """
        response = client.get("/articulos/")

        if response.status_code == 500:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except Exception:
                print("No se pudo parsear el JSON del error")

        assert response.status_code == 200
        articulos = response.json()
        articulo_service = ArticuloService(self.db)
        assert len(articulos) == articulo_service.contar()

    def test_obtener_articulo_no_existe(self):
        """
        Test para obtener un artículo que no existe
        """
        response = client.get("/articulos/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Artículo no encontrado"}

    def test_crear_articulo(self):
        """
        Test para crear un artículo nuevo
        """
        articulo_data = {
            "nombre": "Artículo de prueba",
            "descripcion": "Descripción del artículo de prueba",
            "codigo": "abxc-123",
            "activo": True,
            "id_familia": None
        }
        
        response = client.post("/articulos/", json=articulo_data)
        assert response.status_code == 201
        articulo = response.json()
        for key in articulo_data:
            assert articulo[key] == articulo_data[key]

    def test_crear_articulo_sin_nombre(self):
        """
        Test para intentar crear un artículo sin nombre
        """
        articulo_data = {
            "nombre": "",
            "descripcion": "Descripción del artículo sin nombre",
            "codigo": "ART-002",
            "activo": True,
            "id_familia": None
        }
        
        response = client.post("/articulos/", json=articulo_data)
        assert response.status_code == 400

    def test_crear_articulo_con_datos_invalidos(self):
        """
        Test para intentar crear un artículo con datos inválidos
        """
        articulo_data = {
            "nombre": 123,
            "descripcion": 123,
            "codigo": False,  
            "activo": "hola",
            "id_familia": "prueba"  
        }
        
        response = client.post("/articulos/", json=articulo_data)
        assert response.status_code == 400

    def test_crear_articulo_con_codigo_existente(self):
        """
        Test para intentar crear un artículo con un código que ya existe
        """
        articulo_data_1 = {
            "nombre": "Artículo 1",
            "descripcion": "Descripción del artículo 1",
            "codigo": "ART-001",  # Código ya existente
            "activo": True,
            "id_familia": None
        }
        
        response = client.post("/articulos/", json=articulo_data_1)        
        assert response.status_code == 201
        
        articulo_data_2 = {
            "nombre": "Artículo 2",
            "descripcion": "Descripción del artículo 2",
            "codigo": "ART-001",  # Código ya existente
            "activo": False,
            "id_familia": None
        }

        response = client.post("/articulos/", json=articulo_data_2)
        assert response.status_code == 400
        
    def test_actualizar_articulo_inexistente(self):
        """
        Test para intentar actualizar un artículo que no existe
        """
        articulo_update_data = {
            "nombre": "Artículo actualizado",
            "descripcion": "Descripción actualizada",
            "codigo": "ART-002",
            "activo": False,
            "id_familia": None
        }
        
        response = client.put("/articulos/9999", json=articulo_update_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "Artículo no encontrado"}

    def test_eliminar_articulo_inexistente(self):
        """
        Test para intentar eliminar un artículo que no existe
        """
        response = client.delete("/articulos/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Artículo no encontrado"}
