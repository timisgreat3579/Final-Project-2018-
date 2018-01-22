
import hashlib,uuid

class register(object):
    @staticmethod
    def hash_password(password):
        salt = str(uuid.uuid4().hex)
        return(hashlib.sha256(salt.encode() + str(password).encode()).hexdigest() + ':' + salt)
    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return(password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest())
