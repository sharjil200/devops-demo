from app import app


def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_index():
    r = app.test_client().get("/")
    assert r.status_code == 200
    assert "message" in r.get_json()


def test_metrics():
    c = app.test_client()
    c.get("/")
    r = c.get("/metrics")
    assert b"http_requests_total" in r.data
