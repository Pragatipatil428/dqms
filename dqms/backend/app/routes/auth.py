from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Patient, Hospital
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

# -------- Patient Signup ----------
@auth_bp.route('/patient/signup', methods=['POST'])
def patient_signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if Patient.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    hashed_pw = generate_password_hash(password)
    new_patient = Patient(name=name, email=email, password=hashed_pw)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient registered successfully'}), 201

# -------- Patient Login ----------
@auth_bp.route('/patient/login', methods=['POST'])
def patient_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    patient = Patient.query.filter_by(email=email).first()
    if not patient or not check_password_hash(patient.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': patient.id,
        'role': 'patient',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'message': 'Login successful', 'token': token, 'user': {'id': patient.id, 'name': patient.name, 'email': patient.email}}), 200

# -------- Hospital Signup ----------
@auth_bp.route('/hospital/signup', methods=['POST'])
def hospital_signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if Hospital.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    hashed_pw = generate_password_hash(password)
    new_hospital = Hospital(name=name, email=email, password=hashed_pw)
    db.session.add(new_hospital)
    db.session.commit()

    return jsonify({'message': 'Hospital registered successfully'}), 201

# -------- Hospital Login ----------
@auth_bp.route('/hospital/login', methods=['POST'])
def hospital_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    hospital = Hospital.query.filter_by(email=email).first()
    if not hospital or not check_password_hash(hospital.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': hospital.id,
        'role': 'hospital',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'message': 'Login successful', 'token': token, 'user': {'id': hospital.id, 'name': hospital.name, 'email': hospital.email}}), 200

# -------- JWT Verification Decorator --------
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1]  # Bearer <token>
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data['user_id']
            request.user_role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated
