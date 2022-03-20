from passlib.context import CryptContext
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pswd):
    return pwd_cxt.hash(pswd)