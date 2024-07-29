import jwt
from datetime import datetime, timedelta
from config import Config

def generate_token(user_id):
    token = jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(hours=6)}, Config.SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token):
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return True
    except:
        return False
