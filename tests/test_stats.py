def get_token(client, email, password="secret123"):
    client.post(
        "/register",
        json={"email": email, "password": password},
    )
    response = client.post(
        "/login",
        json={"email": email, "password": password},
    )
    return response.json()["access_token"]


def test_stats_requires_auth(client):
    response = client.get("/stats")
    assert response.status_code == 401


def test_stats_user_isolation(client):
    token_a = get_token(client, "stats-a@test.com")
    token_b = get_token(client, "stats-b@test.com")

    client.post(
        "/transactions",
        json={"amount": 40, "category": "food"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    client.post(
        "/transactions",
        json={"amount": 60, "category": "transport"},
        headers={"Authorization": f"Bearer {token_a}"},
    )

    response_b = client.get(
        "/stats",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert response_b.status_code == 200
    assert response_b.json() == {
        "total_expenses": 0,
        "total_number": 0,
        "max_amount": 0,
    }
