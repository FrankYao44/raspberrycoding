

class Group(object):

    default_args = {'N': 40, 'p_z': 0.01, 'p_b': 0.01, 'range': (-1, 1), 'accurate': 11}

    def __init__(self, x ,y):
        self.x = x
        self.y = y

    def __sec_to_oct(self):
        self.x = self.default_args['accurate']

def select(one):

