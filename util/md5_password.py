import hashlib


def encode_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()


def decode_md5(password):
    pass
