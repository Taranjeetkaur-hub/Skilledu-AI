# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import json, os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # dev only — restrict origin in production

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"ok": False, "error": "Email and password required"}), 400

    users = load_users()
    if any(u.get("email") == email for u in users):
        return jsonify({"ok": False, "error": "Email already registered"}), 400

    hashed = generate_password_hash(password)  # PBKDF2
    user = {"email": email, "password_hash": hashed, "created_at": datetime.utcnow().isoformat() + "Z"}
    users.append(user)
    save_users(users)
    return jsonify({"ok": True, "message": "Registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"ok": False, "error": "Email and password required"}), 400

    users = load_users()
    user = next((u for u in users if u.get("email") == email), None)
    if not user:
        return jsonify({"ok": False, "error": "User not found"}), 404

    if not check_password_hash(user.get("password_hash", ""), password):
        return jsonify({"ok": False, "error": "Incorrect password"}), 401

    return jsonify({"ok": True, "message": "Login success"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)