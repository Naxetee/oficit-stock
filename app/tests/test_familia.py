from time import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.schemas.familiaDTO import FamiliaCreate
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

    def teardown_class(cls):
        """
        Limpieza final para la clase de pruebas.
        Se ejecuta una vez después de todos los tests de la clase.
        """
        cls.db = SessionLocal()
        reset_db(cls.db)
        cls.db.close()

    
    def test_listar_familias_vacías(self):
        """
        Test para obtener una lista de familias vacía
        """
        response = client.get("/familias/")

        if response.status_code == 500:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except:
                print("No se pudo parsear el JSON del error")

        assert response.status_code == 200
        familias = response.json()
        assert isinstance(familias, list)
        familia_service = FamiliaService(self.db)
        assert len(familias) == familia_service.contar()

    def test_obtener_familia_no_existente(self):
        """
        Test para obtener una familia que no existe
        """
        response = client.get("/familias/9999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Familia no encontrada"}

    def test_crear_familia(self):
        """
        Test para crear una nueva familia 
        """
        nueva_familia = FamiliaCreate(
            nombre="Madera",
            descripcion="Familia de productos de madera"
        )
        
        response = client.post("/familias/", json=nueva_familia.model_dump())

        assert response.status_code == 201
        assert response.json()["nombre"] == nueva_familia.nombre
        assert response.json()["descripcion"] == nueva_familia.descripcion

    def test_crear_familia_invalida(self):
        """
        Test para crear una nueva familia con datos inválidos
        """
        # Enviar datos directamente como diccionario para evitar validación de Pydantic
        datos_invalidos = {
            "nombre": "",  # Nombre vacío
            "descripcion": "Familia de productos de madera"
        }
        
        response = client.post("/familias/", json=datos_invalidos)
        assert response.status_code == 400  # Error de validación de Pydantic
       

    def test_crear_familia_sin_nombre(self):
        """
        Test para crear una familia sin el campo nombre requerido
        """
        datos_sin_nombre = {
            "descripcion": "Familia sin nombre"
            # nombre está ausente
        }
        
        response = client.post("/familias/", json=datos_sin_nombre)
        assert response.status_code == 400
        
    def test_crear_familia_datos_incorrectos(self):
        """
        Test para crear una familia con tipos de datos incorrectos
        """
        datos_incorrectos = {
            "nombre": 123,  # Debería ser string
            "descripcion": True  # Debería ser string o None
        }
        
        response = client.post("/familias/", json=datos_incorrectos)
        assert response.status_code == 400
        
    def test_crear_familia_nombre_muy_largo(self):
        """
        Test para crear una familia con nombre muy largo
        """
        nombre_largo = "x" * 101  # Suponiendo que hay límite de 100 caracteres
        datos_invalidos = {
            "nombre": nombre_largo,
            "descripcion": "Familia de productos metálicos"
            }
        response = client.post("/familias/", json=datos_invalidos)
        assert response.status_code in [400, 422]

    def test_actualizar_familia_no_existente(self):
        """
        Test para intentar actualizar una familia que no existe
        """
        nueva_familia = FamiliaCreate(
            nombre="Metal",
            descripcion="Familia de productos metálicos"
        )
        
        response = client.put("/familias/9999", json=nueva_familia.model_dump())

        assert response.status_code == 404
        assert response.json() == {"detail": "No se encontró familia con ID 9999"}

    def test_actualizar_familia_invalida(self):
        """
        Test para intentar actualizar una familia con datos inválidos
        """
        # Enviar datos directamente como diccionario para evitar validación de Pydantic
        datos_invalidos = {
            "nombre": "",  # Nombre vacío
            "descripcion": "Familia de productos metálicos"
        }
        
        response = client.put("/familias/9999", json=datos_invalidos)
        assert response.status_code == 400

    def test_actualizar_familia_datos_incorrectos(self):
        """
        Test para intentar actualizar una familia con tipos de datos incorrectos
        """
        datos_incorrectos = {
            "nombre": 123,  # Debería ser string
            "descripcion": True  # Debería ser string o None
        }
        
        response = client.put("/familias/9999", json=datos_incorrectos)
        assert response.status_code == 400

    def test_eliminar_familia_no_existente(self):
        """
        Test para intentar eliminar una familia que no existe
        """
        response = client.delete("/familias/9999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Familia no encontrada"}

