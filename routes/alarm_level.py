from flask import Blueprint, request, jsonify
from models import get_db_connection
from utils.decorators import token_required
from utils.limiter import create_limiter
from utils.logger import get_logger
from config import Config

def register_alarm_blueprint(app):
    limiter = create_limiter(app)
    logger = get_logger(Config.APP_NAME)
    alarm_levels_blueprint = Blueprint('alarm_levels', __name__)

    @alarm_levels_blueprint.route('/api/alarm-levels', methods=['GET'])
    @token_required
    @limiter.limit("1 per minute")
    def get_all_alarm_levels(current_user):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alarm_levels")
        alarm_levels = cursor.fetchall()
        conn.close()
        logger.info(f"GET /api/alarm-levels - User ID: {current_user[0]}")
        return jsonify({'total': len(alarm_levels), 'alarm_levels': [{'id': row[0], 'level': row[1], 'description': row[2]} for row in alarm_levels]})

    @alarm_levels_blueprint.route('/api/alarm-levels/<int:id>', methods=['GET'])
    @token_required
    @limiter.limit("1 per minute")
    def get_alarm_level(current_user, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alarm_levels WHERE id = %s", (id,))
        alarm_level = cursor.fetchone()
        conn.close()
        if alarm_level:
            logger.info(f"GET /api/alarm-levels/{id} - User ID: {current_user[0]}")
            return jsonify({'id': alarm_level[0], 'level': alarm_level[1], 'description': alarm_level[2]})
        logger.error(f"GET /api/alarm-levels/{id} - User ID: {current_user[0]} - Alarm level not found")
        return jsonify({'error': 'Alarm level not found'}), 404

    @alarm_levels_blueprint.route('/api/alarm-levels', methods=['POST'])
    @token_required
    @limiter.limit("1 per minute")
    def add_alarm_level(current_user):
        data = request.get_json()
        level = data['level']
        description = data['description']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alarm_levels (level, description) VALUES (%s, %s)", (level, description))
        conn.commit()
        conn.close()
        logger.info(f"POST /api/alarm-levels - User ID: {current_user[0]} - Level: {level}")
        return jsonify({'id': cursor.lastrowid, 'level': level, 'description': description}), 201

    app.register_blueprint(alarm_levels_blueprint)
