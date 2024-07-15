import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

# private_key = os.getenv('private_key')
# public_key = os.getenv('public_key')
algorithm = os.getenv('algorithm')
access_token_expire:int = 15

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt

def load_private_key():
    with open("C:\\Users\\Тимур\\test2\\app\\certs\\jwt_private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def load_public_key():
    with open("C:\\Users\\Тимур\\test2\\app\\certs\\jwt_public.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

private_key = load_private_key()
public_key = load_public_key()

# Пример использования ключей для создания и проверки JWT токена
# def create_jwt_token():
#     payload = {"some": "data"}
#     token = jwt.encode(payload, private_key, algorithm="RS256")
#     return token
#
# def verify_jwt_token(token):
#     decoded = jwt.decode(token, public_key, algorithms=["RS256"])
#     return decoded
#
# token = create_jwt_token()
# print("JWT Token:", token)
#
# decoded_payload = verify_jwt_token(token)
# print("Decoded Payload:", decoded_payload)
a='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huIiwiZW1haWwiOiJqb2huQGdtYWlsLmNvbSIsImV4cCI6MTcyMTA0NzIyNCwiaWF0IjoxNzIxMDQ3MDQ0fQ.HXOo0MkXEEAFnvRLqWPDi0oedR0i8nzDy2MbIqWTTN1PYi4IkVJZzrGpiereAh_uS4GhRJR0vqf2wclTdGH1wKG-f0BIvotew-IXYrPv-lK14IQJtHlnOip5SofE55Nvq01ScufbSkcr7rMa-eynqE5gkEXg6YsTNAAkVeXgK4eAuT6PN1z9LydeL3Fa1Gcfg9qmq34nlTxVHMPO6hVI1MejJYMJ3muNlkKi3fJGvvgkFoQwneehE0TyHBhbYYktOtMI5JqFHjK__dimjsx2pwF6Gq5aqNtG8t9q6g7r71bbsr4dFXdAevP5qkaLEtrF5MnsHPs0MGr0FFJOJI1RQw'
b='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huIiwiZW1haWwiOiJqb2huQGdtYWlsLmNvbSIsImV4cCI6MTcyMTA0NzM1NiwiaWF0IjoxNzIxMDQ3MTc2fQ.lj-mM8BMqR_3ErS7OcFzHVl4UmL5sASscrDa3f8dUzDHKKPsf1zFFUOGaLVyl8H96D5gjh3kGM79J6KS2cLyHW0ybZDp8Z9_IYQq8jvNDGGFIYvB7uUV5msewXJQaIdRk0vbzIwTwdrQihk9GM-IlznuVXWw98KK4BkpiD5RNjDBJqSJwsCulVUHQGFJ2ocSJVWfnDy042n_SsVM5CFSzuruTTi8vq-Fxq_77w2r4m7CPN9JRWyCgWVl6eb4qlqI4kXdQJ8C1__nbm7lJ3e-99S-XnlLKNwJhSV5NqFemPkocoDPBGCKkUr7RBUf0h85cYTnlD2gmv0lIDxcEAId1A'