from flask import Blueprint, request, jsonify
from models import get_db_connection
import bcrypt
from utils.limiter import create_limiter
from utils.helpers import generate_token
from utils.decorators import token_required
from utils.logger import get_logger
from config import Config

def register_auth_blueprint(app):
    limiter = create_limiter(app)
    logger = get_logger(Config.APP_NAME)
    auth_blueprint = Blueprint('auth', __name__)

    @auth_blueprint.route('/api/token', methods=['POST'])
    @limiter.limit("1 per minute")
    def get_token():
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            token = generate_token(user[0])
            logger.info(f"User {username} logged in")
            return jsonify({'token': token, 'expires_in': 21600})
        logger.error("Invalid credentials")
        return jsonify({'error': 'Invalid credentials'}), 401

    @auth_blueprint.route('/api/users/register', methods=['POST'])
    @limiter.limit("1 per minute")
    def register_user():
        data = request.get_json()
        username = data['username']
        password = data['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            conn.close()
            logger.info(f"User {username} registered")
            return jsonify({'message': 'User registered successfully'}), 201
        except:
            conn.close()
            logger.error(f"User {username} already exists")
            return jsonify({'error': 'User already exists'}), 400
        
    @auth_blueprint.route('/api/users', methods=['GET'])
    @limiter.limit("1 per minute")
    @token_required
    def get_all_users(current_user):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        logger.info(f"GET /api/users - User ID: {current_user[0]}")
        return jsonify({'total': len(users), 'users': [{'id': row[0], 'username': row[1]} for row in users]})
    
    @auth_blueprint.route('/api/users/<int:id>', methods=['GET'])
    @limiter.limit("1 per minute")
    @token_required
    def get_user(current_user, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            logger.info(f"GET /api/users/{id} - User ID: {current_user[0]}")
            return jsonify({'id': user[0], 'username': user[1]})
        logger.error(f"GET /api/users/{id} - User ID: {current_user[0]} - User not found")
        return jsonify({'error': 'User not found'}), 404
    
    @auth_blueprint.route('/api/users/<int:id>', methods=['PUT'])
    @limiter.limit("1 per minute")
    @token_required
    def update_user(current_user, id):
        data = request.get_json()
        username = data['username']
        password = data['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            logger.error(f"User with ID {id} does not exist")
            return jsonify({'error': 'User does not exist'}), 404
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", (username, hashed_password, id))
        conn.commit()
        conn.close()
        logger.info(f"PUT /api/users/{id} - User ID: {current_user[0]}")
        return jsonify({'message': 'User updated successfully'})

    @auth_blueprint.route('/api/users/<int:id>', methods=['DELETE'])
    @limiter.limit("1 per minute")
    @token_required
    def delete_user(current_user, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            logger.error(f"User with ID {id} does not exist")
            return jsonify({'error': 'User does not exist'}), 404
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        logger.info(f"DELETE /api/users/{id} - User ID: {current_user[0]}")
        return jsonify({'message': 'User deleted successfully'})

    @auth_blueprint.route('/api/users/login', methods=['POST'])
    @limiter.limit("1 per minute")
    def login_user():
        return get_token()

    @auth_blueprint.route('/api/token/validate', methods=['GET'])
    @limiter.limit("1 per minute")
    @token_required
    def validate_token(current_user):
        logger.info(f"Token validated - User ID: {current_user[0]}")
        return jsonify({'valid': True})
    
    app.register_blueprint(auth_blueprint)
