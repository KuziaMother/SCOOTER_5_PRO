import os
import sys
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if os.path.join(ROOT, "webui") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "webui"))

import app as webapp
import micloud_ltmk as ml


@pytest.fixture
def client():
    webapp.app.config["TESTING"] = True
    with webapp.app.test_client() as c:
        yield c


def test_ltmk_status(client):
    res = client.get("/api/ltmk/status")
    assert res.status_code == 200
    data = res.get_json()
    assert "logged_in" in data
    assert "qr" in data


def test_ltmk_save_manual_validation(client):
    test_mac = "2C:19:5C:99:88:77"
    safe = test_mac.replace(":", "")
    path = os.path.join(ROOT, "secrets", f"ltmk_{safe}.hex")
    if os.path.exists(path):
        os.remove(path)

    # Invalid MAC
    res = client.post("/api/ltmk/save_manual", json={"mac": "bad_mac", "ltmk_hex": "aa" * 32})
    assert res.status_code == 400

    # Empty hex
    res = client.post("/api/ltmk/save_manual", json={"mac": test_mac, "ltmk_hex": ""})
    assert res.status_code == 400

    # Non-hex characters
    res = client.post("/api/ltmk/save_manual", json={"mac": test_mac, "ltmk_hex": "gg" * 32})
    assert res.status_code == 400

    # Incorrect length (10 bytes)
    res = client.post("/api/ltmk/save_manual", json={"mac": test_mac, "ltmk_hex": "aa" * 10})
    assert res.status_code == 400

    # Valid 32 bytes (64 hex)
    res = client.post("/api/ltmk/save_manual", json={"mac": test_mac, "ltmk_hex": "11" * 32})
    assert res.status_code == 200
    assert res.get_json()["ok"] is True
    assert res.get_json()["length"] == 32
    assert ml.load_saved_ltmk_hex_exact(test_mac) == "11" * 32

    # Clean up
    if os.path.exists(path):
        os.remove(path)


def test_ltmk_password_login_validation(client):
    res = client.post("/api/ltmk/password_login", json={})
    assert res.status_code == 400

    res = client.post("/api/ltmk/password_login", json={"username": "test"})
    assert res.status_code == 400


def test_ltmk_logout(client):
    res = client.post("/api/ltmk/logout")
    assert res.status_code == 200
    assert res.get_json()["ok"] is True

