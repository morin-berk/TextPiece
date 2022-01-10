from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_pieces_with_nonexistent_index():
    response = client.get("/pieces/")
    assert response.status_code == 404
    assert response.json() == {'detail': 'The index doesn`t exist yet.'}
