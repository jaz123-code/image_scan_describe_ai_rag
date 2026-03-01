import bcrypt
from passlib.context import CryptContext

# passlib expects `schemes` (plural) and the scheme name is 'bcrypt'
# 'deprecated' is the correct keyword for setting deprecation policy
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes[:72], salt)
    return hashed_bytes.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    try:
        return bcrypt.checkpw(password_bytes[:72], hashed_bytes)
    except ValueError:
        return False
