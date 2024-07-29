from flask_limiter import Limiter
from config import Config
from flask_limiter.util import get_remote_address

def create_limiter(app):
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        # storage_uri="mysql://" + Config.MYSQL_USER + ":" + Config.MYSQL_PASSWORD + "@" + Config.MYSQL_HOST + "/" + Config.MYSQL_DB
    )
    return limiter
