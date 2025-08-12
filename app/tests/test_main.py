from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

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
    def test_health_check_db_connected():
        with patch("app.main.get_db") as mock_get_db:
            mock_db = MagicMock()
            mock_db.execute.return_value = None
            mock_get_db.return_value.__enter__.return_value = mock_db
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["estado"] == "✅ Saludable"
            assert data["base_datos"] == "✅ Conectada"
            assert "timestamp" in data
