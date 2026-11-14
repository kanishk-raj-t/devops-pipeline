# Todo REST API for DevOps Pipeline 
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory list acting as our temporary data store
todos = [
    {"id": 1, "task": "Initialize DevOps pipeline", "done": True}
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Todo API is running"})

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify({"todos": todos})

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Task field is required"}), 400
    new_todo = {
        "id": len(todos) + 1,
        "task": data["task"],
        "done": False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)