def test_security_headers(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in response.headers
    assert response.headers["Referrer-Policy"] == "no-referrer"

def test_xss_is_escaped(client):
    payload = "<script>alert('x')</script>"
    response = client.post("/analyze", data={
        "sender": "safe@example.com",
        "subject": payload,
        "body": "Normal content"
    })
    html = response.get_data(as_text=True)
    assert payload not in html
    assert "&lt;script&gt;" in html

def test_api_rejects_missing_json_gracefully(client):
    response = client.post("/api/analyze", data="not-json",
                           content_type="application/json")
    assert response.status_code == 200
    assert "risk_score" in response.get_json()

def test_sql_injection_like_input_does_not_break_history(client):
    payload = "' OR 1=1 --"

    response = client.post("/api/analyze", json={
        "sender": "user@example.com",
        "subject": payload,
        "body": "hello"
    })

    assert response.status_code == 200

    history = client.get("/history")

    assert history.status_code == 200

    html = history.get_data(as_text=True)

    # The payload should be safely rendered/escaped rather than
    # interpreted as SQL or HTML.
    assert "OR 1=1" in html
    assert "&#39; OR 1=1 --" in html

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
