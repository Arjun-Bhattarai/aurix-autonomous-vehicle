import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.routes.vehicle import get_vehicle
from app.vehicle.simulator import SimulatedVehicle


@pytest.fixture
def client():
    """Provides a TestClient with an isolated, fresh SimulatedVehicle instance for every test."""
    test_vehicle = SimulatedVehicle()
    app.dependency_overrides[get_vehicle] = lambda: test_vehicle
    
    with TestClient(app) as c:
        yield c
        
    app.dependency_overrides.clear()


def test_get_vehicle_state(client):
    response = client.get("/api/v1/state")
    assert response.status_code == 200
    data = response.json()
    assert data["speed"] == 0.0
    assert data["steering"] == 0.0
    assert data["throttle"] == 0.0
    assert data["brake"] is False
    assert data["is_connected"] is True
    assert data["mode"] == "simulation"


def test_control_vehicle(client):
    response = client.post(
        "/api/v1/control",
        json={
            "steering": 0.5,
            "throttle": 0.8,
            "brake": False
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["steering"] == 0.5
    assert data["throttle"] == 0.8
    assert data["brake"] is False 


def test_emergency_stop(client):
    response = client.post("/api/v1/emergency-stop")
    assert response.status_code == 200
    data = response.json()
    assert data["speed"] == 0.0
    assert data["throttle"] == 0.0
    assert data["brake"] is True      
    assert data["emergency_stopped"] is True


def test_brake_vehicle(client):
    response = client.post(
        "/api/v1/control",
        json={
            "steering": 0.5,
            "throttle": 0.8,
            "brake": True
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["throttle"] == 0.0  
    assert data["brake"] is True    
    assert data["emergency_stopped"] is False


def test_reset_emergency_stop(client):
    client.post("/api/v1/emergency-stop")

    response = client.post("/api/v1/reset-emergency-stop")
    assert response.status_code == 200

    data = response.json()
    assert data["emergency_stopped"] is False
    assert data["brake"] is False
    assert data["throttle"] == 0.0
    assert data["speed"] == 0.0     

    reset_response = client.post("/api/v1/control", json={"steering": 0.5, "throttle": 0.7, "brake": False})
    assert reset_response.status_code == 200
    assert reset_response.json()["throttle"] == 0.7
    assert reset_response.json()["emergency_stopped"] is False