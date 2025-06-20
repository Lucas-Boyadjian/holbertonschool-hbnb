<<<<<<< HEAD
=======
#!/usr/bin/env python3

import pytest
>>>>>>> origin/main
from app.models.amenity import Amenity
from app import create_app

def test_amenity_creation_valid():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"

def test_amenity_creation_empty_name():
    with pytest.raises(ValueError):
        Amenity(name="")

def test_amenity_creation_long_name():
    with pytest.raises(ValueError):
        Amenity(name="A" * 51)

def test_amenity_setter_valid():
    amenity = Amenity(name="Piscine")
    amenity.name = "Barbecue"
    assert amenity.name == "Barbecue"

def test_amenity_setter_invalid():
    amenity = Amenity(name="Piscine")
    with pytest.raises(ValueError):
        amenity.name = ""
    with pytest.raises(ValueError):
        amenity.name = "B" * 51

def test_amenity_to_dict():
    amenity = Amenity(name="Wi-Fi")
    d = amenity.to_dict()
    assert d["name"] == "Wi-Fi"
    assert "id" in d
    assert "created_at" in d
    assert "updated_at" in d

def test_amenity_multiple_setter():
    amenity = Amenity(name="Piscine")
    amenity.name = "Barbecue"
    amenity.name = "Sauna"
    assert amenity.name == "Sauna"

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_api_create_amenity_valid(client):
    response = client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    assert response.status_code == 201
    assert response.json["name"] == "Wi-Fi"
    assert "id" in response.json

def test_api_create_amenity_empty_name(client):
    response = client.post('/api/v1/amenities/', json={"name": ""})
    assert response.status_code == 400

def test_api_create_amenity_long_name(client):
    response = client.post('/api/v1/amenities/', json={"name": "A" * 51})
    assert response.status_code == 400

def test_api_get_all_amenities(client):
    client.post('/api/v1/amenities/', json={"name": "Piscine"})
    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(a["name"] == "Piscine" for a in response.json)

def test_api_get_amenity_by_id(client):
    post_resp = client.post('/api/v1/amenities/', json={"name": "Sauna"})
    amenity_id = post_resp.json["id"]
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    assert response.json["id"] == amenity_id
    assert response.json["name"] == "Sauna"

def test_api_get_amenity_not_found(client):
    response = client.get('/api/v1/amenities/doesnotexist')
    assert response.status_code == 404

def test_api_update_amenity_valid(client):
    post_resp = client.post('/api/v1/amenities/', json={"name": "Jacuzzi"})
    amenity_id = post_resp.json["id"]
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Hammam"})
    assert response.status_code == 200
    assert response.json["name"] == "Hammam"

def test_api_update_amenity_invalid_name(client):
    post_resp = client.post('/api/v1/amenities/', json={"name": "Spa"})
    amenity_id = post_resp.json["id"]
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={"name": ""})
    assert response.status_code == 400

def test_api_update_amenity_not_found(client):
    response = client.put('/api/v1/amenities/doesnotexist', json={"name": "NewName"})
    assert response.status_code == 404