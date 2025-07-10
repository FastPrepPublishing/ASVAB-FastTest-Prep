from flask import Flask, request, jsonify, render_template
import json
from asvab_session_manager import asvab_sessions

app = Flask(__name__)

with open("questions_practice_full.json") as f:
    practice_data = json.load(f)

with open("questions_simulations_full.json") as f:
    simulation_data = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/practice/<section>")
def get_practice(section):
    return jsonify(practice_data.get(section.upper(), []))

@app.route("/simulation/<int:sim_id>")
def get_simulation(sim_id):
    if 0 <= sim_id < len(simulation_data):
        return jsonify(simulation_data[sim_id])
    return jsonify([])

@app.route("/session", methods=["POST"])
def manage_session():
    data = request.json
    action = data.get("action")
    user_id = data.get("user_id")
    mode = data.get("mode")
    key = data.get("key")
    if action == "start":
        return jsonify(asvab_sessions.start_session(user_id, mode, section=key if mode == "practice" else None, sim_number=key if mode == "simulation" else None))
    elif action == "save":
        return jsonify(asvab_sessions.save_answer(user_id, mode, key, data["answer"], data["correct"]))
    elif action == "get":
        return jsonify(asvab_sessions.get_session(user_id, mode, key))
    elif action == "pause":
        return jsonify(asvab_sessions.pause_session(user_id, mode, key))
    elif action == "stop":
        return jsonify(asvab_sessions.stop_session(user_id, mode, key))
    return jsonify({"error": "Invalid action"})

if __name__ == "__main__":
    app.run(debug=True)