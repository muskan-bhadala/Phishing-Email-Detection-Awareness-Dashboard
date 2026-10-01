import re
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

TRAIN_TEXT = [
    "urgent verify your account click the link immediately password suspended",
    "your invoice is attached please review the document",
    "security alert confirm your identity now",
    "bank account locked update credentials immediately",
    "team meeting is scheduled for tomorrow at 10 am",
    "please find the project report attached for review",
    "lunch meeting moved to friday afternoon",
    "monthly newsletter and product update",
]
TRAIN_LABELS = [1, 1, 1, 1, 0, 0, 0, 0]

_vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
_X = _vectorizer.fit_transform(TRAIN_TEXT)
_model = LogisticRegression(max_iter=1000, random_state=42)
_model.fit(_X, TRAIN_LABELS)

SUSPICIOUS_TERMS = [
    "urgent", "immediately", "verify", "suspended", "password",
    "credential", "confirm your identity", "account locked",
    "gift card", "wire transfer", "security alert"
]

def extract_urls(text):
    return re.findall(r"https?://[^\s<>'\"]+", text or "", flags=re.I)

def analyze_urls(text):
    indicators = []
    urls = extract_urls(text)
    details = []
    for raw in urls:
        clean = raw.rstrip(".,);]")
        parsed = urlparse(clean)
        host = (parsed.hostname or "").lower()
        flags = []
        if parsed.scheme != "https":
            flags.append("non-HTTPS URL")
        if "@" in parsed.netloc:
            flags.append("userinfo in URL")
        if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
            flags.append("IP-address host")
        if host.startswith("xn--") or ".xn--" in host:
            flags.append("punycode host")
        if len(clean) > 120:
            flags.append("unusually long URL")
        if flags:
            indicators.extend(flags)
        details.append({"url": clean, "host": host, "flags": flags})
    return urls, details, indicators

def analyze_attachments(text):
    names = re.findall(r"\b[\w.-]+\.(?:exe|scr|js|vbs|bat|cmd|msi|zip|rar)\b", text or "", re.I)
    indicators = []
    for name in names:
        ext = name.rsplit(".", 1)[-1].lower()
        indicators.append(f"risky attachment type: .{ext}")
    return names, indicators

def sender_analysis(sender):
    indicators = []
    sender = (sender or "").strip()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", sender):
        indicators.append("invalid or unusual sender format")
    if sender.count("@") == 1:
        domain = sender.split("@", 1)[1].lower()
        free_domains = {"gmail.com", "outlook.com", "yahoo.com", "hotmail.com"}
        if domain in free_domains:
            indicators.append("free-mail sender domain")
        if any(ch.isdigit() for ch in domain):
            indicators.append("numeric characters in sender domain")
    return indicators

def analyze_email(sender, subject, body):
    subject = subject or ""
    body = body or ""
    combined = f"{subject}\n{body}"
    lower = combined.lower()

    indicators = []
    matched_terms = [t for t in SUSPICIOUS_TERMS if t in lower]
    for term in matched_terms:
        indicators.append(f"suspicious language: {term}")

    urls, url_details, url_indicators = analyze_urls(combined)
    indicators.extend(url_indicators)

    attachment_names, attachment_indicators = analyze_attachments(combined)
    indicators.extend(attachment_indicators)
    indicators.extend(sender_analysis(sender))

    ml_probability = float(_model.predict_proba(_vectorizer.transform([combined]))[0][1])
    score = int(round(ml_probability * 45))
    score += min(25, len(matched_terms) * 5)
    score += min(20, len(url_indicators) * 10)
    score += min(10, len(attachment_indicators) * 10)
    score += min(10, len(sender_analysis(sender)) * 5)
    score = min(100, score)

    if score >= 70:
        level, verdict = "HIGH", "Likely phishing"
    elif score >= 40:
        level, verdict = "MEDIUM", "Suspicious — review carefully"
    else:
        level, verdict = "LOW", "No strong phishing indicators detected"

    return {
        "sender": sender,
        "subject": subject,
        "body": body,
        "risk_score": score,
        "risk_level": level,
        "verdict": verdict,
        "indicators": indicators or ["No rule-based indicators detected"],
        "urls": url_details,
        "attachments": attachment_names,
        "ml_probability": round(ml_probability * 100, 2),
        "explanation": {
            "sender": sender_analysis(sender),
            "content": [f"matched term: {x}" for x in matched_terms],
            "urls": url_indicators,
            "attachments": attachment_indicators,
        }
    }
