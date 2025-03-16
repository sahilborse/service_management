from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from models import Customer, Professional, Admin
from datetime import timedelta

login_bp = Blueprint('login_bp', __name__)

# Route for customer login
@login_bp.route('/customer', methods=['POST'])
def customer_login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request, JSON data required"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    customer = Customer.query.filter_by(username=username).first()

    if customer and check_password_hash(customer.password, password):
        session['customer_id'] = customer.id 

        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid username or password"}), 401

# Route for admin login
@login_bp.route('/admin', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request, JSON data required"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    admin = Admin.query.first()  # Get the only admin record

    if admin and admin.username == username and admin.password == password:
        session['admin_id'] = admin.id  # Store admin ID in session
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid username or password"}), 401

# Route for professional login
@login_bp.route('/professional', methods=['POST'])
def professional_login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request, JSON data required"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    professional = Professional.query.filter_by(username=username).first()

    if professional and check_password_hash(professional.password, password):
        session['professional_id'] = professional.id  # Store professional ID in session
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid username or password"}), 401

# Route for logout
@login_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

