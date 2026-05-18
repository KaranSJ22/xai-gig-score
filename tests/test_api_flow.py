from __future__ import annotations

import uuid


def _register_user(api_client):
    email = f"user_{uuid.uuid4().hex}@example.com"
    payload = {
        "name": "Test User",
        "email": email,
        "password": "strongpass123",
    }
    response = api_client.post("/auth/register", json=payload)
    assert response.status_code == 201
    token = response.json()["access_token"]
    return email, token


def _register_lender(api_client):
    email = f"lender_{uuid.uuid4().hex}@example.com"
    payload = {
        "name": "Test Lender",
        "email": email,
        "password": "strongpass123",
        "institution_name": "Test Bank",
        "institution_type": "Bank",
        "license_number": f"LIC-{uuid.uuid4().hex[:8]}",
    }
    response = api_client.post("/auth/lender-register", json=payload)
    assert response.status_code == 201
    token = response.json()["access_token"]
    return email, token


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_auth_register_and_login(api_client):
    """Register and then login with valid credentials."""
    email, _ = _register_user(api_client)

    login_payload = {
        "email": email,
        "password": "strongpass123",
    }
    login_response = api_client.post("/auth/login", json=login_payload)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_auth_login_invalid_password(api_client):
    """Reject login with incorrect password."""
    email, _ = _register_user(api_client)

    login_payload = {
        "email": email,
        "password": "wrongpass",
    }
    login_response = api_client.post("/auth/login", json=login_payload)

    assert login_response.status_code == 401


def test_protected_route_requires_auth(api_client):
    """Ensure protected routes reject missing auth."""
    response = api_client.get("/platforms/")
    assert response.status_code == 401


def test_predict_requires_platform_data(api_client):
    """Predict should fail if no connected platforms exist."""
    _, token = _register_user(api_client)
    response = api_client.post("/predict/", headers=_auth_header(token))

    assert response.status_code == 400


def test_connect_platform_and_predict(api_client):
    """Connect a platform and run prediction successfully."""
    _, token = _register_user(api_client)

    connect_response = api_client.post(
        "/platforms/connect",
        json={"platform_name": "uber"},
        headers=_auth_header(token),
    )

    assert connect_response.status_code == 201

    predict_response = api_client.post("/predict/", headers=_auth_header(token))

    assert predict_response.status_code == 200
    payload = predict_response.json()

    assert "credit_score" in payload
    assert "default_probability" in payload
    assert "risk_level" in payload


def test_predict_forbidden_for_lender(api_client):
    """Ensure /predict/ returns 403 Forbidden for lender role."""
    _, token = _register_lender(api_client)
    response = api_client.post("/predict/", headers=_auth_header(token))
    assert response.status_code == 403
    assert "Borrower access required" in response.text
