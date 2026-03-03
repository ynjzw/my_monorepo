import pytest
from fastapi.testclient import TestClient
from apps.server.main import app

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}

def test_get_datas():
    response = client.get("/data")
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_get_links():
    response = client.get("/links")
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_get_family():
    response = client.get("/family")
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_get_world():
    response = client.get("/world")
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_upload_file():
    # This test would require a file upload simulation
    pass

def test_get_files():
    response = client.get("/files")
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_get_file():
    # This test would require a valid file ID
    pass

def test_delete_file():
    # This test would require a valid file ID
    pass

def test_get_statistics():
    response = client.get("/stats")
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_speech_to_text():
    response = client.get("/speechtotext")
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_chat_with_ollama():
    response = client.post("/chat", json={"text": "Hello"})
    assert response.status_code == 200
    # Add more assertions based on expected data