def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_signup_success(client):
    response = client.post("/signup", json={"username": "sarika", "password": "test1234"})
    assert response.status_code == 200


def test_login_success(client):
    client.post("/signup", json={"username": "sarika", "password": "test1234"})
    response = client.post("/login", data={"username": "sarika", "password": "test1234"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_note_without_token(client):
    response = client.post("/notes", json={"title": "x", "content": "y"})
    assert response.status_code == 401


def test_create_and_get_note(client, login_as):
    headers = login_as("sarika")
    client.post("/notes", json={"title": "My Note", "content": "Hello"}, headers=headers)
    response = client.get("/notes", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["notes"]) == 1