from time import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.schemas.proveedorDTO import ProveedorCreate, ProveedorUpdate
from sqlalchemy import text

from app.tests import reset_db

client = TestClient(app)

class TestEmptyProveedorDB:
    @classmethod
    def setup_class(cls):
        """
        Se ejecuta una vez antes de todos los tests de la clase.
        Limpia la tabla de colores en la base de datos.
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

    def test_listar_proveedores_vacio(self):
        """
        Test para verificar que la lista de proveedores está vacía.
        """
        response = client.get("/proveedores/")

        if response.status_code == 500:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except:
                print("No se pudo parsear el JSON del error")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_obtener_proveedor_no_existe(self):
        """
        Test para verificar que al intentar obtener un proveedor que no existe, se retorna 404.
        """
        response = client.get("/proveedores/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Proveedor no encontrado"}

    def test_crear_proveedor(self):
        """
        Test para crear un proveedor y verificar que se crea correctamente.
        """
        nuevo_proveedor = ProveedorCreate(
            nombre="Proveedor Test",
            nif_cif="12345678A",
            telefono="123456789",
            email="hola@prueba.com",
            direccion="Calle Falsa 123",
            activo=True
            )
        response = client.post("/proveedores/", json=nuevo_proveedor.model_dump())    

        assert response.status_code == 201
        proveedor = response.json()
        nuevo_proveedor = nuevo_proveedor.model_dump()
        for key in nuevo_proveedor.keys():
            assert proveedor[key] == nuevo_proveedor[key]

    def test_crear_proveedor_sin_nombre(self):
        """
        Test para crear un proveedor sin nombre.
        Debe retornar un error de validación.
        """
        proveedor_data = {
            "nombre": "",
            "nif_cif": "12345678A",
            "telefono": "123456789",
            "email": "hola@prueba.com",
            "direccion": "Calle Falsa 123",
            "activo": True
        }
        response = client.post("/proveedores/", json=proveedor_data)

        assert response.status_code == 400

    def test_crear_proveedor_sin_nif_cif(self):
        """
        Test para crear un proveedor sin NIF/CIF.
        Debe retornar un error de validación.
        """
        proveedor_data = {
            "nombre": "Proveedor Test",
            "nif_cif": "",
            "telefono": "123456789",
            "email": "hola@prueba.com",
            "direccion": "Calle Falsa 123",
            "activo": True
        }
        response = client.post("/proveedores/", json=proveedor_data)

        assert response.status_code == 400

    def test_crear_proveedor_con_email_invalido(self):
        """
        Test para crear un proveedor con un email inválido.
        Debe retornar un error de validación.
        """
        proveedor_data = {
            "nombre": "Proveedor Test",
            "nif_cif": "12345678A",
            "telefono": "123456789",
            "email": "noesunemail",
            "direccion": "Calle Falsa 123",
            "activo": True
        }
        response = client.post("/proveedores/", json=proveedor_data)

        assert response.status_code == 400

    def test_crear_proveedor_con_telefono_invalido(self):
        """
        Test para crear un proveedor con un teléfono inválido.
        Debe retornar un error de validación.
        """
        proveedor_data = {
            "nombre": "Proveedor Test",
            "nif_cif": "12345678A",
            "telefono": "noesuntelefono",
            "email": "hola@prueba.com",
            "direccion": "Calle Falsa 123",
            "activo": True
        }
        response = client.post("/proveedores/", json=proveedor_data)
        assert response.status_code == 400

    def test_actualizar_proveedor_inexistente(self):
        """
        Test para intentar actualizar un proveedor que no existe.
        Debe retornar un error 404.
        """
        proveedor_data = ProveedorUpdate(
            nombre="Proveedor Actualizado",
            nif_cif="87654321B",
            telefono="987654321",
            email="hola@prueba.com",
            direccion="Calle Falsa 456",
            activo=True
        )
        response = client.put("/proveedores/9999", json=proveedor_data.model_dump())
        assert response.status_code == 404
        assert response.json() == {"detail": "Proveedor no encontrado"}

    def test_eliminar_proveedor_inexistente(self):
        """
        Test para intentar eliminar un proveedor que no existe.
        Debe retornar un error 404.
        """
        response = client.delete("/proveedores/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Proveedor no encontrado"}

class TestProveedorDBWithData:
    @classmethod
    def setup_class(cls):
        """
        Se ejecuta una vez antes de todos los tests de la clase.
        Limpia la tabla de proveedores en la base de datos y crea un proveedor de prueba.
        """
        cls.db = SessionLocal()
        try:
            reset_db(cls.db)
            sleep(1)  # Esperar un segundo para asegurar que la base de datos esté limpia
            
            # Crear un proveedor de prueba
            proveedor_data = [
                {
                    "nombre": "Proveedor Uno",
                    "nif_cif": "11111111A",
                    "telefono": "+39 600111111",
                    "email": "uno@proveedor.com",
                    "direccion": "Calle Uno 1",
                    "activo": True
                },
                {
                    "nombre": "Proveedor Dos",
                    "nif_cif": "22222222B",
                    "telefono": "600222222",
                    "email": "dos@proveedor.com",
                    "direccion": "Calle Dos 2",
                    "activo": False
                }
            ]
            for proveedor in proveedor_data:
                cls.db.execute(
                    text("""
                        INSERT INTO proveedor (nombre, nif_cif, telefono, email, direccion, activo)
                        VALUES (:nombre, :nif_cif, :telefono, :email, :direccion, :activo)
                    """), 
                    {
                        "nombre": proveedor["nombre"],
                        "nif_cif": proveedor["nif_cif"],
                        "telefono": proveedor["telefono"],
                        "email": proveedor["email"],
                        "direccion": proveedor["direccion"],
                        "activo": proveedor["activo"]
                    }
                )
            cls.db.commit()
            sleep(1)  # Esperar un segundo para asegurar que los datos estén disponibles
        finally:
            cls.db.close()

    def setup_method(self, method):
        """
        Se ejecuta antes de cada test.
        Limpia la tabla de proveedores en la base de datos.
        """
        self.db = SessionLocal()

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

    def test_listar_proveedores_con_datos(self):
        """
        Test para listar proveedores cuando ya existen datos.
        Debe devolver una lista con los proveedores creados en setup_class.
        """
        response = client.get("/proveedores/")

        if response.status_code == 500:
            try:
                error_detail = response.json()
                print(f"Error detail: {error_detail}")
            except:
                print("No se pudo parsear el JSON del error")
        
        assert response.status_code == 200
        proveedores = response.json()
        assert len(proveedores) == 2
        assert proveedores[0]["nombre"] == "Proveedor Uno"
        assert proveedores[1]["nombre"] == "Proveedor Dos"

    def test_obtener_proveedor_existente(self):
        """
        Test para obtener un proveedor existente.
        Debe devolver el proveedor con ID 1.
        """
        response = client.get("/proveedores/1")
        assert response.status_code == 200
        proveedor = response.json()
        assert proveedor["nombre"] == "Proveedor Uno"
        assert proveedor["nif_cif"] == "11111111A"

    def test_obtener_proveedor_inexistente(self):
        """
        Test para intentar obtener un proveedor que no existe.
        Debe retornar un error 404.
        """
        response = client.get("/proveedores/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Proveedor no encontrado"}

    def test_crear_proveedor_con_datos(self):
        """
        Test para crear un nuevo proveedor cuando ya existen datos.
        Debe devolver el proveedor creado con un ID asignado.
        """
        nuevo_proveedor = ProveedorCreate(
            nombre="Proveedor Tres",
            nif_cif="33333333C",
            telefono="600333333",
            email="tres@proveedor.com",
            direccion="Calle Tres 3",
            activo=True
        )
        response = client.post("/proveedores/", json=nuevo_proveedor.model_dump())
        assert response.status_code == 201
        proveedor = response.json()
        nuevo_proveedor = nuevo_proveedor.model_dump()
        for key in nuevo_proveedor.keys():
            assert proveedor[key] == nuevo_proveedor[key]

    def test_crear_proveedor_con_nombre_existente(self):
        """
        Test para intentar crear un proveedor con un nombre que ya existe.
        Debe retornar un error de validación.
        """
        nuevo_proveedor = ProveedorCreate(
            nombre="Proveedor Uno",  # Nombre ya existente
            nif_cif="33333333C",
            telefono="600333333",
            email="tres@proveedor.com",
            direccion="Calle Tres 3",
            activo=True
        )
        response = client.post("/proveedores/", json=nuevo_proveedor.model_dump())
        assert response.status_code == 400

    def test_crear_proveedor_con_nif_cif_existente(self):
        """
        Test para intentar crear un proveedor con un NIF/CIF que ya existe.
        Debe retornar un error de validación.
        """
        nuevo_proveedor = ProveedorCreate(
            nombre="Proveedor Cuatro",
            nif_cif="11111111A",  # NIF/CIF ya existente
            telefono="600444444",
            email="cuatro@proveedor.com",
            direccion="Calle Cuatro 4",
            activo=True
        )
        response = client.post("/proveedores/", json=nuevo_proveedor.model_dump())
        assert response.status_code == 400

    def test_actualizar_proveedor_existente(self):
        """
        Test para actualizar un proveedor existente.
        Debe devolver el proveedor actualizado.
        """
        proveedor_data = ProveedorUpdate(
            nombre="Proveedor Uno Actualizado",
            nif_cif="11111111A",
            telefono="600111111",
            email="unouno@proveedor.com",
            direccion="Calle Uno Actualizada 1",
            activo=True
        )
        response = client.put("/proveedores/1", json=proveedor_data.model_dump())
        assert response.status_code == 200
        proveedor = response.json()
        proveedor_data = proveedor_data.model_dump()
        for key in proveedor_data.keys():
            assert proveedor[key] == proveedor_data[key]

    def test_actualizar_proveedor_a_nombre_existente(self):
        """
        Test para intentar actualizar un proveedor que no existe.
        Debe retornar un error 404.
        """
        proveedor_data = ProveedorUpdate(
            nombre="Proveedor Dos",
            nif_cif="22222222ABC",
            telefono="600222222",
            email="unouno@proveedor.com",
            direccion="Calle Uno Actualizada 1",
            activo=True
        )
        response = client.put("/proveedores/1", json=proveedor_data.model_dump())
        assert response.status_code == 400

    def test_actualizar_proveedor_a_nifcif_existente(self):
        """
        Test para intentar actualizar un proveedor a un NIF/CIF que ya existe.
        Debe retornar un error de validación.
        """
        proveedor_data = ProveedorUpdate(
            nombre="Proveedor Uno",
            nif_cif="22222222B",  # NIF/CIF ya existente
            telefono="600111111",
            email="unouno@proveedor.com",
            direccion="Calle Uno Actualizada 1",
            activo=True
        )
        response = client.put("/proveedores/1", json=proveedor_data.model_dump())
        assert response.status_code == 400

    def test_actualizar_proveedor_telefono_invalido(self):
        """
        Test para intentar actualizar un proveedor con un teléfono inválido.
        Debe retornar un error de validación.
        """
        proveedor_data = {
            "nombre": "Proveedor Uno",
            "nif_cif": "11111111A",
            "telefono": "noesuntelefono",  # Teléfono inválido
            "email": "unouno@proveedor.com",
            "direccion": "Calle Uno Actualizada 1",
            "activo": True
        }
        response = client.put("/proveedores/1", json=proveedor_data)
        assert response.status_code == 400

    def test_actualizar_proveedor_email_invalido(self):
        """
        Test para intentar actualizar un proveedor con un email inválido.
        Debe retornar un error de validación.
        """
        proveedor_data = {
            "nombre": "Proveedor Uno",
            "nif_cif": "11111111A",
            "telefono": "600111111",
            "email": "noesunemail",  # Email inválido
            "direccion": "Calle Uno Actualizada 1",
            "activo": True
        }
        response = client.put("/proveedores/1", json=proveedor_data)
        assert response.status_code == 400

    def test_eliminar_proveedor_existente(self):
        """
        Test para eliminar un proveedor existente.
        Debe retornar un mensaje de éxito.
        """
        response = client.delete("/proveedores/1")
        assert response.status_code == 200
        assert response.json() == {"detail": "Proveedor eliminado exitosamente"}
