from flask import Blueprint, current_app, render_template, request, jsonify
from .services.analyzer import analyze_email
from .services.database import save_analysis, list_analyses

bp = Blueprint("main", __name__)

@bp.get("/")
def dashboard():
    history = list_analyses(current_app.config["DATABASE"], 20)
    return render_template("index.html", history=history)

@bp.post("/analyze")
def analyze():
    data = request.form
    result = analyze_email(
        data.get("sender", ""),
        data.get("subject", ""),
        data.get("body", "")
    )
    save_analysis(current_app.config["DATABASE"], result)
    return render_template("result.html", result=result)

@bp.get("/history")
def history():
    rows = list_analyses(current_app.config["DATABASE"], 100)
    return render_template("history.html", history=rows)

@bp.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "phishing-email-detector"})

@bp.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    result = analyze_email(
        data.get("sender", ""),
        data.get("subject", ""),
        data.get("body", "")
    )
    save_analysis(current_app.config["DATABASE"], result)
    return jsonify(result)
