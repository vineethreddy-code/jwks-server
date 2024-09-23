from flask import Flask, jsonify, request
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

app = Flask(__name__)

private_key = rsa.generate_private_key(public_exponent=65537, 
key_size=2048)
public_key = private_key.public_key()

kid = "24cbbe9b-321e-48bb-a0d4-c3980c92fe74"

@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEOM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return jsonify({
        "keys": [{
            "kid": kid,
            "kty": "RSA",
            "n": public_key_bytes.split('\n')[1:-1],
            "e": "AQAB"
        }]
    })

@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired', default='false', 
type=str).lower() == 'true'
    # Your logic to generate JWT here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

