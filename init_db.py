from models import get_db_connection
from config import Config
from utils.logger import get_logger

# 获取日志记录器
logger = get_logger(Config.APP_NAME)

def init_db():
    # 连接到MySQL服务器
    conn = get_db_connection()

    # 创建一个游标对象来执行SQL查询
    cursor = conn.cursor()

    # 如果users表不存在，则创建users表
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_users_table)

    # 如果alarm_levels表不存在，则创建alarm_levels表
    create_alarm_levels_table = """
    CREATE TABLE IF NOT EXISTS alarm_levels (
        id INT AUTO_INCREMENT PRIMARY KEY,
        level VARCHAR(255) NOT NULL,
        description TEXT NOT NULL
    )
    """
    cursor.execute(create_alarm_levels_table)

    # 提交更改
    conn.commit()

    # 打印表信息
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    logger.info(f"Tables: {tables}")

    # 关闭游标和连接
    cursor.close()
    conn.close()
    logger.info("Database initialization successful")
