import sqlite3
import time
import uuid
import json
import logging
import redis
from usertoken import redis_host, redis_port  

# 定义SQLite数据库文件名
userneed = "alarms.db"

# 配置日志记录
logging.basicConfig(filename='application.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 连接Redis
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

def verify_token(token):
    # 检查token是否存在于Redis中
    return r.exists(token)

def init_db():
    # 初始化SQLite数据库和表
    conn = sqlite3.connect(userneed)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alarms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 批量查询告警
def get_all_alarms(token):
    logging.debug("get_all_alarms called")
    # 验证token
    if not verify_token(token):
        return json.dumps({"error": "Invalid token"})
    conn = sqlite3.connect(userneed)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alarms")
    alarms = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in cursor.fetchall()]
    conn.close()
    logging.debug(f"get_all_alarms returning {alarms}")
    return json.dumps(alarms)  # 将结果转换为JSON字符串

# 精确查询告警
def get_alarm(token, alarm_id):
    logging.debug(f"get_alarm called with {alarm_id}")
    # 验证token
    if not verify_token(token):
        return json.dumps({"error": "Invalid token"})
    conn = sqlite3.connect(userneed)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alarms WHERE id = ?", (alarm_id,))
    alarm = cursor.fetchone()
    conn.close()
    if alarm:
        return json.dumps({'id': alarm[0], 'name': alarm[1], 'description': alarm[2]})
    else:
        return json.dumps({"error": "Alarm not found"})

# 添加告警
def add_alarm(token, alarm_data):
    logging.debug(f"add_alarm called with {alarm_data}")
    # 验证token
    if not verify_token(token):
        return json.dumps({"error": "Invalid token"})
    try:
        conn = sqlite3.connect(userneed)
        cursor = conn.cursor()
        # 假设 alarm_data 是一个包含 'name' 和 'description' 的字典
        cursor.execute("INSERT INTO alarms (name, description) VALUES (?, ?)", (alarm_data['name'], alarm_data['description']))
        conn.commit()
        logging.debug(f"add_alarm completed with {alarm_data}")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return json.dumps({"error": "Database error"})
    except Exception as e:
        logging.error(f"Exception in add_alarm: {e}")
        return json.dumps({"error": "An error occurred"})
    finally:
        if conn:
            conn.close()
    return json.dumps({"success": "Alarm added successfully"})

# 确保数据库和表已经创建
init_db()