from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return CRIPTO.hash(password)

def verificar_senha(password: str, hashed_password: str) -> bool:
    return CRIPTO.verify(password, hashed_password)
