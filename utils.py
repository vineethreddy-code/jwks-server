import os
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

KEYS_DIR = './keys/'

def generate_rsa_key(kid, expiry_minutes=60):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(f'{KEYS_DIR}{kid}_private.pem', 'wb') as private_file:
        private_file.write(private_key_pem)
    with open(f'{KEYS_DIR}{kid}_public.pem', 'wb') as public_file:
        public_file.write(public_key_pem)
    expiry_time = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    return kid, expiry_time

def create_jwt(kid, payload):
    with open(f'{KEYS_DIR}{kid}_private.pem', 'rb') as private_file:
        private_key = private_file.read()
    token = jwt.encode(payload, private_key, algorithm='RS256', 
headers={"kid": kid})
    return token

def verify_jwt(token):
    kid = jwt.get_unverified_header(token)['kid']
    with open(f'{KEYS_DIR}{kid}_public.pem', 'rb') as public_file:
        public_key = public_file.read()
    try:
        decoded = jwt.decode(token, public_key, algorithms=['RS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return 'Signature has expired.'
    except jwt.InvalidTokenError:
        return 'Invalid token.'

