import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import redis
import secrets
import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# 定义Redis服务器的主机地址和端口号
redis_host = 'localhost'
redis_port = 6379

# 使用定义的主机地址和端口号初始化Redis客户端
redis_client = redis.Redis(host=redis_host, port=redis_port)

# MySQL数据库连接配置
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '111111',
    'database': 'userdata'
}

# 创建MySQL连接池
pool = MySQLConnectionPool(pool_name="mypool", pool_size=5, **mysql_config)

# 使用连接池连接MySQL数据库
def connect_to_mysql():
    return pool.get_connection()

# 验证用户凭据
def verify_credentials(id, password):
    # 从连接池获取连接
    cnx = connect_to_mysql()
    cursor = cnx.cursor()
    # 查询用户凭据是否匹配
    query = "SELECT COUNT(*) FROM users WHERE id = %s AND password = %s"
    cursor.execute(query, (id, password))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    # 如果匹配，生成Token
    if result[0] == 1:
        return True
    else:
        return False

# 生成Token并储存进redis中
def generate_token(id):
    # 生成一个随机的Token
    token = secrets.token_urlsafe(16)
    # 设置Token的过期时间为6小时后
    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=6)
    redis_key = f"user:{id}:token_expiration"
    # 将Token的过期时间存储到Redis中
    redis_client.set(redis_key, expiration_time.timestamp())
    # 将Token存储到Redis中
    redis_client.set(f"user:{id}:token", token)
    return token

# 获取Token
def get_token(id, password):
    # 验证用户凭据
    if verify_credentials(id, password):
        redis_key = f"user:{id}:token_expiration"
        expiration_timestamp = redis_client.get(redis_key)
        # 检查Token是否过期
        if expiration_timestamp is not None:
            expiration_time = datetime.datetime.fromtimestamp(float(expiration_timestamp))
            if expiration_time < datetime.datetime.now():
                redis_client.delete(redis_key)
                redis_client.delete(f"user:{id}:token")
                # 生成新的Token
                token = generate_token(id)
            else:
                # 获取现有的Token
                token = redis_client.get(f"user:{id}:token").decode('utf-8')
        else:
            # 生成新的Token
            token = generate_token(id)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    # 启动Flask应用
    app.run()
