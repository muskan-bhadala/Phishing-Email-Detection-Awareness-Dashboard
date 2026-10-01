from app.services.analyzer import analyze_email, extract_urls

def test_phishing_signals_raise_risk():
    result = analyze_email(
        "security-alert123@gmail.com",
        "URGENT: Verify your account",
        "Your account is suspended. Verify your password immediately at http://192.168.1.50/login"
    )
    assert result["risk_score"] >= 40
    assert result["risk_level"] in {"MEDIUM", "HIGH"}
    assert len(result["indicators"]) > 0

def test_normal_email_has_lower_signal():
    result = analyze_email(
        "team@example.org",
        "Project meeting",
        "Hello, our project meeting is scheduled for Friday at 10 AM."
    )
    assert result["risk_score"] < 70

def test_url_extraction():
    urls = extract_urls("Visit https://example.com and http://test.local/path.")
    assert len(urls) == 2

def test_attachment_detection():
    result = analyze_email("a@example.com", "Report", "Please open invoice.exe and script.js")
    assert any("risky attachment" in x for x in result["indicators"])

def test_explainability_fields_exist():
    result = analyze_email("a@example.com", "Hello", "Just checking in.")
    assert "explanation" in result
    assert set(result["explanation"]) == {"sender", "content", "urls", "attachments"}
