from fastapi.testclient import TestClient
from app.main import app


def test_get_applications():
    with TestClient(app) as client:
        response = client.get("/applications")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_application():
    job = {
        "company": "Google",
        "position": "Intern",
        "status": "Applied"
    }

    with TestClient(app) as client:
        response = client.post("/applications", json=job)

    assert response.status_code == 200
    assert response.json()["company"] == job["company"] #read the response data as a Python dictionary.
    assert "id" in response.json()

def test_delete_application():
    job = {
        "company": "Microsoft",
        "position": "Intern",
        "status": "Applied"
    }

    with TestClient(app) as client:
        create_response = client.post("/applications", json=job)
        create_id = create_response.json()["id"]
        delete_response = client.delete(f"/applications/{create_id}")

    assert delete_response.status_code == 204

