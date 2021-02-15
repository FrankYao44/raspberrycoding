

class OrderFailedException(Exception):

    def __init__(self, t):
        super.__init__(t)


class ExpandRunningException(Exception):
    def __init__(self, t):
        super.__init__(t)
