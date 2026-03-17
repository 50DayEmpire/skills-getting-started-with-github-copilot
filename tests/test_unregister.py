def test_unregister_removes_student_from_activity(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"

    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email not in participants


def test_unregister_returns_not_found_for_missing_activity(client):
    response = client.delete(
        "/activities/Nonexistent Activity/signup",
        params={"email": "someone@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_not_found_when_student_not_registered(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not registered for this activity"
