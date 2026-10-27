from app import app

def test_index():
    r = app.test_client().get("/")
    assert r.status_code == 200
    # Verify that the HTML template renders properly
    assert b"<!DOCTYPE html>" in r.data or b"html" in r.data

def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}

def test_metrics():
    r = app.test_client().get("/metrics")
    assert r.status_code == 200
