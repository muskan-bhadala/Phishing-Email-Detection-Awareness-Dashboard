# Project Documentation

## Folder Structure

```text
Phishing-Email-Detection-Awareness-Dashboard/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── services/
│   │   ├── analyzer.py
│   │   └── database.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── result.html
│       └── history.html
├── data/
│   └── sample_emails.txt
├── screenshots/
├── tests/
│   ├── conftest.py
│   ├── test_analyzer.py
│   └── test_security.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Requested Completion Items

### Implement analysis history
Implemented using SQLite in `app/services/database.py`. Every successful analysis is saved and displayed on `/history` and on the dashboard.

### Add automated security tests
Implemented in `tests/test_security.py`. The suite checks security headers, XSS escaping, SQL-injection-like input handling, malformed JSON behavior, and the health endpoint.

### Complete README and documentation
Implemented in `README.md` and this document, including installation, architecture, API, testing, security/privacy, limitations, future improvements, screenshots, learning outcomes, and disclaimer.
