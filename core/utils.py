from cryptography.fernet import Fernet
import django.conf

key = django.conf.settings.SECRET_KEY_CIPHER.encode()
cipher_suite = Fernet(key)


def encrypt_email(email: str) -> str:
    return cipher_suite.encrypt(email.encode()).decode()


def decrypt_email(encrypted_email: str) -> str:
    return cipher_suite.decrypt(encrypted_email.encode()).decode()
