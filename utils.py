from hashlib import sha256
import random

def encode(string):
    encoded_string = string.encode('utf-8')

    h = sha256()
    h.update(encoded_string)

    salt = str(random.random()).split(".")[1]

    return {
        "hash": h.hexdigest(),
        "salt": salt
    }