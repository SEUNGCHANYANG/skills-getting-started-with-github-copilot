from urllib.parse import quote

import pytest


@pytest.mark.parametrize(
    "path, expected_redirect",
    [("/", "/static/index.html")],
)
def test_root_redirects_to_static_index(client, path, expected_redirect):
    # Arrange
    # The app mounts the static site at /static and redirects the root route there.

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers.get("location") == expected_redirect


def test_get_activities_returns_catalog(client):
    # Arrange
    # The in-memory catalog should contain the default activity list.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    activity_path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activity_path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_for_activity_rejects_missing_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "newstudent@mergington.edu"
    activity_path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activity_path = f"/activities/{quote(activity_name)}/unregister"

    # Act
    response = client.delete(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in client.get("/activities").json()[activity_name]["participants"]
