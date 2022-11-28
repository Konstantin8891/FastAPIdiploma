from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_pass, hashed_pass):
    return bcrypt_context.verify(plain_pass, hashed_pass)
