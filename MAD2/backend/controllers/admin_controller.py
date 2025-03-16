from flask import Blueprint, request, jsonify, session
from models import db, Customer, Professional, Service, ServiceRequest, Admin
from flask_login import current_user

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    customers = db.session.get(Customer, session.get("customers")) or Customer.query.all()
    professionals = db.session.get(Professional, session.get("professionals")) or Professional.query.all()
    services = db.session.get(Service, session.get("services")) or Service.query.all()
    service_requests = db.session.get(ServiceRequest, session.get("service_requests")) or ServiceRequest.query.all()

    customers_data = [
        {
            "id": c.id,
            "username": c.username,
            "email": c.email,
            "is_blocked": c.is_blocked,
        }
        for c in customers
    ]

    professionals_data = [
        {
            "id": p.id,
            "username": p.username,
            "email": p.email,
            "service_type": p.service_type,
            "experience": p.experience,
            "is_blocked": p.is_blocked,
            "is_approved": p.is_approved,
        }
        for p in professionals
    ]

    services_data = [
        {
            "id": s.id,
            "name": s.name,
            "base_price": s.base_price,
            "location": s.location,
        }
        for s in services
    ]

    customer_requests = {}
    for request in service_requests:
        request_data = {
            "id": request.id,
            "service": {"id": request.service.id, "name": request.service.name},
            "date_of_request": request.date_of_request.strftime("%Y-%m-%d"),
        }
        if request.customer_id not in customer_requests:
            customer_requests[request.customer_id] = []
        customer_requests[request.customer_id].append(request_data)

    return jsonify(
        {
            "customers": customers_data,
            "professionals": professionals_data,
            "services": services_data,
            "customer_requests": customer_requests,
        }
    )

@admin_bp.route("/block_customer/<int:id>", methods=["POST"])
def block_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    customer.is_blocked = True
    db.session.commit()
    return jsonify({"message": f"Customer {customer.username} has been blocked", "status": "blocked"})

@admin_bp.route("/unblock_customer/<int:id>", methods=["POST"])
def unblock_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    customer.is_blocked = False
    db.session.commit()
    return jsonify({"message": f"Customer {customer.username} has been unblocked", "status": "unblocked"})

@admin_bp.route("/approve_professional/<int:id>", methods=["POST"])
def approve_professional(id):
    professional = db.session.get(Professional, id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    professional.is_approved = True
    db.session.commit()
    return jsonify({"message": f"Professional {professional.username} has been approved", "status": "approved"})

@admin_bp.route("/block_professional/<int:id>", methods=["POST"])
def block_professional(id):
    professional = db.session.get(Professional, id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    professional.is_blocked = True
    db.session.commit()
    return jsonify({"message": f"Professional {professional.username} has been blocked", "status": "blocked"})

@admin_bp.route("/unblock_professional/<int:id>", methods=["POST"])
def unblock_professional(id):
    professional = db.session.get(Professional, id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    professional.is_blocked = False
    db.session.commit()
    return jsonify({"message": f"Professional {professional.username} has been unblocked", "status": "unblocked"})

@admin_bp.route("/create_service", methods=["POST"])
def create_service():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("base_price") or not data.get("location"):
        return jsonify({"message": "Missing required fields"}), 400

    new_service = Service(
        name=data["name"],
        base_price=data["base_price"],
        location=data["location"]
    )

    db.session.add(new_service)
    db.session.commit()

    return jsonify({"message": "Service created successfully", "service": {
        "id": new_service.id,
        "name": new_service.name,
        "base_price": new_service.base_price,
        "location": new_service.location
    }}), 201

@admin_bp.route("/edit_service/<int:id>", methods=['PUT'])
def edit_service(id):
    service = db.session.get(Service, id)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    data = request.get_json()
    
    if not data or not data.get("name") or not data.get("base_price") or not data.get("location"):
        return jsonify({"message": "Missing required fields"}), 400

    service.name = data["name"]
    service.base_price = data["base_price"]
    service.location = data["location"]

    db.session.commit()

    return jsonify({"message": "Service updated successfully", "service": {
        "id": service.id,
        "name": service.name,
        "base_price": service.base_price,
        "location": service.location
    }}), 200

@admin_bp.route("/delete_service/<int:id>", methods=["DELETE"])
def delete_service(id):
    service = db.session.get(Service, id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully", "service_id": id})

@admin_bp.route('/dashboard/profile', methods=['GET'])
def profile():
    admin = db.session.get(Admin, session.get("admin_id")) or Admin.query.first()
    
    if admin:
        return jsonify({
            "id": admin.id,
            "username": admin.username,
            "password": admin.password  # Add more fields if necessary
        })
    else:
        return jsonify({"error": "Admin data not found"}), 404
