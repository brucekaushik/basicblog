import hashlib

x = hashlib.md5("text")
print x # hash object
print x.hexdigest() #hash string