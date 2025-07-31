from time import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.schemas.articuloDTO import ArticuloCreate, ArticuloUpdate
from app.services.articulo_service import ArticuloService
from sqlalchemy import text

from app.services.familia_service import FamiliaService
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
        Test para obtener un Articulo que no existe
        """
        response = client.get("/articulos/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Articulo no encontrado"}

    def test_crear_articulo(self):
        """
        Test para crear un Articulo nuevo
        """
        articulo_data = {
            "nombre": "Articulo de prueba",
            "descripcion": "Descripción del Articulo de prueba",
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
        Test para intentar crear un Articulo sin nombre
        """
        articulo_data = {
            "nombre": "",
            "descripcion": "Descripción del Articulo sin nombre",
            "codigo": "ART-002",
            "activo": True,
            "id_familia": None
        }
        
        response = client.post("/articulos/", json=articulo_data)
        assert response.status_code == 400

    def test_crear_articulo_con_datos_invalidos(self):
        """
        Test para intentar crear un Articulo con datos inválidos
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
        Test para intentar crear un Articulo con un código que ya existe
        """
        articulo_data_1 = {
            "nombre": "Articulo 1",
            "descripcion": "Descripción del Articulo 1",
            "codigo": "ART-001",  # Código ya existente
            "activo": True,
            "id_familia": None
        }
        
        response = client.post("/articulos/", json=articulo_data_1)        
        assert response.status_code == 201
        
        articulo_data_2 = {
            "nombre": "Articulo 2",
            "descripcion": "Descripción del Articulo 2",
            "codigo": "ART-001",  # Código ya existente
            "activo": False,
            "id_familia": None
        }

        response = client.post("/articulos/", json=articulo_data_2)
        assert response.status_code == 400
        
    def test_actualizar_articulo_inexistente(self):
        """
        Test para intentar actualizar un Articulo que no existe
        """
        articulo_update_data = {
            "nombre": "Articulo actualizado",
            "descripcion": "Descripción actualizada",
            "codigo": "ART-002",
            "activo": False,
            "id_familia": None
        }
        
        response = client.put("/articulos/9999", json=articulo_update_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "Articulo no encontrado"}

    def test_eliminar_articulo_inexistente(self):
        """
        Test para intentar eliminar un Articulo que no existe
        """
        response = client.delete("/articulos/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Articulo no encontrado"}

