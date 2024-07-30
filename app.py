from flask import Flask
from routes.auth import register_auth_blueprint
from routes.alarm_level import register_alarm_blueprint
from config import Config
from init_db import init_db

import time

app = Flask(__name__)
app.config.from_object(Config)

register_auth_blueprint(app)
register_alarm_blueprint(app)

if __name__ == '__main__':
    while True:
        try:
            init_db()
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    app.run(debug=True, host='0.0.0.0', port=5000)
