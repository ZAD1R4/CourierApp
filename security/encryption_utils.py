from cryptography.fernet import Fernet
import base64
import os

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data: str, key: bytes) -> str:
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return encrypted.decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data.encode())
    return decrypted.decode()