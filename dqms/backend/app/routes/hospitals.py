from flask import Blueprint, request, jsonify
from app.models import Hospital, Token, Patient
from app import db
from datetime import datetime
from app.routes.auth import token_required

hospitals_bp = Blueprint('hospitals', __name__)

# -------- View Patient Token Requests ----------
@hospitals_bp.route('/token-requests/<int:hospital_id>', methods=['GET'])
@token_required
def token_requests(hospital_id):
    today = datetime.utcnow().date()
    tokens = Token.query.filter_by(hospital_id=hospital_id, date=today).all()
    result = []
    for t in tokens:
        patient = Patient.query.get(t.patient_id)
        result.append({
            'token_number': t.token_number,
            'patient_name': patient.name,
            'time_slot': t.time_slot,
            'slot_type': 'scheduled' if t.time_slot != 'N/A' else 'normal',
            'status': t.status
        })
    return jsonify(result), 200

# -------- Update Token Status ----------
@hospitals_bp.route("/update-token-status", methods=["POST"])
@token_required
def update_token_status():
    data = request.json
    hospital_id = data.get("hospital_id")
    token_number = data.get("token_number")
    status = data.get("status")  # "approved", "rejected", or "completed"

    today = datetime.utcnow().date()
    token = db.session.query(Token).filter_by(token_number=token_number, hospital_id=hospital_id, date=today).first()
    if not token:
        return jsonify({"message": "Token not found"}), 404

    token.status = status
    db.session.commit()

    today = datetime.utcnow().date()

    # If marking as approved and no running token, set this as in_progress
    if status == "approved":
        running_token = Token.query.filter_by(hospital_id=hospital_id, date=today, status='in_progress').first()
        if not running_token:
            token.status = 'in_progress'
            db.session.commit()

    # If marking as completed, find and mark next token as in_progress
    if status == "completed":
        # Find next token: same hospital, date, status in ('normal', 'scheduled', 'approved'), time_slot > current time_slot, order by time_slot
        next_token = Token.query.filter(
            Token.hospital_id == hospital_id,
            Token.date == today,
            Token.status.in_(['normal', 'scheduled', 'approved']),
            Token.time_slot > token.time_slot
        ).order_by(Token.time_slot).first()

        if next_token:
            next_token.status = 'in_progress'
            db.session.commit()

    return jsonify({"message": f"Token #{token_number} {status} successfully"})

# -------- Get Current Queue for Patients ----------
@hospitals_bp.route('/current-queue/<int:hospital_id>', methods=['GET'])
@token_required
def get_current_queue(hospital_id):
    today = datetime.utcnow().date()
    # Get currently running token (in_progress)
    running_token = Token.query.filter_by(hospital_id=hospital_id, date=today, status='in_progress').first()

    # Get upcoming tokens (normal or scheduled, approved, not completed, ordered by time_slot)
    upcoming_tokens = Token.query.filter(
        Token.hospital_id == hospital_id,
        Token.date == today,
        Token.status.in_(['normal', 'scheduled', 'approved'])
    ).order_by(Token.time_slot).all()

    result = {
        'running_token': {
            'token_number': running_token.token_number,
            'time_slot': running_token.time_slot
        } if running_token else None,
        'upcoming_tokens': [{
            'token_number': t.token_number,
            'time_slot': t.time_slot
        } for t in upcoming_tokens]
    }

    return jsonify(result), 200

