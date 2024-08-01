from flask import Blueprint, request, jsonify
from models import get_db_connection
import bcrypt
from utils.limiter import create_limiter
from utils.helpers import generate_token
from utils.decorators import token_required
from utils.logger import get_logger
from config import Config

# 定义一个注册认证蓝图函数
def register_auth_blueprint(app):
    # 创建一个限流器
    limiter = create_limiter(app)
    # 获取日志记录器
    logger = get_logger(Config.APP_NAME)
    # 创建一个认证蓝图
    auth_blueprint = Blueprint('auth', __name__)

    # 定义获取token的路由
    @auth_blueprint.route('/api/token', methods=['POST'])
    # 限制每分钟只能请求一次
    @limiter.limit("1 per minute")
    def get_token():
        # 获取请求的json数据
        data = request.get_json()
        # 获取用户名和密码
        username = data['username']
        password = data['password']
        
        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        # 查询用户名是否存在
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        # 如果用户存在且密码正确，则生成token
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            token = generate_token(user[0])
            logger.info(f"User {username} logged in")
            return jsonify({'token': token, 'expires_in': 21600})
        logger.error("Invalid credentials")
        return jsonify({'error': 'Invalid credentials'}), 401

    # 定义注册用户的路由
    @auth_blueprint.route('/api/users/register', methods=['POST'])
    # 限制每分钟只能请求一次
    @limiter.limit("1 per minute")
    def register_user():
        # 获取请求的json数据
        data = request.get_json()
        # 获取用户名和密码
        username = data['username']
        password = data['password']
        # 对密码进行加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # 插入用户数据
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            conn.close()
            logger.info(f"User {username} registered")
            return jsonify({'message': 'User registered successfully'}), 201
        except:
            conn.close()
            logger.error(f"User {username} already exists")
            return jsonify({'error': 'User already exists'}), 400

    # 定义登录用户的路由
    @auth_blueprint.route('/api/users/login', methods=['POST'])
    # 限制每分钟只能请求一次
    @limiter.limit("1 per minute")
    def login_user():
        # 调用获取token的路由
        return get_token()

    # 定义验证token的路由
    @auth_blueprint.route('/api/token/validate', methods=['GET'])
    # 限制每分钟只能请求一次
    @limiter.limit("1 per minute")
    # 验证token的装饰器
    @token_required
    def validate_token(current_user):
        logger.info(f"Token validated - User ID: {current_user[0]}")
        return jsonify({'valid': True})
    
    # 注册认证蓝图到app中
    app.register_blueprint(auth_blueprint)