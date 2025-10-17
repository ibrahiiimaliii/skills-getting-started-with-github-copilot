from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    # Test structure of an activity
    first_activity = list(activities.values())[0]
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity

def test_signup_for_activity():
    # Get first activity name
    activities = client.get("/activities").json()
    activity_name = list(activities.keys())[0]
    test_email = "test_student@mergington.edu"
    
    # Test successful signup
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {test_email} for {activity_name}"
    
    # Test duplicate signup
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

def test_unregister_from_activity():
    # Get first activity name
    activities = client.get("/activities").json()
    activity_name = list(activities.keys())[0]
    test_email = "test_unregister@mergington.edu"
    
    # First sign up a test user
    client.post(f"/activities/{activity_name}/signup?email={test_email}")
    
    # Test successful unregister
    response = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {test_email} from {activity_name}"
    
    # Test unregistering non-registered user
    response = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()

def test_signup_nonexistent_activity():
    response = client.post("/activities/nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_nonexistent_activity():
    response = client.post("/activities/nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"