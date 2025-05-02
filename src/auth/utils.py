from passlib.context import CryptContext



passwd_context = CryptContext(schemes=["bcrypt"])

def generate_passwd_hash(password: str) -> str:
    hash_pass = passwd_context.hash(password)

    return hash_pass


def verify_password(password: str, hash_pass: str) -> bool:
    return passwd_context.verify(password, hash_pass)