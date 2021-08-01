from Cyberkernal.Expand.gui import *
from Cyberkernal.Cyberkernal import Order
import time
import sys
test_receive_list = []


#class UOrder(Order):
 #   instruction = 'test *time.' \
 #                 'if no error,no error,then save *time in *test \'s *test;' \
   #               'if no error, then save time in *test \'s *test'

 #   def __init__(self, time):
    #    super(UOrder, self).__init__(time=time)



class DOrder(Order):
    instruction = 'find those *time is *number in *test \'s *test.show *data'

def main(CYBER):
    #time.sleep(10)
    d = DOrder(key=time.time, value=1000, database='test', table='test')
    # i don't really know if this would be thread danger
    CYBER.order_list.append(d)

'''
class App(QWidget,ModelClass):


    def upload(self):
        u = UOrder(time.time)
        # i don't really know if this would be thread danger
        global CYBER
        CYBER.order_list.append(u)
        while True:
            if test_receive_list:
                o = test_receive_list[0]
                o[1].set_result(int(time.time)^2)
                break

    def download(self):

        d = DOrder()

    def _construction(self):
        self.grid = self.init_grid()

        self.group_box = self.init_group_box()
        # edit line&text
        self.belong_to = self.grid_add_Edit_line('belong_to', 10, 0, 10, 10, 1, 10)
        self.status = self.grid_add_Edit_line('status', 20, 14, 20, 14, 1, 6)
        self.status.setReadOnly(True)
        self.text = self.grid_add_Edit_text('text', 30, 0, 30, 10, 1, 10)
        self.addition = self.grid_add_Edit_text('addition', 40, 0, 40, 10, 1, 5)
        # button
        self.init_button('save', 'save all these information', 0, 0.1, fn=self.upload, shortcut='Alt+S')
        self.init_button('find_l', 'find level', 0, 0.15,
                         fn=self.download, shortcut='Alt+L')

    def __init__(self):
        super().__init__()
        self._construction()



def main():
    print('test')
    app = App()
    print('done')
    print('done')
    app.exec_()
'''

