from flask import Blueprint, request, jsonify
from models import db, Customer, Professional
from werkzeug.security import generate_password_hash

registration_bp = Blueprint('registration_bp', __name__)

@registration_bp.route('/customer', methods=['POST'])
def register_customer():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request data"}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    new_customer = Customer(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )
    
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Customer registered successfully!", "redirect": "/customer/dashboard"}), 201

@registration_bp.route('/professional', methods=['POST'])
def register_professional():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request data"}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    service_type = data.get('service_type')
    experience = data.get('experience')

    if not username or not email or not password or not service_type or experience is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        experience = int(experience)
    except ValueError:
        return jsonify({"error": "Invalid experience value"}), 400
    
    new_professional = Professional(
        username=username,
        email=email,
        password=generate_password_hash(password),
        service_type=service_type,
        experience=experience
    )
    
    db.session.add(new_professional)
    db.session.commit()

    return jsonify({"message": "Professional registered successfully!", "redirect": "/professional/dashboard"}), 201
