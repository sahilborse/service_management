from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # For password security

db = SQLAlchemy()

class Admin(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Admin {self.username}>'
    
    def get_id(self):
        return str(self.id)

class Customer(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)

    # Flask-Login required methods and properties
    @property
    def is_active(self):
        """All customers are active unless explicitly blocked."""
        return not self.is_blocked

    def get_id(self):
        """Return the unique ID of the user."""
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Customer {self.username}>'

class Professional(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    service_type = db.Column(db.String(80), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)

    # Flask-Login required methods and properties
    @property
    def is_active(self):
        """All professionals are active unless explicitly blocked."""
        return not self.is_blocked

    def get_id(self):
        """Return the unique ID of the user."""
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Professional {self.username}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Service {self.name}>'

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="Requested")
    remarks = db.Column(db.String(255), nullable=True)
    
    # Add a relationship to the Service model
    service = db.relationship('Service', backref='requests')
    customer = db.relationship('Customer', backref='requests')

    def __repr__(self):
        return f'<ServiceRequest {self.id} - Status: {self.status}>'
