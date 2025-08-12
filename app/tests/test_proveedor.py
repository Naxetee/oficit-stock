from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestProveedorCRUD:
    def test_listar_proveedor(self):
        res = client.get("/proveedor/")
        assert res.status_code == 200
        assert isinstance(res.json(), list)
    
    def test_crear_proveedor(self):
        data = {"nombre": "ProveedorTest", "email": "test@proveedor.com"}
        res = client.post("/proveedor/", json=data)
        assert res.status_code == 201
        prov = res.json()
        assert prov["nombre"] == "ProveedorTest"
        self.prov_id = prov["id"]

    def test_obtener_proveedor_por_id(self):
        data = {"nombre": "ProveedorX", "email": "x@proveedor.com"}
        res = client.post("/proveedor/", json=data)
        prov_id = res.json()["id"]
        res = client.get(f"/proveedor/{prov_id}")
        assert res.status_code == 200
        assert res.json()["id"] == prov_id

    def test_actualizar_proveedor(self):
        data = {"nombre": "ProveedorY", "email": "y@proveedor.com"}
        res = client.post("/proveedor/", json=data)
        prov_id = res.json()["id"]
        update_data = {"nombre": "ProveedorMod"}
        res = client.put(f"/proveedor/{prov_id}", json=update_data)
        assert res.status_code == 200
        assert res.json()["nombre"] == "ProveedorMod"

    def test_eliminar_proveedor(self):
        data = {"nombre": "ProveedorZ", "email": "z@proveedor.com"}
        res = client.post("/proveedor/", json=data)
        prov_id = res.json()["id"]
        res = client.delete(f"/proveedor/{prov_id}")
        assert res.status_code == 200
        res = client.get(f"/proveedor/{prov_id}")
        assert res.status_code == 404
