from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Endpoint principal para verificar el estado de la aplicación
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert 'estado' in response.json()
    assert response.json()['estado'] == "✅ Activo"

# Endpoint de verificación de salud del sistema
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert 'estado' in response.json()
    assert response.json()['estado'] == "✅ Saludable"
    assert 'base_datos' in response.json()
    assert response.json()['base_datos'] == "✅ Conectada"