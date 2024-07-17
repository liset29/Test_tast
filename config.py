import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

load_dotenv()

algorithm = os.getenv('algorithm')
access_token_expire = os.getenv('access_token_expire')

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
PORT = os.getenv('PORT')
public_path = os.getenv('public_path')
private_path = os.getenv('private_path')

def load_private_key():
    with open(f"{private_path}", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def load_public_key():
    with open(f"{public_path}", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


private_key = load_private_key()
public_key = load_public_key()
