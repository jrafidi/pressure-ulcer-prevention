from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode 
import os

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = bs - (len(chunk) % bs)
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            if padding_length < 1 or padding_length > bs:
               raise ValueError("bad decrypt pad (%d)" % padding_length)
            # all the pad-bytes must be the same
            if chunk[-padding_length:] != (padding_length * chr(padding_length)):
               # this is similar to the bad decrypt:evp_enc.c from openssl program
               raise ValueError("bad decrypt")
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)

def encrypt_RSA(public_key_loc, message):
    '''
    param: public_key_loc Path to public key
    param: message String to be encrypted
    return base64 encoded encrypted string
    '''
    key = open(public_key_loc, "r").read()
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = rsakey.encrypt(message)
    return encrypted.encode('base64')

def decrypt_RSA(private_key_loc, package):
    '''
    param: public_key_loc Path to your private key
    param: package String to be decrypted
    return decrypted string
    '''
    key = open(private_key_loc, "r").read() 
    rsakey = RSA.importKey(key) 
    rsakey = PKCS1_OAEP.new(rsakey) 
    decrypted = rsakey.decrypt(b64decode(package)) 
    return decrypted

def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    new_key = RSA.generate(bits, e=65537) 
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 
    return private_key, public_key

if __name__ == '__main__':
    # Generate AES password
    aes_password = os.urandom(32)

    # AES encrypt the file from test to test2
    with open('test.txt', 'rb') as in_file, open('test2.txt', 'wb') as out_file:
        encrypt(in_file, out_file, aes_password)
    # RSA encrypt the key
    encoded_password = encrypt_RSA('public_key.pem', aes_password)

    # RSA decrypt the key
    decoded_password = decrypt_RSA('private_key.pem', encoded_password)
    # AES decrypt the file from test2 to test3
    with open('test2.txt', 'rb') as in_file, open('test3.txt', 'wb') as out_file:
        decrypt(in_file, out_file, decoded_password)