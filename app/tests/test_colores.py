from time import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.schemas.colorDTO import ColorCreate, ColorUpdate
from sqlalchemy import text

from app.tests import reset_db

client = TestClient(app)

class TestEmptyColorDB:
    @classmethod
    def setup_class(cls):
        """
        Se ejecuta una vez antes de todos los tests de la clase.
        Limpia la base de datos.
        """
        cls.db = SessionLocal()
        try:
            reset_db(cls.db)
            sleep(1)  # Esperar un segundo para asegurar que la base de datos esté limpia
        finally:
            cls.db.close()
            
    def setup_method(self, method):
        """
        Se ejecuta antes de cada test.
        Limpia la tabla de colores en la base de datos.
        """
        self.db = SessionLocal()
        pass

    def teardown_method(self, method):
        """
        Se ejecuta después de cada test.
        Cierra la sesión de base de datos.
        """
        self.db.close()

    @classmethod
    def teardown_class(cls):
        """
        Se ejecuta una vez después de todos los tests de la clase.
        Cierra la sesión de base de datos.
        """
        cls.db = SessionLocal()
        reset_db(cls.db)
        cls.db.close()

    def test_listar_colores_vacíos(self):
        """
        Test para listar colores cuando la base de datos está vacía.
        Debe devolver una lista vacía.
        """
        response = client.get("/colores")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_obtener_color_no_existe(self):
        """
        Test para obtener un color que no existe.
        Debe devolver un error 404.
        """
        response = client.get("/colores/9999")
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Color no encontrado"}

    def test_crear_color(self):
        """
        Test para crear un color.
        Debe devolver el color creado con un ID asignado.
        """
        nuevo_color = ColorCreate(
            nombre="Rojo",
            codigo_hex="#FF0000",
            url_imagen="http://example.com/rojo.png",
            activo=True,
            descripcion="Color rojo brillante",
            id_familia=None  # Asumiendo que no se proporciona familia
        )
        
        response = client.post("/colores", json=nuevo_color.model_dump())
        
        assert response.status_code == 201
        color = response.json()
        nuevo_color = nuevo_color.model_dump()
        for key in nuevo_color.keys():
            assert color[key] == nuevo_color[key]

    def test_crear_color_sin_nombre(self):
        """
        Test para crear un color con un nombre vacío.
        Debe devolver un error 422.
        """
        color_data = {
            "nombre": "",  # Nombre vacío
            "codigo_hex": "#FF0000",
            "url_imagen": "http://example.com/rojo.png",
            "activo": True,
            "descripcion": "Color rojo brillante",
            "id_familia": None
        }
        
        response = client.post("/colores", json=color_data)
        
        assert response.status_code == 400

    def test_crear_color_con_nombre_duplicado(self):
        """
        Test para crear un color con un nombre que ya existe.
        Debe devolver un error 422.
        """
        color_data = ColorCreate(
            nombre="Azul",
            codigo_hex="#0000FF",
            url_imagen="http://example.com/azul.png",
            activo=True,
            descripcion="Color azul brillante",
            id_familia=None
        )
        
        # Crear el primer color
        response = client.post("/colores", json=color_data.model_dump())
        assert response.status_code == 201
        
        # Intentar crear el mismo color de nuevo
        response = client.post("/colores", json=color_data.model_dump())
        
        assert response.status_code == 400

    def test_crear_color_con_codigo_hex_invalido(self):
        """
        Test para crear un color con un código hexadecimal inválido.
        Debe devolver un error 422.
        """
        color_data = {
            "nombre": "Rojo", 
            "codigo_hex": "#x213", # Código hexadecimal inválido
            "url_imagen": "http://example.com/rojo.png",
            "activo": True,
            "descripcion": "Color rojo brillante",
            "id_familia": None
        }
        
        response = client.post("/colores", json=color_data)
        
        assert response.status_code == 400

    def test_crear_color_con_datos_incorrectos(self):
        """
        Test para crear un color con datos incorrectos.
        Debe devolver un error 422.
        """
        color_data = {
            "nombre": 2,
            "codigo_hex": False,
            "url_imagen": True,
            "activo": "abc",
            "descripcion": 1,
            "id_familia": "no_es_un_entero"  # ID de familia no válido
        }
        
        response = client.post("/colores", json=color_data)
        
        assert response.status_code == 400

    def test_actualizar_color_inexistente(self):
        """
        Test para actualizar un color que no existe.
        Debe devolver un error 404.
        """
        color_data = ColorUpdate(
            nombre="Verde",
            codigo_hex="#00FF00",
            url_imagen="http://example.com/verde.png",
            activo=True,
            descripcion="Color verde brillante",
            id_familia=None
        )
        
        response = client.put("/colores/9999", json=color_data.model_dump())
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Color no encontrado"}

    def test_actualizar_color_invalido(self):
        """
        Test para actualizar un color con datos inválidos.
        Debe devolver un error 422.
        """
        # Primero, creamos un color para actualizar
        update_data = {
            "nombre": "",  # Nombre vacío
            "codigo_hex": "#FFFF00",
            "url_imagen": "http://example.com/amarillo.png",
            "activo": True,
            "descripcion": "Color amarillo brillante actualizado",
            "id_familia": None
        }
        
        response = client.put("/colores/9999", json=update_data)
        
        assert response.status_code == 400

    def test_eliminar_color_inexistente(self):
        """
        Test para eliminar un color que no existe.
        Debe devolver un error 404.
        """
        response = client.delete("/colores/9999")
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Color no encontrado"}

