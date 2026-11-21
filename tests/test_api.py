import time
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.routes.vehicle import get_vehicle
from app.vehicle.simulator import SimulatedVehicle


@pytest.fixture
def vehicle():
    test_vehicle = SimulatedVehicle()
    app.dependency_overrides[get_vehicle] = lambda: test_vehicle
    yield test_vehicle
    app.dependency_overrides.clear()


@pytest.fixture
def client(vehicle):
    with TestClient(app) as c:
        yield c


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
            "brake": False,
        },
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
            "brake": True,
        },
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

    reset_response = client.post(
        "/api/v1/control",
        json={
            "steering": 0.5,
            "throttle": 0.7,
            "brake": False,
        },
    )
    assert reset_response.status_code == 200
    assert reset_response.json()["throttle"] == 0.7
    assert reset_response.json()["emergency_stopped"] is False


def test_reset_communication_timeout_success(client, vehicle):
    vehicle.command_timeout = 0.1
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()
    assert vehicle.communication_timed_out is True
    assert vehicle.brake is True

    vehicle.last_command_time = time.monotonic()

    response = client.post("/api/v1/reset-communication-timeout")
    assert response.status_code == 200
    data = response.json()
    assert data["communication_timed_out"] is False
    assert data["is_connected"] is True
    assert data["brake"] is True


def test_reset_communication_timeout_reject(client, vehicle):
    vehicle.command_timeout = 0.1
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()

    response = client.post("/api/v1/reset-communication-timeout")
    assert response.status_code == 409
    data = response.json()
    assert "Cannot reset communication timeout" in data["detail"]


def test_throttle_rejected_while_emergency_stop_active(client):
    estop_resp = client.post("/api/v1/emergency-stop")
    assert estop_resp.status_code == 200

    response = client.post(
        "/api/v1/control",
        json={
            "steering": 0.5,
            "throttle": 0.8,
            "brake": False,
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert "Cannot control vehicle while emergency stop is active" in data["detail"]

    state = client.get("/api/v1/state").json()
    assert state["throttle"] == 0.0
    assert state["emergency_stopped"] is True


def test_throttle_rejected_after_comm_reset_when_estop_still_active(client, vehicle):
    vehicle.command_timeout = 0.1
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()
    assert vehicle.communication_timed_out is True

    estop_resp = client.post("/api/v1/emergency-stop")
    assert estop_resp.status_code == 200
    assert estop_resp.json()["emergency_stopped"] is True

    vehicle.last_command_time = time.monotonic()

    reset_comm_resp = client.post("/api/v1/reset-communication-timeout")
    assert reset_comm_resp.status_code == 200
    assert reset_comm_resp.json()["communication_timed_out"] is False
    assert reset_comm_resp.json()["emergency_stopped"] is True

    control_resp = client.post(
        "/api/v1/control",
        json={
            "steering": 0.2,
            "throttle": 0.6,
            "brake": False,
        },
    )
    assert control_resp.status_code == 409

    state = client.get("/api/v1/state").json()
    assert state["throttle"] == 0.0
    assert state["emergency_stopped"] is True
    assert state["communication_timed_out"] is False

def test_control_rejected_during_communication_timeout(client, vehicle):
    vehicle.command_timeout = 0.1
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()
    assert vehicle.communication_timed_out is True

    response = client.post(
        "/api/v1/control",
        json={
            "steering": 0.3,
            "throttle": 0.5,
            "brake": False,
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert "Cannot control vehicle while communication timeout is active" in data["detail"]

    state = client.get("/api/v1/state").json()
    assert state["throttle"] == 0.0
    assert state["communication_timed_out"] is True
    assert state["brake"] is True


def test_heartbeat_does_not_clear_communication_timeout(client, vehicle):
    vehicle.command_timeout = 0.1
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()
    assert vehicle.communication_timed_out is True

    previous_command_time = vehicle.get_last_command_time()

    heartbeat_resp = client.post("/api/v1/heartbeat")
    assert heartbeat_resp.status_code == 200

    data = heartbeat_resp.json()
    assert vehicle.get_last_command_time() > previous_command_time
    assert data["brake"] is True
    assert data["communication_timed_out"] is True
    assert data["emergency_stopped"] is False
    assert data["is_connected"] is True