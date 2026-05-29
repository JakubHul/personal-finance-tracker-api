def get_token(client, email="user@example.com", password="secret123"):
    client.post(
        "/register",
        json={"email": email, "password": password},
    )
    response = client.post(
        "/login",
        json={"email": email, "password": password},
    )
    return response.json()["access_token"]


def test_create_transaction(client):
    token = get_token(client)

    response = client.post(
        "/transactions",
        json={"amount": 100, "category": "food"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert response.json()["amount"] == 100


def test_get_transactions_unauthorized(client):
    response = client.get("/transactions")
    assert response.status_code == 401


def test_user_isolation(client):
    token_a = get_token(client, email="a@test.com", password="pass1234")

    client.post(
        "/transactions",
        json={"amount": 999, "category": "secret"},
        headers={"Authorization": f"Bearer {token_a}"},
    )

    token_b = get_token(client, email="b@test.com", password="pass1234")

    response = client.get(
        "/transactions",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert response.status_code == 200
    assert response.json() == []
