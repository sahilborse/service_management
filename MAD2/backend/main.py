from flask import Flask, jsonify, request, session # Import request
from flask_session import Session
from controllers.admin_controller import admin_bp
from controllers.customer_controller import customer_bp
from controllers.professional_controller import professional_bp
from controllers.registration_controller import registration_bp
from controllers.login_controller import login_bp
from models import db, Admin
from flask_cors import CORS
from flask_migrate import Migrate
from redis import Redis
from celery import Celery

app = Flask(__name__)
migrate = Migrate(app, db)

CORS(app, supports_credentials=True)

redis_client = Redis(host='localhost', port=6379, db=0)

# Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_service.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SESSION_TYPE'] = 'filesystem'
# app.secret_key = 'your_secret_key_here'  # Change this to a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Vasu123@localhost:3306/household_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your_secret_key_here'


Session(app)
db.init_app(app)

# Initialize admin user (hardcoded)
def initialize_admin():
    with app.app_context():
        if not Admin.query.first():
            admin = Admin(username="admin", password="admin@123")  # Ensure password hashing if required
            db.session.add(admin)
            db.session.commit()
            
            


# Register blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(professional_bp, url_prefix='/professional')
app.register_blueprint(registration_bp, url_prefix='/register')
app.register_blueprint(login_bp, url_prefix='/login')

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Household Services",
        "description": "Get the best services at your doorstep with ease.",
        "login_routes": {
            "customer": "/login/customer",
            "professional": "/login/professional",
            "admin": "/login/admin"
        },
        "registration_routes": {
            "customer": "/register/customer",
            "professional": "/register/professional"
        }
    })
    
@app.route('/redis')
def get_redis_connection():
    redis_client.set('My_Message', 'Household Services Redis')
    msg = redis_client.get('My_Message').decode('utf-8')
    return jsonify({
        "message": msg
    })
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
        initialize_admin()  # Initialize admin credentials
    app.run(debug=True)
