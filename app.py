import sys
import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
from myRoutes import register_routes

# 插入当前文件目录到 sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)

try:
    # 尝试连接到 Redis 服务器
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # 测试连接
    redis_client.ping()
    print("成功连接到 Redis 服务器")
except redis.ConnectionError as e:
    print(f"无法连接到 Redis 服务器: {e}")
    # 提供更多调试信息·
    print("请确保 Redis 服务器正在运行并监听端口 6379。")
    sys.exit(1)

# 配置 Flask-Limiter
limiter = Limiter(
    app=app,  # 确保 app 是通过关键字参数传递
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["200 per day", "50 per hour"]
)

# 注册路由
register_routes(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)