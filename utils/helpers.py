import jwt
from datetime import datetime, timedelta
from config import Config

def generate_token(user_id):
    token = jwt.encode({'user_id': user_id, 'exp': datetime.now() + timedelta(hours=6)}, Config.SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token):
    data = parse_token(token)
    return data is not None and data['exp'] > int(datetime.now().timestamp())
    
def parse_token(token):
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return data
    except:
        return None
