from flask import Blueprint, request, jsonify
from models import get_db_connection
from utils.decorators import token_required
from utils.limiter import create_limiter
from utils.logger import get_logger
from config import Config

# 注册报警级别蓝图
def register_alarm_blueprint(app):
    # 创建限流器
    limiter = create_limiter(app)
    # 获取日志记录器
    logger = get_logger(Config.APP_NAME)
    # 创建报警级别蓝图
    alarm_levels_blueprint = Blueprint('alarm_levels', __name__)

   # 获取所有报警级别
    @alarm_levels_blueprint.route('/api/alarm-levels', methods=['GET'])
   # 需要token验证
    @token_required
   # 限制每分钟只能访问一次
    @limiter.limit("1 per minute")
    def get_all_alarm_levels(current_user):
       conn = None
       cursor = None
       try:
            # 获取数据库连接
        conn = get_db_connection()
        cursor = conn.cursor()
        # 查询报警级别表
        cursor.execute("SELECT * FROM alarm_levels")
        alarm_levels = cursor.fetchall()
        
        # 记录日志
        logger.info(f"GET /api/alarm-levels - User ID: {current_user[0]}")
        # 返回报警级别列表
        return jsonify({'total': len(alarm_levels), 'alarm_levels': [{'id': row[0], 'level': row[1], 'description': row[2]} for row in alarm_levels]})
       except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({'error': 'An error occurred while fetching alarm levels'}), 500
       finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    
    
    # 获取指定id的报警级别
    @alarm_levels_blueprint.route('/api/alarm-levels/<int:id>', methods=['GET'])
    # 需要token验证
    @token_required
    # 限制每分钟只能访问一次
    @limiter.limit("1 per minute")
    def get_alarm_level(current_user, id):
      conn = None
      cursor = None
      try:
          # 获取数据库连接
         conn = get_db_connection()
         cursor = conn.cursor()
        # 查询指定id的报警级别
         cursor.execute("SELECT * FROM alarm_levels WHERE id = %s", (id,))
         alarm_level = cursor.fetchone()
        
         if alarm_level:
            # 记录日志
            logger.info(f"GET /api/alarm-levels/{id} - User ID: {current_user[0]}")
            # 返回报警级别
            return jsonify({'id': alarm_level[0], 'level': alarm_level[1], 'description': alarm_level[2]})
         else:
            # 记录错误日志
            logger.error(f"GET /api/alarm-levels/{id} - User ID: {current_user[0]} - Alarm level not found")
            # 返回错误信息
            return jsonify({'error': 'Alarm level not found'}), 404
      except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({'error': 'An error occurred while fetching the alarm level'}), 500
      finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    
    
    # 添加报警级别
    @alarm_levels_blueprint.route('/api/alarm-levels', methods=['POST'])
    # 需要token验证
    @token_required
    # 限制每分钟只能访问一次
    @limiter.limit("1 per minute")
    def add_alarm_level(current_user):
      conn = None
      cursor = None
      try:
        # 获取请求数据
        data = request.get_json()
        level = data['level']
        description = data['description']
        
        # 获取数据库连接
        conn = get_db_connection()
        cursor = conn.cursor()
        # 插入报警级别
        cursor.execute("INSERT INTO alarm_levels (level, description) VALUES (%s, %s)", (level, description))
        conn.commit()
        
        # 记录日志
        logger.info(f"POST /api/alarm-levels - User ID: {current_user[0]} - Level: {level}")
        # 返回报警级别
        return jsonify({'id': cursor.lastrowid, 'level': level, 'description': description}), 201
      except Exception as e:
        logger.error(f"Error occurred: {e}")
        if conn:
            conn.rollback()
        return jsonify({'error': 'An error occurred while adding the alarm level'}), 500
      finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    # 注册报警级别蓝图
    app.register_blueprint(alarm_levels_blueprint)
