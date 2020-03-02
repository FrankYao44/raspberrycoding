import time
import uuid
import os


configs = {
    'picture': {
        'picture_name_fn': lambda: '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex),
        'picture_address': os.path.join(os.path.abspath('.'), 'resource'),
        'picture_index': os.path.join(os.path.abspath('.'), 'resource', 'index.bmp')
    },
    'ico': {
        'ico_index': os.path.join(os.path.abspath('.'), 'resource', 'notes.ico'),
        'ico_exit': os.path.join(os.path.abspath('.'), 'resource', 'exit.ico')
    }
}
