def test_signup_adds_student_to_activity(client):
    email = "new.student@mergington.edu"
    activity = "Chess Club"

    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email in participants


def test_signup_rejects_duplicate_registration(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"

    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_not_found_for_missing_activity(client):
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "someone@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
