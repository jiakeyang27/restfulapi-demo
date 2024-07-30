from flask import request, jsonify
from functools import wraps
import jwt
from config import Config
from models import get_db_connection
from utils.logger import get_logger

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logger = get_logger(Config.APP_NAME)
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            logger.error('Token is missing!')
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s", (data['user_id'],))
            current_user = cursor.fetchone()
        except:
            logger.error('Token is invalid!')
            return jsonify({'error': 'Token is invalid!'}), 401
        logger.info(f"Token validated - User ID: {current_user[0]}")
        return f(current_user, *args, **kwargs)
    return decorated