class TestColorDBWithData:
    @classmethod
    def setup_class(cls):
        """
        Se ejecuta una vez antes de todos los tests de la clase.
        Limpia la tabla de colores en la base de datos y crea un color inicial.
        """
        cls.db = SessionLocal()
        try:
            reset_db(cls.db)
            sleep(1)  # Esperar un segundo para asegurar que la base de datos esté limpia
            # Crear familias iniciales
            familia_data = [{
                "nombre": "Familia de prueba",
                "descripcion": "Descripción de la familia de prueba"
                }, {
                "nombre": "Familia de prueba 2",
                "descripcion": "Descripción de la familia de prueba 2"
            }]
            color_data = [{
                "nombre": "Verde",
                "codigo_hex": "#00FF00",
                "url_imagen": "http://example.com/verde.png",
                "activo": True,
                "descripcion": "Color verde brillante",
                "id_familia": 1
            }, {
                "nombre": "Azul",
                "codigo_hex": "#0000FF",
                "url_imagen": "http://example.com/azul.png",
                "activo": True,
                "descripcion": "Color azul brillante",
                "id_familia": None
            }]
            # Insertar familias
            for familia in familia_data:
                cls.db.execute(
                    text("INSERT INTO familia (nombre, descripcion) VALUES (:nombre, :descripcion)"),
                    {"nombre": familia["nombre"], "descripcion": familia["descripcion"]}
                )
            # Insertar colores
            for color in color_data:
                cls.db.execute(
                    text("INSERT INTO color (nombre, codigo_hex, url_imagen, activo, descripcion, id_familia) VALUES (:nombre, :codigo_hex, :url_imagen, :activo, :descripcion, :id_familia)"),
                    {
                        "nombre": color["nombre"],
                        "codigo_hex": color["codigo_hex"],
                        "url_imagen": color["url_imagen"],
                        "activo": color["activo"],
                        "descripcion": color["descripcion"],
                        "id_familia": color["id_familia"]
                    }
                )
            cls.db.commit()
            sleep(1)  # Esperar un segundo para asegurar que el color se haya creado
        finally:
            cls.db.close()

    def setup_method(self, method):
        """
        Se ejecuta antes de cada test.
        """
        self.db = SessionLocal()
        pass

    def teardown_method(self, method):
        """
        Se ejecuta después de cada test.
        Cierra la sesión de base de datos.
        """
        self.db.close()

    @classmethod
    def teardown_class(cls):
        """
        Se ejecuta una vez después de todos los tests de la clase.
        Limpia la base de datos.
        """
        cls.db = SessionLocal()
        reset_db(cls.db)
        cls.db.close()

    def test_listar_colores_con_datos(self):
        """
        Test para listar colores cuando hay datos en la base de datos.
        Debe devolver una lista con los colores existentes.
        """
        response = client.get("/colores")

        if response.status_code == 500:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except:
                print("No se pudo parsear el JSON del error")
        
        assert response.status_code == 200
        colores = response.json()
        assert len(colores) == 2

    def test_obtener_color_existente(self):
        """
        Test para obtener un color que existe.
        Debe devolver el color con el ID 1.
        """
        response = client.get("/colores/1")
        
        if response.status_code == 500:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except:
                print("No se pudo parsear el JSON del error")
        
        assert response.status_code == 200
        color = response.json()
        assert color["id"] == 1
        assert color["nombre"] == "Verde"

    def test_obtener_color_no_existente(self):
        """
        Test para obtener un color que no existe.
        Debe devolver un error 404.
        """
        response = client.get("/colores/9999")
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Color no encontrado"}

    def test_crear_color_existente(self):
        """
        Test para crear un color con un nombre que ya existe.
        Debe devolver un error 422.
        """
        color_data = ColorCreate(
            nombre="Verde",  # Nombre ya existente
            codigo_hex="#00FF00",
            url_imagen="http://example.com/verde.png",
            activo=True,
            descripcion="Color verde brillante",
            id_familia=None
        )
        
        response = client.post("/colores", json=color_data.model_dump())
        
        assert response.status_code == 400

    def test_crear_nuevo_color(self):
        """
        Test para crear un nuevo color.
        Debe devolver el color creado con un ID asignado.
        """
        color_data = ColorCreate(
            nombre="Amarillo",
            codigo_hex="#FFFF00",
            url_imagen="http://example.com/amarillo.png",
            activo=True,
            descripcion="Color amarillo brillante",
            id_familia=None
        )
        
        response = client.post("/colores", json=color_data.model_dump())

        if response.status_code == 400:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except:
                print("No se pudo parsear el JSON del error")
        
        assert response.status_code == 201
        color = response.json()
        assert color["nombre"] == color_data.nombre
        assert color["codigo_hex"] == color_data.codigo_hex
        assert color["url_imagen"] == color_data.url_imagen
        assert color["activo"] == color_data.activo

    def test_crear_color_con_familia_no_existente(self):
        """
        Test para crear un color con una familia que no existe.
        Debe devolver un error 404.
        """
        color_data = ColorCreate(
            nombre="Naranja",
            codigo_hex="#FFA500",
            url_imagen="http://example.com/naranja.png",
            activo=True,
            descripcion="Color naranja brillante",
            id_familia=9999  # ID de familia no existente
        )
        
        response = client.post("/colores", json=color_data.model_dump())
        
        assert response.status_code == 400

    def test_actulizar_color_existente(self):
        """
        Test para actualizar un color existente.
        Debe devolver el color actualizado.
        """
        color_data = ColorUpdate(
            nombre="Verde Claro",
            codigo_hex="#90EE90",
            url_imagen="http://example.com/verde_claro.png",
            activo=True,
            descripcion="Color verde claro brillante",
            id_familia=2
        )
        
        response = client.put("/colores/1", json=color_data.model_dump())

        if response.status_code == 400:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except:
                print("No se pudo parsear el JSON del error")
        
        assert response.status_code == 200
        color = response.json()
        assert color["id"] == 1
        assert color["nombre"] == "Verde Claro"
        assert color["codigo_hex"] == "#90EE90"
        assert color["url_imagen"] == "http://example.com/verde_claro.png"
        assert color["activo"] is True
        assert color["descripcion"] == "Color verde claro brillante"
        assert color["id_familia"] == 2

    def test_actualizar_color_a_otro_existente(self):
        """
        Test para actualizar un color a otro nombre que ya existe.
        Debe devolver un error 422.
        """
        color_data = ColorUpdate(
            nombre="Azul",  # Nombre ya existente
            codigo_hex="#0000FF",
            url_imagen="http://example.com/azul.png",
            activo=True,
            descripcion="Color azul brillante actualizado",
            id_familia=None
        )
        
        response = client.put("/colores/1", json=color_data.model_dump())
        
        assert response.status_code == 400

    def test_actualizar_color_inexistente(self):
        """
        Test para actualizar un color que no existe.
        Debe devolver un error 404.
        """
        color_data = ColorUpdate(
            nombre="Verde",
            codigo_hex="#00FF00",
            url_imagen="http://example.com/verde.png",
            activo=True,
            descripcion="Color verde brillante",
            id_familia=None
        )
        
        response = client.put("/colores/9999", json=color_data.model_dump())
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Color no encontrado"}

    def test_actualizar_a_familia_no_existente(self):
        """
        Test para actualizar un color a una familia que no existe.
        Debe devolver un error 422.
        """
        color_data = ColorUpdate(
            nombre="Verde",
            codigo_hex="#00FF00",
            url_imagen="http://example.com/verde.png",
            activo=True,
            descripcion="Color verde brillante",
            id_familia=9999  # ID de familia no existente
        )
        
        response = client.put("/colores/1", json=color_data.model_dump())
        
        assert response.status_code == 404

    def test_eliminar_color_existente(self):
        """
        Test para eliminar un color que existe.
        Debe devolver un mensaje de éxito.
        """
        response = client.delete("/colores/1")
        
        if response.status_code == 500:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except:
                print("No se pudo parsear el JSON del error")
        
        assert response.status_code == 200
        assert response.json() == {"detail": "Color eliminado exitosamente"}

    def test_eliminar_color_no_existente(self):
        """
        Test para eliminar un color que no existe.
        Debe devolver un error 404.
        """
        response = client.delete("/colores/9999")
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Color no encontrado"}

    