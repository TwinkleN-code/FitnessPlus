from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_private_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())    
    return private_key

def generate_public_key(private_key):
    return private_key.public_key()

#save private key to a file
def save_private_key(private_key):
    #serialize 
    serial_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
    )
    try:
        with open('private_key.pem', 'wb') as f: 
            f.write(serial_private)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def save_public_key(public_key):
    #serialize
    serial_pub = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    try:
        with open('public_key.pem', 'wb') as f: 
            f.write(serial_pub)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 


#read private key
def read_private_key():
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

#read public key
def read_public_key():
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

#encrypt
def encrypt(message, public_key):
    message = message.encode('utf-8')
    return public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

#decrypt
def decrypt(encrypted_message, private_key):
    decrypt = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    return decrypt.decode('utf-8')

