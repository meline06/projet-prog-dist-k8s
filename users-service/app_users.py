from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Melina", "role": "dev"},
    {"id": 2, "name": "Imran", "role": "admin"}
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)