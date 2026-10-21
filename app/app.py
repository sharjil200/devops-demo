import os, time
from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "dev")

REQUESTS = Counter("http_requests_total", "Total requests", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["path"])


@app.before_request
def _start():
    request._t = time.time()


@app.after_request
def _record(resp):
    path = request.path
    LATENCY.labels(path).observe(time.time() - getattr(request, "_t", time.time()))
    REQUESTS.labels(request.method, path, resp.status_code).inc()
    return resp


@app.get("/")
def index():
    return jsonify(message="Hello from DevOps demo", version=VERSION)


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
