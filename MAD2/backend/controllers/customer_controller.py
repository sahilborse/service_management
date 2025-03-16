from flask import Blueprint, request, jsonify, session, flash, redirect, url_for
from datetime import datetime
from models import db, Customer, Service, ServiceRequest
from config.redis import redis_client

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/dashboard', methods=['GET'])
def dashboard():
    print("In customer_ dashboard !!")
    customer_id = session.get('customer_id')  # Get customer ID from session
    print("customer : ",customer_id)
    if not customer_id:
        return jsonify({"error": "Unauthorized"}), 401

    search_query = request.args.get('search', '')
    search_type = request.args.get('search_type', 'name')
    
    if search_type == 'name':
        services = Service.query.filter(Service.name.ilike(f'%{search_query}%')).all()
    elif search_type == 'location':
        services = Service.query.filter(Service.location.ilike(f'%{search_query}%')).all()
    else:
        services = Service.query.all()
    
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    
    service_requests_with_details = []
    for sr in service_requests:
        service = Service.query.get(sr.service_id)
        sr_dict = {
            "id": sr.id,
            "status": sr.status,
            "completion_date": sr.date_of_completion,
            "remarks": sr.remarks,
            "service": {
                "id": service.id,
                "name": service.name,
                "price": service.base_price,
                "location": service.location
            } if service else None
        }
        service_requests_with_details.append(sr_dict)
    
    return jsonify({
        "services": [{"id": s.id, "name": s.name, "price": s.base_price, "location": s.location} for s in services],
        "service_requests": service_requests_with_details
    })

@customer_bp.route('/request_service/<int:service_id>', methods=['POST'])
def request_service(service_id):
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({"error": "Unauthorized"}), 401

    service = Service.query.get(service_id)
   
    if service:
        redis_client.set(f"service:{service_id}:customer:{customer_id}", "Requested")
        new_request = ServiceRequest(
            service_id=service.id,
            customer_id=customer_id,
            date_of_request=datetime.now(),
            status="Requested"
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({"message": f"Service request for {service.name} created successfully!"}), 201
    return jsonify({"error": "Service not found"}), 404

@customer_bp.route('/close_request/<int:request_id>', methods=['POST'])
def close_request(request_id):
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({"error": "Unauthorized"}), 401

    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.customer_id == customer_id:
        service_request.status = "Closed"
        db.session.commit()
        return jsonify({"message": "Service request closed successfully."})
    return jsonify({"error": "Request not found or unauthorized"}), 403

@customer_bp.route('/add_remark/<int:request_id>', methods=['POST'])
def add_remark(request_id):
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({"error": "Unauthorized"}), 401

    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.customer_id == customer_id and service_request.status == "Closed":
        remark = request.json.get('remark')
        if remark:
            service_request.remarks = remark
            db.session.commit()
            return jsonify({"message": "Remark added successfully."})
        return jsonify({"error": "Please enter a valid remark."}), 400
    return jsonify({"error": "Request not found or unauthorized"}), 403

@customer_bp.route('/edit_service_request/<int:request_id>', methods=['POST'])
def edit_service_request(request_id):
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.customer_id == customer_id:
        new_service_id = request.json.get('service_id')
        new_location = request.json.get('location')
        new_price = request.json.get('price')

        new_service = Service.query.get(new_service_id)
        if new_service:
            service_request.service_id = new_service.id
            service_request.location = new_location
            service_request.service.base_price = new_price
            db.session.commit()
            return jsonify({"message": "Service request updated successfully."})
    return jsonify({"error": "Request not found or unauthorized"}), 403

@customer_bp.route('/edit_completion_date/<int:request_id>', methods=['POST'])
def edit_completion_date(request_id):
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.customer_id == customer_id:
        completion_date = request.json.get('completion_date')
        if completion_date:
            service_request.date_of_completion = datetime.strptime(completion_date, "%Y-%m-%d")
            db.session.commit()
            return jsonify({"message": "Completion date updated successfully."})
        return jsonify({"error": "Invalid completion date."}), 400
    return jsonify({"error": "Request not found or unauthorized"}), 403

@customer_bp.route('/dashboard/profile', methods=['GET'])
def profile():
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    customer = Customer.query.get(customer_id)
    if customer:
        return jsonify({
            "id": customer.id,
            "username": customer.username,
            "email": customer.email,
            "is_blocked": customer.is_blocked
        })
    return jsonify({"error": "Customer data not found"}), 404
