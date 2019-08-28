import string
import os
import random
from hashlib import blake2b, md5

DEFAULT_RAND_STR_LEN = 10
DEFAULT_DIGEST_SIZE = 10
SECRET_KEY = b'THE_RANDOM_SECRET_KEY'


def str_2_bin(string):
    return ''.join(map(bin, bytearray(string, encoding='ascii')))


def rand_str(length=None):
    if not length:
        length = DEFAULT_RAND_STR_LEN
    letter_range = string.ascii_letters + string.digits + '_-.'
    return "".join(random.choice(letter_range) for x in range(length))


def gen_hash_key(digest_size=None):
    if not digest_size:
        digest_size = DEFAULT_DIGEST_SIZE
    key = rand_str()
    salt = os.urandom(blake2b.SALT_SIZE)
    h = blake2b(digest_size=digest_size, key=SECRET_KEY, salt=salt)
    h.update(str_2_bin(f"{key}").encode('ascii'))
    return h.hexdigest()


def hash(*keys):
    keys = list(keys)
    keys.append(SECRET_KEY)
    return md5(str_2_bin(f"{keys}").encode('ascii')).hexdigest()
