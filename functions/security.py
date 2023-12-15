import hashlib
def hash(password):
    hashed = hashlib.sha3_256(password.encode()).hexdigest()
    return hashed

def login(password):

    if hash(password) == 'a00e4d3b352e9d11979549b9eef5dc951592f594488451e6cd86fdc4bce76a53':
        global wrong
        wrong = 0
        return True
    return False

