import hashlib
md5A=hashlib.md5()
md5B=hashlib.md5()
md5A.update('hello md5'.encode('utf-8'))
print(md5A.hexdigest())
md5B.update('hello md5'.encode('utf-8'))
md5B.update('hello md5'.encode('utf-8'))
print(md5B.hexdigest())

def add_salt(passage):
    r=hashlib.md5()
    r.update((passage+'the salt').encode('utf-8'))
    return r.hexdigest()

r=add_salt('YX2544762897blue')
print(r)
