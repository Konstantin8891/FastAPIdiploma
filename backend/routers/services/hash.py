from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def get_hash(string):
    return bcrypt_context.hash(string)


def verify_hash(plain_string, hashed_string):
    return bcrypt_context.verify(plain_string, hashed_string)
