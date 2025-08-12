from asyncio import sleep
from fastapi.testclient import TestClient
from app.db import SessionLocal
from app.main import app
from app.tests import reset_db

client = TestClient(app)

class TestComponenteCRUD:
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
        
    def test_listar_componente(self):
        res = client.get("/componente/")
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        
    def test_crear_componente(self):
        prov = client.post("/proveedor/", json={"nombre": "ProvComp", "email": "prov@comp.com"}).json()
        data = {"nombre": "CompTest", "id_proveedor": prov["id"]}
        res = client.post("/componente/", json=data)
        assert res.status_code == 201
        comp = res.json()
        assert comp["nombre"] == "CompTest"
        assert comp["id_proveedor"] == prov["id"]

    def test_obtener_componente_por_id(self):
        prov = client.post("/proveedor/", json={"nombre": "ProvComp2", "email": "prov2@comp.com"}).json()
        comp = client.post("/componente/", json={"nombre": "CompX", "id_proveedor": prov["id"]}).json()
        comp_id = comp["id"]
        res = client.get(f"/componente/{comp_id}")
        assert res.status_code == 200
        assert res.json()["id"] == comp_id

    def test_actualizar_componente(self):
        prov = client.post("/proveedor/", json={"nombre": "ProvComp3", "email": "prov3@comp.com"}).json()
        comp = client.post("/componente/", json={"nombre": "CompY", "id_proveedor": prov["id"]}).json()
        comp_id = comp["id"]
        res = client.put(f"/componente/{comp_id}", json={"nombre": "CompMod"})
        assert res.status_code == 200
        assert res.json()["nombre"] == "CompMod"

    def test_eliminar_componente(self):
        prov = client.post("/proveedor/", json={"nombre": "ProvComp4", "email": "prov4@comp.com"}).json()
        comp = client.post("/componente/", json={"nombre": "CompZ", "id_proveedor": prov["id"]}).json()
        comp_id = comp["id"]
        res = client.delete(f"/componente/{comp_id}")
        assert res.status_code == 200
        res = client.get(f"/componente/{comp_id}")
        assert res.status_code == 404

    def test_obtener_componentes_por_producto_compuesto(self):
        # Creamos un proveedor para los componentes
        prov = client.post("/proveedor/", json={"nombre": "ProvCompTest", "email": "provcomp@test.com"}).json()
        # Creamos un producto compuesto y 2 componentes y los asociamos
        comp1 = client.post("/componente/", json={"nombre": "CompA", "id_proveedor": prov["id"]}).json()
        comp2 = client.post("/componente/", json={"nombre": "CompB", "id_proveedor": prov["id"]}).json()
        producto_compuesto = client.post("/articulo/", json={
            "nombre": "ProductoCompuesto1",
            "tipo": "compuesto",
        }).json()
        prod_id = producto_compuesto["id"]
        componentes = [
            {"id_componente": comp1["id"], "cantidad": 2},
            {"id_componente": comp2["id"], "cantidad": 3}
        ]
        
        # Asociamos los componentes al producto compuesto
        resp = client.post(f"/componente/compuesto/{prod_id}", json=componentes)
        assert resp.status_code == 200

        # Obtenemos los componenetes
        resp = client.get(f"/componente/compuesto/{prod_id}")
        assert resp.status_code == 200
        componentes_resp = resp.json()
        assert len(componentes_resp) == 2
        assert componentes_resp[0]["id"] in [comp1["id"], comp2["id"]]
        assert componentes_resp[1]["id"] in [comp1["id"], comp2["id"]]

        # Eliminamos los componentes del producto compuesto
        resp = client.request(
            "DELETE",
            f"/componente/compuesto/{prod_id}",
            json=[comp1["id"], comp2["id"]],
        )
        assert resp.status_code == 200
        resp = client.get(f"/componente/compuesto/{prod_id}")
        assert resp.status_code == 200
        componentes_resp = resp.json()
        assert len(componentes_resp) == 0