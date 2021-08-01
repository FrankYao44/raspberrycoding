import time
import uuid
import os
import hashlib


def password(_time, salt):
    s = _time // 100000
    sha1 = hashlib.sha1()
    sha2 = hashlib.sha1()
    sha1.update(str(s - 1).encode('utf-8') + salt.encode('utf-8'))
    sha2.update(str(s).encode('utf-8') + salt.encode('utf-8'))
    return '%s,%s' % (sha1.hexdigest(), sha2.hexdigest())


configs = {
    'IP': 'http://127.0.0.1:8000/atomheart',
    'init_IP': 'http://127.0.0.1:8000/atomheart/init/'
               '%s' % (password(time.time(), '1')),
    'picture': {
        'picture_name_fn': lambda: '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex),
        'picture_address': os.path.join(os.path.abspath(''), 'resource'),
        'picture_index': os.path.join(os.path.abspath(''), 'resource', 'index.bmp')
    },
    'ico': {
        'ico_index': os.path.join(os.path.abspath(''), 'resource', 'notes.ico'),
        'ico_exit': os.path.join(os.path.abspath(''), 'resource', 'exit.ico')
    },
    'safety': {
        'salt': '1'
    }
}
