from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def hashing_password(password):
    return pwd_context.hash(password)


def verify_password(input_password, hashed_password):
    return pwd_context.verify(input_password, hashed_password)
