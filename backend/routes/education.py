import json
from flask import jsonify

with open("data/cycle_phases.json", "r", encoding="utf-8") as file:
    cycle_phases = json.load(file)

def get_phase_info(phase):
    return jsonify(cycle_phases.get(phase, {}))