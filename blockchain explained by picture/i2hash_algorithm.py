import hashlib    
import random


def sha(pw,salt):                     
    pw_bytes = pw.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    # print('len=', len(hashlib.sha256(pw_bytes + salt_bytes).hexdigest()))
    return hashlib.sha256(pw_bytes + salt_bytes).hexdigest() 

def add_validation_to_sn(source, salt='1@2#3%4^'):
    sha_str = sha(source, salt)    
    return sha_str 

source = 'py创世模块demo开始了'
r = add_validation_to_sn(source)
print(r)