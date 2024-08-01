import jwt
from datetime import datetime, timedelta
from config import Config

# 生成token
def generate_token(user_id):
    # 使用jwt.encode方法生成token，其中包含user_id和过期时间
    token = jwt.encode({'user_id': user_id, 'exp': datetime.now() + timedelta(hours=6)}, Config.SECRET_KEY, algorithm="HS256")
    return token

# 验证token
def validate_token(token):
    # 解析token
    data = parse_token(token)
    # 如果解析成功且token未过期，则返回True，否则返回False
    return data is not None and data['exp'] > int(datetime.now().timestamp())
    
# 解析token
def parse_token(token):
    try:
        # 使用jwt.decode方法解析token
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return data
    except:
        # 解析失败，返回None
        return None
