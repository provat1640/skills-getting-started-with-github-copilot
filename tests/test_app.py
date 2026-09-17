import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


@pytest.fixture
def registered_participant():
    activity_name = "Art Studio"
    email = "existing-participant@mergington.edu"
    activities[activity_name]["participants"].append(email)
    yield activity_name, email
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)


def test_get_activities_returns_activity_data():
    # Arrange
    activity_name = "Swimming Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert activity_name in response.json()
    assert response.json()[activity_name]["participants"] == activities[activity_name][
        "participants"
    ]


def test_signup_registers_participant():
    # Arrange
    email = "test-signup@mergington.edu"
    activity_name = "Swimming Club"
    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    finally:
        if email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(email)


def test_signup_rejects_duplicate_participant(registered_participant):
    # Arrange
    activity_name, email = registered_participant

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_rejects_unknown_activity():
    # Arrange
    activity_name = "Unknown Club"
    email = "unknown-activity@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(registered_participant):
    # Arrange
    activity_name, email = registered_participant

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_rejects_unknown_participant():
    # Arrange
    activity_name = "Debate Team"
    email = "not-registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up"
