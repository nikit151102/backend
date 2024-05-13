import jwt 

import secrets

secret_key = "1e9cb1ff6950647229010fb1af7d932ba0e33f15688c59dd2e6252ab4a7e96e9"

def generateSecretKey():
    secret_key = secrets.token_hex(32)
    print(secret_key)


def generateToken(payload):
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print(token)
    return token

def decryptToken(token):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Token has expired
        print("Token has expired.")
    except jwt.InvalidTokenError:
        # Invalid token
        print("Invalid token.")
    except Exception as e:
        print(f"An error occurred: {e}")
