from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestArticuloCRUD:
    def test_listar_articulos(self):
        res = client.get("/articulo/")
        assert res.status_code == 200
        assert isinstance(res.json(), dict)
        
    def test_crear_y_actualizar_articulo_simple(self):
        data = {"nombre": "Articulo Simple", "tipo": "simple"}
        res = client.post("/articulo/", json=data)
        assert res.status_code == 201
        art = res.json()
        assert art["nombre"] == "Articulo Simple"
        assert art["tipo"] == "simple"
        articulo_id = art["id"]
        res = client.put(f"/articulo/{articulo_id}", json={"nombre": "Articulo Modificado", "tipo": "simple"})
        assert res.status_code == 200
        art = res.json()
        assert art["nombre"] == "Articulo Modificado"
        assert art["tipo"] == "simple"

    def test_crear_y_actualizar_articulo_compuesto(self):
        data = {"nombre": "Articulo Compuesto", "tipo": "compuesto"}
        res = client.post("/articulo/", json=data)
        assert res.status_code == 201
        art = res.json()
        assert art["nombre"] == "Articulo Compuesto"
        assert art["tipo"] == "compuesto"
        articulo_id = art["id"]
        res = client.put(f"/articulo/{articulo_id}", json={"nombre": "Articulo Modificado Compuesto", "tipo": "compuesto"})
        assert res.status_code == 200
        art = res.json()
        assert art["nombre"] == "Articulo Modificado Compuesto"
        assert art["tipo"] == "compuesto"

    def test_crear_y_actualizar_articulo_pack(self):
        data = {"nombre": "Articulo Pack", "tipo": "pack"}
        res = client.post("/articulo/", json=data)
        assert res.status_code == 201
        art = res.json()
        assert art["nombre"] == "Articulo Pack"
        assert art["tipo"] == "pack"
        articulo_id = art["id"]
        res = client.put(f"/articulo/{articulo_id}", json={"nombre": "Articulo Modificado Pack", "tipo": "pack"})
        assert res.status_code == 200
        art = res.json()
        assert art["nombre"] == "Articulo Modificado Pack"
        assert art["tipo"] == "pack"

    def test_crear_articulo_invalido(self):
        data = {"nombre": "Articulo Invalido", "tipo": "invalido"}
        res = client.post("/articulo/", json=data)
        assert res.status_code == 422

    def test_actualizar_articulo_invalido(self):
        data = {"nombre": "Articulo Simple", "tipo": "simple"}
        res = client.post("/articulo/", json=data)
        assert res.status_code == 201
        art = res.json()
        assert art["nombre"] == "Articulo Simple"
        assert art["tipo"] == "simple"
        articulo_id = art["id"]
        res = client.put(f"/articulo/{articulo_id}", json={"nombre": "Articulo Modificado", "tipo": "invalido"})
        assert res.status_code == 422
        
    def test_obtener_articulo_por_id(self):
        data = {"nombre": "ArticuloX", "tipo": "compuesto"}
        res = client.post("/articulo/", json=data)
        art_id = res.json()["id"]
        res = client.get(f"/articulo/{art_id}")
        assert res.status_code == 200
        assert res.json()["id"] == art_id

    def test_actualizar_articulo(self):
        data = {"nombre": "ArticuloY", "tipo": "simple"}
        res = client.post("/articulo/", json=data)
        art_id = res.json()["id"]
        update_data = {"nombre": "ArticuloMod", "tipo": "simple"}
        res = client.put(f"/articulo/{art_id}", json=update_data)
        assert res.status_code == 200
        assert res.json()["nombre"] == "ArticuloMod"

    def test_actualizar_articulo_inexistente(self):
        res = client.put("/articulo/9999", json={"nombre": "Articulo Inexistente", "tipo": "simple"})
        assert res.status_code == 404

    def test_eliminar_articulo_simple(self):
        data = {"nombre": "ArticuloZ", "tipo": "simple"}
        res = client.post("/articulo/", json=data)
        art_id = res.json()["id"]
        res = client.delete(f"/articulo/{art_id}")
        assert res.status_code == 200
        res = client.get(f"/articulo/{art_id}")
        assert res.status_code == 404

    def test_eliminar_articulo_compuesto(self):
        data = {"nombre": "Articulo Compuesto", "tipo": "compuesto"}
        res = client.post("/articulo/", json=data)
        art_id = res.json()["id"]
        res = client.delete(f"/articulo/{art_id}")
        assert res.status_code == 200
        res = client.get(f"/articulo/{art_id}")
        assert res.status_code == 404
        
    def test_eliminar_articulo_pack(self):
        data = {"nombre": "Articulo Pack", "tipo": "pack"}
        res = client.post("/articulo/", json=data)
        art_id = res.json()["id"]
        res = client.delete(f"/articulo/{art_id}")
        assert res.status_code == 200
        res = client.get(f"/articulo/{art_id}")
        assert res.status_code == 404