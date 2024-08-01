from flask import request, jsonify
from functools import wraps
from config import Config
from models import get_db_connection
from utils.logger import get_logger
from utils.helpers import parse_token, validate_token

# 定义一个装饰器，用于验证token
def token_required(f):
    # 使用wraps装饰器，保留原函数的元信息
    @wraps(f)
    def decorated(*args, **kwargs):
        # 获取logger
        logger = get_logger(Config.APP_NAME)
        # 获取token
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        # 如果没有token，返回错误信息
        if not token:
            logger.error('Token is missing!')
            return jsonify({'error': 'Token is missing!'}), 401
        # 验证token
        try:
            assert validate_token(token) is True
            # 解析token
            data = parse_token(token)
            # 获取数据库连接
            conn = get_db_connection()
            cursor = conn.cursor()
            # 查询用户信息
            cursor.execute("SELECT * FROM users WHERE id = %s", (data['user_id'],))
            current_user = cursor.fetchone()
        except:
            # 如果token无效，返回错误信息
            logger.error('Token is invalid!')
            return jsonify({'error': 'Token is invalid!'}), 401
        # 记录日志
        logger.info(f"Token validated - User ID: {current_user[0]}")
        # 返回原函数，并传入当前用户信息
        return f(current_user, *args, **kwargs)
    # 返回装饰后的函数
    return decorated