class TestArticulosDBWithData:
    @classmethod
    def setup_class(cls):
        """
        Configuración inicial para la clase de pruebas.
        Se ejecuta una vez antes de todos los tests de la clase.
        Limpia la tabla de familias en la base de datos y crea un Articulo de prueba.
        """
        cls.db = SessionLocal()
        try:
            reset_db(cls.db)
            familia_service = FamiliaService(cls.db)
            familia_data = [
                {"nombre": "Familia 1", "descripcion": "Descripción de la familia 1"},
                {"nombre": "Familia 2", "descripcion": "Descripción de la familia 2"}
            ]

            for familia in familia_data:
                cls.db.execute(
                    text("INSERT INTO familia (nombre, descripcion) VALUES (:nombre, :descripcion)"),
                    {"nombre": familia["nombre"], "descripcion": familia["descripcion"]}
                )
            
            articulo_service = ArticuloService(cls.db)
            articulo_data = [{
                "nombre": "Articulo 1",
                "descripcion": "Descripción del Articulo 1",
                "codigo": "ART-001",
                "activo": True,
                "id_familia": 1
            }, {
                "nombre": "Articulo 2",
                "descripcion": "Descripción del Articulo 2",
                "codigo": "ART-002",
                "activo": True,
                "id_familia": 2
            }]
            
            for articulo in articulo_data:
                cls.db.execute(
                    text("INSERT INTO articulo (nombre, descripcion, codigo, activo, id_familia) VALUES (:nombre, :descripcion, :codigo, :activo, :id_familia)"),
                    {
                        "nombre": articulo["nombre"],
                        "descripcion": articulo["descripcion"],
                        "codigo": articulo["codigo"],
                        "activo": articulo["activo"],
                        "id_familia": articulo["id_familia"]
                    }
                )

            cls.db.commit()
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

    def test_listar_articulos_con_datos(self):
        """
        Test para obtener una lista de Articulos con datos existentes
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

    def test_obtener_articulo_existente(self):
        """
        Test para obtener un Articulo existente
        """
        response = client.get("/articulos/1")
        assert response.status_code == 200
        articulo = response.json()
        assert articulo["id"] == 1

    def test_obtener_articulo_no_existente(self):
        """
        Test para intentar obtener un Articulo que no existe
        """
        response = client.get("/articulos/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Articulo no encontrado"}

    def test_crear_articulo_con_datos_validos(self):
        """
        Test para crear un Articulo con datos válidos
        """
        articulo_data = {
            "nombre": "Articulo 3",
            "descripcion": "Descripción del Articulo 3",
            "codigo": "ART-003",
            "activo": True,
            "id_familia": 1
        }
        
        response = client.post("/articulos/", json=articulo_data)
        assert response.status_code == 201
        articulo = response.json()
        for key in articulo_data:
            assert articulo[key] == articulo_data[key]

    def test_crear_articulo_con_codigo_existente(self):
        """
        Test para intentar crear un Articulo con un código que ya existe
        """
        articulo_data = {
            "nombre": "Articulo 4",
            "descripcion": "Descripción del Articulo 4",
            "codigo": "ART-001",  # Código ya existente
            "activo": True,
            "id_familia": 2
        }
        
        response = client.post("/articulos/", json=articulo_data)
        assert response.status_code == 400

    def test_crear_articulo_con_mismo_nombre(self):
        """
        Test para intentar crear un Articulo con el mismo nombre que otro existente
        """
        articulo_data = {
            "nombre": "Articulo 1",  # Nombre ya existente
            "descripcion": "Descripción del Articulo 1 duplicado",
            "codigo": "ART-004",
            "activo": True,
            "id_familia": 1
        }
        
        response = client.post("/articulos/", json=articulo_data)
        assert response.status_code == 400

    def test_actualizar_articulo_existente(self):
        """
        Test para actualizar un Articulo existente
        """
        articulo_update_data = {
            "nombre": "Articulo 1 actualizado",
            "descripcion": "Descripción actualizada del Articulo 1",
            "codigo": "ART-001-UPDATED",
            "activo": False,
            "id_familia": 2
        }
        
        response = client.put("/articulos/1", json=articulo_update_data)
        assert response.status_code == 200
        articulo = response.json()
        for key in articulo_update_data:
            assert articulo[key] == articulo_update_data[key]

    def test_actualizar_articulo_no_existente(self):
        """
        Test para intentar actualizar un Articulo que no existe
        """
        articulo_update_data = {
            "nombre": "Articulo inexistente actualizado",
            "descripcion": "Descripción actualizada del Articulo inexistente",
            "codigo": "ART-9999",
            "activo": True,
            "id_familia": 1
        }
        
        response = client.put("/articulos/9999", json=articulo_update_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "Articulo no encontrado"}

    def test_actualizar_articulo_con_codigo_existente(self):
        """
        Test para intentar actualizar un Articulo con un código que ya existe
        """
        articulo_update_data = {
            "nombre": "Articulo 1 actualizado",
            "descripcion": "Descripción actualizada del Articulo 1",
            "codigo": "ART-002",  # Código ya existente
            "activo": True,
            "id_familia": 1
        }
        
        response = client.put("/articulos/1", json=articulo_update_data)
        assert response.status_code == 400

    def test_actualizar_articulo_con_mismo_nombre(self):
        """
        Test para intentar actualizar un Articulo con el mismo nombre que otro existente
        """
        articulo_update_data = {
            "nombre": "Articulo 1 actualizado",  # Nombre ya existente
            "descripcion": "Descripción del Articulo 1 duplicado",
            "codigo": "ART-005",
            "activo": True,
            "id_familia": 2
        }
        
        response = client.put("/articulos/2", json=articulo_update_data)
        assert response.status_code == 400

    def test_actualizar_articulo_con_datos_invalidos(self):
        """
        Test para intentar actualizar un Articulo con datos inválidos
        """
        articulo_update_data = {
            "nombre": 123,
            "descripcion": 123,
            "codigo": False,  
            "activo": "hola",
            "id_familia": "prueba"  
        }
        
        response = client.put("/articulos/1", json=articulo_update_data)
        assert response.status_code == 400

    def test_actualizar_articulo_con_datos_vacios(self):
        """
        Test para intentar actualizar un Articulo con datos vacíos
        """
        articulo_update_data = {
            "nombre": "",
            "descripcion": "Descripción del Articulo vacío",
            "codigo": "ART-006",
            "activo": True,
            "id_familia": None
        }
        
        response = client.put("/articulos/1", json=articulo_update_data)
        assert response.status_code == 400

    def test_eliminar_articulo_existente(self):
        """
        Test para eliminar un Articulo existente
        """
        response = client.delete("/articulos/1")
        assert response.status_code == 200
        assert response.json() == {"detail": "Articulo eliminado exitosamente"}

    def test_eliminar_articulo_no_existente(self):
        """
        Test para intentar eliminar un Articulo que no existe
        """
        response = client.delete("/articulos/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Articulo no encontrado"}
