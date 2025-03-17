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
# from redis import Redis
import json
import redis
from celery import Celery
# from config.redis import redis_client
app = Flask(__name__)
migrate = Migrate(app, db)

CORS(app, supports_credentials=True)

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

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
    
@app.route('/redis',methods=['GET'])
def get_redis_connection():
    # redis_client.set('my_key', 'Hello, Redis2!')
    value = redis_client.get('my_key')
    # return jsonify({
    #     "message": value
    # })
    return value
    

# @app.route('/test_redis', methods=['GET'])
# def test_redis():
#     try:
#         # Ping Redis to check connection
#         response = redis_client.ping()
#         return jsonify({"message": "Connected to Redis!", "status": response}), 200
#     except redis.ConnectionError as e:
#         return jsonify({"error": "Redis connection failed", "details": str(e)}), 500

@app.route('/get_data', methods=['GET'])
def get_data():
    # Retrieve the JSON string from Redis
    data = redis_client.get('sample_key')

    if data is None:
        return jsonify({"message": "No data found"}), 404

    # Convert JSON string back to Python dict
    data = json.loads(data)
    
    return jsonify(data), 200



@app.route('/set_data', methods=['POST'])
def set_data():
    data = request.json  # Expecting JSON in the request body

    # Convert Python dict to JSON string and store it in Redis
    redis_client.set('sample_key', json.dumps(data))

    return jsonify({"message": "Data stored successfully"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
        initialize_admin()  # Initialize admin credentials
    app.run(debug=True)
