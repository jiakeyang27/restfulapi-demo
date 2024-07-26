from flask import jsonify, request
from service import get_all_alarms, get_alarm, add_alarm  # type: ignore
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from usertoken import get_token
# 假设 app 是在其他地方创建的 Flask 应用实例

def register_routes(app):
    # 初始化请求速率限制器
    limiter = Limiter(key_func=get_remote_address, app=app)

    # 定义获取令牌的路由
    @app.route('/api/auth/token', methods=['POST'])
    def get_token_route():
        # 从请求体中获取 id 和密码
        data = request.get_json()
        id = data.get('id')
        password = data.get('password')
        # 调用 get_token 函数验证身份并返回令牌
        return get_token(id, password)

    # 定义获取所有警报的路由
    @app.route('/alarms', methods=['GET'])
    @limiter.limit("60 per minute")  # 对该路由应用请求速率限制
    def get_all_alarms_route():
        # 从请求头中获取授权令牌
        token = request.headers.get('Authorization')
        # 调用 get_all_alarms 函数获取所有警报
        alarms = get_all_alarms(token)
        # 将警报列表转换为 JSON 格式并返回
        return jsonify(alarms)

    # 定义根据警报 ID 获取单个警报的路由
    @app.route('/alarms/<int:alarm_id>', methods=['GET'])
    @limiter.limit("60 per minute")  # 对该路由应用请求速率限制
    def get_alarm_route(alarm_id):
        # 从请求头中获取授权令牌
        token = request.headers.get('Authorization')
        # 调用 get_alarm 函数获取指定 ID 的警报
        alarm = get_alarm(token, alarm_id)
        # 将警报信息转换为 JSON 格式并返回
        return jsonify(alarm)

    # 定义添加新警报的路由
    @app.route('/alarms', methods=['POST'])
    @limiter.limit("60 per minute")  # 对该路由应用请求速率限制
    def add_alarm_route():
        # 从请求头中获取授权令牌
        token = request.headers.get('Authorization')
        # 从请求体中获取警报数据
        alarm_data = request.get_json()
        # 调用 add_alarm 函数添加新警报
        new_alarm = add_alarm(token, alarm_data)
        # 返回新添加的警报信息和状态码201，表示资源成功创建
        return jsonify(new_alarm), 201