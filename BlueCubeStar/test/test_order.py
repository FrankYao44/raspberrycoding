import time
from Cyberkernal.Cyberkernal import Order


class TestOrder(Order):
    instruction = 'save %s in test\'s test ' % time.time


TestOrder()