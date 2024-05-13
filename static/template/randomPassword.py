import random
import string

def generate_temp_password(length=12):
    characters = string.ascii_letters + string.digits
    temp_password = ''.join(random.choice(characters) for i in range(length))
    return temp_password
