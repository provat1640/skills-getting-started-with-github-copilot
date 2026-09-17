from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_signup_registers_participant():
    email = "test-signup@mergington.edu"
    activity_name = "Swimming Club"
    try:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    finally:
        if email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(email)


def test_signup_rejects_duplicate_participant():
    email = "existing-participant@mergington.edu"
    activity_name = "Art Studio"
    activities[activity_name]["participants"].append(email)

    try:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up"
    finally:
        activities[activity_name]["participants"].remove(email)


def test_unregister_removes_participant():
    email = "test-unregister@mergington.edu"
    activity_name = "Debate Team"
    activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
