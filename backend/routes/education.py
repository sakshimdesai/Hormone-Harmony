from flask import jsonify
from utils import login_required
from data.cycle_phases import cycle_phases

@login_required
def get_phase_info(phase):
    return jsonify(cycle_phases.get(phase, {}))
