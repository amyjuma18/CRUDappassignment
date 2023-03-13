import os
# generate the secret key
mykey = os.urandom(24).hex()
print(mykey)