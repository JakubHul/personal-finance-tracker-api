def test_register_success(client):
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    assert "id" in response.json()


def test_register_duplicate_email(client):
    payload = {"email": "test@example.com", "password": "secret123"}
    client.post("/register", json=payload)
    response = client.post("/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_login_success(client):
    client.post(
        "/register",
        json={"email": "test@example.com", "password": "secret123"},
    )

    response = client.post(
        "/login",
        json={"email": "test@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post(
        "/register",
        json={"email": "test@example.com", "password": "secret123"},
    )

    response = client.post(
        "/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401
