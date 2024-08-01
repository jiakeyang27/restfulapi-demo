from flask import Flask
from routes.auth import register_auth_blueprint
from routes.alarm_level import register_alarm_blueprint
from config import Config
from init_db import init_db

import time

# 创建Flask应用
app = Flask(__name__)
# 从Config类中加载配置
app.config.from_object(Config)

# 注册auth蓝图
register_auth_blueprint(app)
# 注册alarm_level蓝图
register_alarm_blueprint(app)

# 如果是主程序
if __name__ == '__main__':
    # 无限循环，直到数据库初始化成功
    while True:
        try:
            # 初始化数据库
            init_db()
            # 跳出循环
            break
        except Exception as e:
            # 打印错误信息
            print('Database initialization failed. Retrying in 1 second...')
            # 等待1秒
            time.sleep(1)
    # 运行Flask应用，开启调试模式，设置主机和端口
    app.run(debug=True, host=Config.APP_HOST, port=5000)
