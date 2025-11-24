import os
import hashlib
from cryptography.fernet import Fernet, InvalidToken

#create a key or generate a key
_KEY = os.environ.get("SB_KEY")
if _KEY is None:
    _KEY = Fernet.generate_key().decode()
KEY = _KEY.encode()
_CIPHER = Fernet(KEY)


def encrypt_data(plaintext: str) -> str:
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")
    token = _CIPHER.encrypt(plaintext)
    return token.decode("utf-8")


def decrypt_data(token: str) -> str:
    if isinstance(token, str):
        token = token.encode("utf-8")
    try:
        plaintext = _CIPHER.decrypt(token)
        return plaintext.decode("utf-8")
    except InvalidToken as e:
        raise


def compute_audit_hash(plaintext: str, ciphertext: str) -> str:
    if not isinstance(plaintext, str):
        plaintext = str(plaintext)
    if not isinstance(ciphertext, str):
        ciphertext = str(ciphertext)
    s = plaintext + "|" + ciphertext
    return hashlib.sha256(s.encode("utf-8")).hexdigest()