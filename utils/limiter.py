from flask_limiter import Limiter
from config import Config
from flask_limiter.util import get_remote_address

# 创建一个限流器
def create_limiter(app):
    # 创建一个Limiter对象，用于限制请求的频率
    limiter = Limiter(
        # 使用get_remote_address函数获取客户端的IP地址作为限流的key
        key_func=get_remote_address,
        # 将app对象传递给Limiter对象
        app=app,
        # storage_uri="mysql://" + Config.MYSQL_USER + ":" + Config.MYSQL_PASSWORD + "@" + Config.MYSQL_HOST + "/" + Config.MYSQL_DB
    )
    # 返回创建的Limiter对象
    return limiter
