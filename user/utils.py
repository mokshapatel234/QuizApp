import jwt
from datetime import datetime, timedelta

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  
    }

    jwt_token_bytes = jwt.encode(payload, 'secret', algorithm='HS256')
    jwt_token_str = jwt_token_bytes.decode('utf-8')  # Convert bytes to string

    return jwt_token_str