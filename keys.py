import rsa
import base64
import uuid

# Function to generate RSA keys and return the public key and private key
def generate_rsa_key_pair():
    (pub_key, priv_key) = rsa.newkeys(2048)
    pub_key_pem = pub_key.save_pkcs1().decode('utf-8')
    priv_key_pem = priv_key.save_pkcs1().decode('utf-8')
    kid = str(uuid.uuid4())  # Generate a unique Key ID (kid)
    return pub_key_pem, priv_key_pem, kid

# Call the function and print the keys
if __name__ == "__main__":
    pub_key, priv_key, kid = generate_rsa_key_pair()
    print("Public Key:", pub_key)
    print("Private Key:", priv_key)
    print("Key ID (kid):", kid)

