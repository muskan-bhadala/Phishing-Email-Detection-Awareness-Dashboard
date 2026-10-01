# Phishing Email Detection & Awareness Dashboard

## Overview

A local, educational cybersecurity dashboard for analyzing authorized or synthetic email content and explaining phishing-related indicators. It combines rule-based checks with a small machine-learning baseline and stores analysis history locally in SQLite.

## Problem Statement

Phishing emails commonly use urgency, credential requests, suspicious links, impersonation signals, and risky attachments. Learners need a safe environment where these indicators can be inspected without sending real email data to third-party services.

## Objectives

- Detect common phishing indicators.
- Provide an explainable risk score.
- Analyze sender, content, URLs, and attachments.
- Preserve local analysis history.
- Provide a simple awareness dashboard.
- Add automated security regression tests.

## Features

- Sender analysis
- Email content analysis
- URL analysis
- Attachment indicator analysis
- Rule-based risk scoring
- TF-IDF + Logistic Regression baseline
- Explainable detection
- Local analysis history
- JSON API
- Security headers
- Automated pytest security tests
- Responsive dashboard

## Cybersecurity Relevance

The project demonstrates defensive email analysis, secure input handling, web security headers, safe local storage, basic threat indicators, and explainability.

## Architecture

```text
Browser
   |
   v
Flask Web UI  ----->  Analyzer Service
   |                       |
   |                       +--> Sender rules
   |                       +--> Content rules
   |                       +--> URL rules
   |                       +--> Attachment rules
   |                       +--> ML baseline
   |
   +---------------> SQLite Analysis History

REST API (/api/analyze) uses the same analyzer service.
```

## Technology Stack

- Python 3.11+ recommended
- Flask
- SQLite
- scikit-learn
- pandas
- HTML5/CSS3
- pytest
- pytest-cov

## Dataset

The ML baseline uses a small **synthetic educational dataset embedded in `app/services/analyzer.py`**. It is intentionally small and is not suitable for production detection or benchmarking.

## Phishing Indicators

Examples include urgency, account suspension language, credential requests, identity verification, suspicious URL properties, and potentially risky attachment extensions.

## Sender Analysis

The sender check validates basic email structure and identifies signals such as free-mail domains and unusual domain characteristics. These are signals, not proof of maliciousness.

## Email Content Analysis

The content analyzer looks for a controlled list of common phishing-related phrases. It does not attempt to understand every possible social-engineering technique.

## URL Analysis

URLs are extracted from the message and inspected for properties including non-HTTPS schemes, IP-address hosts, punycode, embedded user information, and unusually long URLs.

## Attachment Analysis

Because this project does not need to open uploaded files, attachment analysis is represented by detecting potentially risky filename extensions in authorized/synthetic text.

## Risk Scoring

The score combines:
1. ML phishing probability.
2. Suspicious content terms.
3. URL indicators.
4. Attachment indicators.
5. Sender indicators.

The result is mapped to LOW, MEDIUM, or HIGH risk. It is an educational heuristic rather than a security verdict.

## Machine Learning

A TF-IDF vectorizer and Logistic Regression model provide a lightweight baseline. The model is trained at application startup on synthetic examples.

## Explainable Detection

Every result includes rule-based indicators and a breakdown of sender, content, URL, and attachment signals.

## Dashboard

The dashboard provides an email-analysis form, recent history, risk score, verdict, and detailed explanations.

## Security Awareness

The interface emphasizes verification of suspicious messages, careful inspection of links and attachments, and avoidance of confidential data in this educational application.

## Installation

### 1. Extract the ZIP

Extract the project, for example:

```powershell
D:\Phishing-Email-Detection-Awareness-Dashboard
```

### 2. Open the folder in VS Code

```powershell
cd D:\Phishing-Email-Detection-Awareness-Dashboard
code .
```

### 3. Create a virtual environment

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Python 3.13 is unavailable, use another supported Python 3.11+ installation.

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run tests

```powershell
pytest -q
```

Expected result: all tests pass.

### 6. Start the dashboard

```powershell
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## Usage

1. Enter an authorized/synthetic sender email.
2. Enter a subject.
3. Paste authorized/synthetic email content.
4. Click **Analyze Email**.
5. Review risk score and explainable indicators.
6. Open **Analysis History** to see previous local analyses.

### API example

```powershell
$body = @{
  sender = "security@example.com"
  subject = "URGENT verify account"
  body = "Please verify your password immediately at http://192.168.1.50/login"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:5000/api/analyze `
  -Method Post -ContentType "application/json" -Body $body
```

## API Documentation

### GET `/api/health`

Returns service status.

### POST `/api/analyze`

JSON request:

```json
{
  "sender": "user@example.com",
  "subject": "Subject",
  "body": "Email content"
}
```

The response includes risk score, risk level, verdict, indicators, URLs, attachments, ML probability, and explanation.

## Testing

Run:

```powershell
pytest -q
```

For coverage:

```powershell
pytest --cov=app --cov-report=term-missing
```

Automated security tests cover:

- Security response headers
- HTML escaping / XSS regression
- JSON handling
- SQL-injection-like input handling
- Health endpoint
- Core analyzer behavior

## Security & Privacy

- Analysis history is stored locally in SQLite.
- No email is transmitted to an external analysis service.
- Do not paste confidential, personal, or proprietary email data.
- The application uses parameterized SQLite queries.
- Flask/Jinja autoescaping is used for displayed user input.
- Security headers are added to responses.
- The ML model is a demonstration baseline.

## Results

The application produces a numeric risk score, a risk category, a verdict, and a list of explainable indicators. Results should be interpreted as educational signals rather than definitive malware/phishing judgments.

## False Positives & False Negatives

Legitimate emails may contain words such as “urgent,” “verify,” or “account,” creating false positives. Sophisticated phishing emails may avoid obvious signals, creating false negatives. The small synthetic training set also limits generalization.

## Limitations

- Small synthetic ML dataset.
- No live threat-intelligence feeds.
- No reputation service.
- No attachment sandboxing.
- No full HTML-email rendering.
- No production authentication.
- Not designed for enterprise-scale email ingestion.

## Future Improvements

- Larger curated datasets.
- Domain reputation and threat-intelligence integrations.
- HTML/DOM email analysis.
- Attachment metadata extraction in a sandbox.
- User authentication and role-based access.
- Charts and analytics for historical trends.
- Model evaluation with precision, recall, F1, ROC-AUC, and confusion matrix.
- Exportable PDF/CSV reports.

## Screenshots

Create screenshots after running the application and save them under:

```text
screenshots/
```

Recommended screenshots:

1. `01-dashboard.png` — main analysis dashboard.
2. `02-phishing-analysis.png` — high-risk sample result.
3. `03-analysis-history.png` — analysis history.
4. `04-api-health.png` — `/api/health` response.
5. `05-pytest.png` — successful automated tests.

## Learning Outcomes

- Understanding phishing indicators.
- Applying explainable rule-based detection.
- Using a basic ML text-classification pipeline.
- Designing a Flask security-analysis dashboard.
- Persisting audit/history data with SQLite.
- Writing automated security regression tests.
- Applying defensive web-security controls.

## Disclaimer

> “This project is designed for cybersecurity education and defensive analysis using synthetic or authorized data.”

## Author

**Muskan Bhadala**

Educational cybersecurity project for portfolio and academic learning.
