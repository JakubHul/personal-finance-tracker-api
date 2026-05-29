import pytest


def get_token(client, email="budget-user@example.com", password="secret123"):
    client.post("/register", json={"email": email, "password": password})
    response = client.post("/login", json={"email": email, "password": password})
    return response.json()["access_token"]


# ── helpers ──────────────────────────────────────────────────────────────────

def auth(token):
    return {"Authorization": f"Bearer {token}"}


def create_budget(client, token, name="Groceries", limit=500.0):
    return client.post(
        "/budgets",
        json={"name": name, "limit": limit},
        headers=auth(token),
    )


# ── tests ─────────────────────────────────────────────────────────────────────

def test_create_budget(client):
    token = get_token(client)
    response = create_budget(client, token)

    assert response.status_code == 201
    assert response.json()["data"]["name"] == "Groceries"
    assert response.json()["data"]["limit"] == 500.0


def test_get_all_budgets_returns_only_mine(client):
    token_a = get_token(client, "a@budgets.com")
    token_b = get_token(client, "b@budgets.com")

    create_budget(client, token_a, name="A-budget")
    create_budget(client, token_b, name="B-budget")

    response = client.get("/budgets", headers=auth(token_a))

    assert response.status_code == 200
    names = [b["name"] for b in response.json()]
    assert "A-budget" in names
    assert "B-budget" not in names


def test_get_budget_by_id(client):
    token = get_token(client)
    budget_id = create_budget(client, token).json()["data"]["id"]

    response = client.get(f"/budgets/{budget_id}", headers=auth(token))

    assert response.status_code == 200
    assert response.json()["id"] == budget_id


def test_get_other_users_budget_returns_404(client):
    token_a = get_token(client, "owner@budgets.com")
    token_b = get_token(client, "thief@budgets.com")

    budget_id = create_budget(client, token_a).json()["data"]["id"]

    response = client.get(f"/budgets/{budget_id}", headers=auth(token_b))

    assert response.status_code == 404


def test_update_budget(client):
    token = get_token(client)
    budget_id = create_budget(client, token).json()["data"]["id"]

    response = client.put(
        f"/budgets/{budget_id}",
        json={"name": "Updated", "limit": 999.0},
        headers=auth(token),
    )

    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Updated"
    assert response.json()["data"]["limit"] == 999.0


def test_delete_budget(client):
    token = get_token(client)
    budget_id = create_budget(client, token).json()["data"]["id"]

    response = client.delete(f"/budgets/{budget_id}", headers=auth(token))
    assert response.status_code == 200

    # po usunięciu powinno zwrócić 404
    follow_up = client.get(f"/budgets/{budget_id}", headers=auth(token))
    assert follow_up.status_code == 404


def test_create_budget_no_token(client):
    response = client.post("/budgets", json={"name": "X", "limit": 100.0})
    assert response.status_code == 401


def test_get_budgets_no_token(client):
    response = client.get("/budgets")
    assert response.status_code == 401


def test_get_budget_invalid_token(client):
    response = client.get(
        "/budgets",
        headers={"Authorization": "Bearer this.is.not.valid"},
    )
    assert response.status_code == 401