class TestFamiliaDBWithData:
    @classmethod
    def setup_class(cls):
        """
        Configuración inicial para la clase de pruebas.
        Se ejecuta una vez antes de todos los tests de la clase.
        Crea una familia de ejemplo en la base de datos.
        """
        cls.db = SessionLocal()
        try:
            reset_db(cls.db)
            sleep(1)  # Esperar un segundo para asegurar que la base de datos esté limpia
            familia = {
                "nombre": "Electrónica",
                "descripcion": "Familia de productos electrónicos"
            }
            cls.db.execute(text("INSERT INTO familia (nombre, descripcion) VALUES (:nombre, :descripcion)"), familia)
            cls.db.commit()
        finally:
            cls.db.close()

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

    def teardown_class(cls):
        """
        Limpieza final para la clase de pruebas.
        Se ejecuta una vez después de todos los tests de la clase.
        Elimina todas las familias de la base de datos.
        """
        cls.db = SessionLocal()
        reset_db(cls.db)
        cls.db.close()

    def test_listar_familias_con_datos(self):
        """
        Test para obtener una lista de familias con datos existentes
        """
        response = client.get("/familias/")

        assert response.status_code == 200
        familias = response.json()
        assert isinstance(familias, list)
        assert len(familias) == 1

    def test_obtener_familia_existente(self):
        """
        Test para obtener una familia que existe
        """
       
        response = client.get("/familias/1")

        assert response.status_code == 200
        familia = response.json()
        assert familia["nombre"] == "Electrónica"
        assert familia["descripcion"] == "Familia de productos electrónicos"

    def test_obtener_familia_no_existente(self):
        """
        Test para obtener una familia que no existe
        """
        response = client.get("/familias/9999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Familia no encontrada"}

    def test_crear_familia_existente(self):
        """
        Test para intentar crear una familia que ya existe
        """
        # Comprobar que la familia ya existe en la base de datos antes de intentar crearla
        familia_service = FamiliaService(self.db)
        existe = familia_service.obtener_por_nombre("Electrónica")
        assert existe is not None

        nueva_familia = FamiliaCreate(
            nombre=existe.nombre,
            descripcion=existe.descripcion
        )
        
        response = client.post("/familias/", json=nueva_familia.model_dump())

        assert response.status_code == 400
        r = response.json()
        assert any(s in r['detail'] for s in ['Ya existe', existe.nombre])

    def test_actualizar_familia_inexistente(self):
        """
        Test para intentar actualizar una familia que no existe
        """
        nueva_familia = FamiliaCreate(
            nombre="Electrodomésticos",
            descripcion="Familia de productos electrodomésticos"
        )
        
        response = client.put("/familias/9999", json=nueva_familia.model_dump())

        assert response.status_code == 404
        assert response.json() == {"detail": "No se encontró familia con ID 9999"}

    def test_actualizar_familia_existente(self):
        """
        Test para actualizar una familia existente
        """
        # Primero verificar que la familia existe y obtener sus datos actuales
        response_get = client.get("/familias/1")
        print(f"DEBUG: Familia antes de actualizar: {response_get.json()}")
        assert response_get.status_code == 200
        familia_original = response_get.json()
        
        # Preparar datos para actualización
        datos_actualizacion = {
            "nombre": "Electrodomésticos",
            "descripcion": "Familia de productos electrodomésticos"
        }
        
        print(f"DEBUG: Datos para actualización: {datos_actualizacion}")
        
        # Realizar la actualización
        response = client.put("/familias/1", json=datos_actualizacion)
        
        print(f"DEBUG: Status code: {response.status_code}")
        print(f"DEBUG: Response content: {response.json()}")
        
        assert response.status_code == 200
        familia_actualizada = response.json()
        
        # Verificar que los datos se actualizaron
        assert familia_actualizada["nombre"] == datos_actualizacion["nombre"]
        assert familia_actualizada["descripcion"] == datos_actualizacion["descripcion"]
        
        # Verificar que la actualización persiste
        response_verificacion = client.get("/familias/1")
        familia_verificada = response_verificacion.json()
        print(f"DEBUG: Familia después de actualizar: {familia_verificada}")
        
        assert familia_verificada["nombre"] == datos_actualizacion["nombre"]
        assert familia_verificada["descripcion"] == datos_actualizacion["descripcion"]

    def test_actualizar_familia_invalida(self):
        """
        Test para intentar actualizar una familia con datos inválidos
        """
        # Enviar datos directamente como diccionario para evitar validación de Pydantic
        datos_invalidos = {
            "nombre": "",  # Nombre vacío
            "descripcion": "Familia de productos electrónicos"
        }
        
        response = client.put("/familias/1", json=datos_invalidos)
        assert response.status_code == 400

    def test_actualizar_familia_datos_incorrectos(self):
        """
        Test para intentar actualizar una familia con tipos de datos incorrectos
        """
        datos_incorrectos = {
            "nombre": 123,  # Debería ser string
            "descripcion": True  # Debería ser string o None
        }
        
        response = client.put("/familias/1", json=datos_incorrectos)
        assert response.status_code == 400

    def test_actualizar_familia_nombre_muy_largo(self):
        """
        Test para intentar actualizar una familia con nombre muy largo
        """
        nombre_largo = "x" * 101
        datos_invalidos = {
            "nombre": nombre_largo,  # Suponiendo que hay límite de 100 caracteres
            "descripcion": "Familia de productos electrónicos"
        }
        response = client.put("/familias/1", json=datos_invalidos)
        assert response.status_code in [400, 422]

    def test_actualizar_a_familiar_con_nombre_existente(self):
        """
        Test para intentar actualizar una familia a un nombre que ya existe
        """
        # Primero verificar que la familia con ID 1 existe
        response_get = client.get("/familias/1")
        assert response_get.status_code == 200
        familia_original = response_get.json()

        # Creamos una nueva familia para que exista un nombre duplicado
        nueva_familia = FamiliaCreate(
            nombre="Muebles", 
            descripcion="Muebles y accesorios"
        )

        response_post = client.post("/familias/", json=nueva_familia.model_dump())
        assert response_post.status_code == 201

        # Intentamos actualizar la familia original a un nombre que ya existe
        datos_actualizacion = {
            "nombre": "Muebles",  # Nombre que ya existe
            "descripcion": "Intento de actualizar a un nombre existente"
        }
        
        response = client.put("/familias/1", json=datos_actualizacion)
        
        assert response.status_code == 400
        r = response.json()
        assert any(s in r['detail'] for s in ['Ya existe', familia_original['nombre']])

    def test_eliminar_familia_existente(self):
        """
        Test para eliminar una familia que existe
        """
        response = client.delete("/familias/1")

        assert response.status_code == 200
        assert response.json() == {"detail": "Familia eliminada exitosamente"}

        # Verificar que la familia ya no existe
        response_get = client.get("/familias/1")
        assert response_get.status_code == 404
        assert response_get.json() == {"detail": "Familia no encontrada"}

    def test_eliminar_familia_no_existente(self):
        """
        Test para intentar eliminar una familia que no existe
        """
        response = client.delete("/familias/9999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Familia no encontrada"}