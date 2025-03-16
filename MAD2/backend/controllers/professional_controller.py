from flask import Blueprint, session, jsonify
from models import db, Professional, ServiceRequest, Customer, Service

professional_bp = Blueprint('professional_bp', __name__)

@professional_bp.route('/dashboard')
def dashboard():
    print("IN professional Dashboard !! ")
    professional_id = session.get('professional_id')
    print("Professional ID : ", professional_id)
    
    if not professional_id:
        return jsonify({"error": "Unauthorized"}), 401
    # Fetch all service requests
    service_requests = ServiceRequest.query.all()
    service_requests_data = [
        {
            'id': request.id,
            'customer': {
                'id': request.customer.id,
                'username': request.customer.username
            } if request.customer else None,
            'professional_id': request.professional_id,
            'service': {
                'id': request.service.id,
                'name': request.service.name
            } if request.service else None,
            'status': request.status,
            'remarks': request.remarks
        } for request in service_requests
    ]
    return jsonify({"service_requests": service_requests_data})

@professional_bp.route('/accept_request/<int:request_id>', methods=['POST'])
def accept_request(request_id):
    # Fetch the service request and update it if requested
    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.status == "Requested":
        service_request.status = "Accepted"
        service_request.professional_id = session.get('professional_id')
        db.session.commit()
        return jsonify({"message": "Service request accepted successfully!"}), 200
    else:
        return jsonify({"message": "Unable to accept the service request."}), 400

@professional_bp.route('/reject_request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    # Fetch the service request and update it if requested
    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.status == "Requested":
        service_request.status = "Rejected"
        service_request.professional_id = session.get('professional_id')
        db.session.commit()
        return jsonify({"message": "Service request rejected."}), 200
    else:
        return jsonify({"message": "Unable to reject the service request."}), 400

@professional_bp.route('/close_request/<int:request_id>', methods=['POST'])
def close_request(request_id):
    # Fetch the service request and close it if the current user is the assigned professional
    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.professional_id == session.get('professional_id'):
        service_request.status = "Closed"
        db.session.commit()
        return jsonify({"message": "Service request closed successfully."}), 200
    else:
        return jsonify({"message": "You are not authorized to close this request."}), 403

# For Professional Profile
@professional_bp.route('/dashboard/profile', methods=['GET'])
def profile():
    professional_id = session.get('professional_id')
    professional = Professional.query.filter_by(id=professional_id).first()

    # Check if the professional exists
    if professional:
        professional_data = {
            'id': professional.id,
            'username': professional.username,
            'email': professional.email,
            'service_type': professional.service_type,
            'experience': professional.experience,
            'is_blocked': professional.is_blocked,
            'is_approved': professional.is_approved
        }
        return jsonify({"professional": professional_data}), 200
    else:
        return jsonify({"message": "Professional data not found"}), 404
