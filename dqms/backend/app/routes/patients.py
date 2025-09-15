from flask import Blueprint, request, jsonify
from app.models import Patient, Hospital, Token
from app import db
from datetime import datetime
from app.routes.auth import token_required

patients_bp = Blueprint('patients', __name__)

# -------- View Hospitals ----------
@patients_bp.route('/hospitals', methods=['GET'])
@token_required
def get_hospitals():
    hospitals = Hospital.query.all()
    result = []
    for h in hospitals:
        result.append({
            'id': h.id,
            'name': h.name,
            'email': h.email
        })
    return jsonify(result), 200

# -------- Request Token ----------
@patients_bp.route('/request-token', methods=['POST'])
@token_required
def request_token():
    data = request.json
    patient_id = data.get('patient_id')
    hospital_id = data.get('hospital_id')
    slot_type = data.get('slot_type')  # "normal" or "scheduled"
    preferred_time = data.get('preferred_time')  # optional for scheduled

    def calculate_time_slot(token_number):
        # Tokens 1 to 42, starting at 10:00 AM, 10-minute intervals, 1 hour break from 1:00 PM to 2:00 PM
        start_hour = 10
        start_minute = 0
        slots_before_break = 18  # 10:00 to 12:50 (18 slots)
        break_duration = 60  # 1 hour break in minutes

        if token_number < 1 or token_number > 42:
            return None

        if token_number <= slots_before_break:
            total_minutes = (token_number - 1) * 10
        else:
            # After break, add break duration
            total_minutes = (slots_before_break * 10) + break_duration + ((token_number - slots_before_break - 1) * 10)

        hour = start_hour + (total_minutes // 60)
        minute = start_minute + (total_minutes % 60)
        return f"{hour:02d}:{minute:02d}"

    # Fetch hospital tokens for today
    today = datetime.utcnow().date()
    hospital_tokens_today = Token.query.filter_by(hospital_id=hospital_id, date=today).all()

    # Collect occupied time slots
    occupied_slots = set(t.time_slot for t in hospital_tokens_today)

    if slot_type == "normal":
        # Find next available token_number from 1 to 42 whose time_slot is not occupied
        next_token = None
        for token_num in range(1, 43):
            slot = calculate_time_slot(token_num)
            if slot not in occupied_slots:
                next_token = token_num
                time_slot = slot
                break
        if next_token is None:
            return jsonify({'message': 'All slots are already allotted.'}), 400
    else:
        # Scheduled token
        if preferred_time:
            # Extract time part if it's a datetime string
            if 'T' in preferred_time:
                preferred_time = preferred_time.split('T')[1][:5]  # e.g., "14:30"
            if preferred_time in occupied_slots:
                return jsonify({'message': 'Already Allotted'}), 400
            # Find token_number for preferred_time
            next_token = None
            for token_num in range(1, 43):
                if calculate_time_slot(token_num) == preferred_time:
                    next_token = token_num
                    break
            if next_token is None:
                return jsonify({'message': 'Invalid preferred time'}), 400
            time_slot = preferred_time
        else:
            # Find next available token_number from 1 to 42 whose time_slot is not occupied
            next_token = None
            for token_num in range(1, 43):
                slot = calculate_time_slot(token_num)
                if slot not in occupied_slots:
                    next_token = token_num
                    time_slot = slot
                    break
            if next_token is None:
                return jsonify({'message': 'All slots are already allotted.'}), 400

    # Create token
    token = Token(
        token_number=next_token,
        date=today,
        time_slot=time_slot,
        patient_id=patient_id,
        hospital_id=hospital_id,
        status=slot_type
    )
    db.session.add(token)
    db.session.commit()

    return jsonify({
        'message': 'Token booked successfully',
        'token_number': token.token_number,
        'time_slot': token.time_slot
    }), 201

# -------- Get My Tokens ----------
@patients_bp.route('/my-tokens', methods=['GET'])
@token_required
def get_my_tokens():
    patient_id = request.user_id
    tokens = Token.query.filter_by(patient_id=patient_id).all()
    result = []
    for t in tokens:
        hospital = Hospital.query.get(t.hospital_id)
        result.append({
            'token_number': t.token_number,
            'hospital_name': hospital.name,
            'time_slot': t.time_slot,
            'slot_type': t.status,
            'status': t.status,
            'date': t.date.isoformat(),
            'hospital_id': t.hospital_id
        })
    return jsonify(result), 200
