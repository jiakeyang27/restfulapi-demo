import mysql.connector
from config import Config

# 获取数据库连接
def get_db_connection():
    # 连接数据库
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,  # 主机名
        user=Config.MYSQL_USER,  # 用户名
        password=Config.MYSQL_PASSWORD,  # 密码
        database=Config.MYSQL_DB  # 数据库名
    )
    return connection  # 返回数据库连接
