from flask import Flask, jsonify, send_from_directory
import json

app = Flask(__name__, static_folder='static')

with open('questions_practice.json') as f:
    practice_questions = json.load(f)

with open('questions_simulations.json') as f:
    simulation_questions = json.load(f)

@app.route('/')
def root():
    return send_from_directory('static', 'index.html')

@app.route('/api/practice/<section>')
def get_practice(section):
    if section in practice_questions:
        return jsonify(practice_questions[section])
    return jsonify([])

@app.route('/api/simulation/<int:sim_number>')
def get_simulation(sim_number):
    if 0 <= sim_number < len(simulation_questions):
        return jsonify(simulation_questions[sim_number])
    return jsonify([])

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
