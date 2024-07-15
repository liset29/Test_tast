import jwt


def encode_jwt(payload: dict,
               private_key,
               algorithm):
    encoded = jwt.encode(payload,private_key,algorithm)
    return encoded


def decode_jwt(token,
               public_key,
               algorithm):
    decoded = jwt.decode(token, public_key, algorithm=[algorithm])
    return decoded
