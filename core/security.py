import bcrypt


def generate_password_hash(password: str) -> str:
    # O bcrypt precisa de bytes.
    # 1. Transformamos a string em bytes
    # 2. Geramos um "salt" (tempero de segurança)
    # 3. Criamos o hash
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(pwd_bytes, salt)

    # Retornamos como string para salvar no banco de dados
    return hash_password.decode("utf-8")


def verificar_senha(password: str, hashed_password: str) -> bool:
    # Para verificar, comparamos a senha vinda do usuário
    # com o hash que está no banco
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
