#!/usr/bin python3
# -*- coding: utf-8 -*-

import sys
import os
import json
from threading import Thread
import requests
from PyQt5.QtWidgets import (QWidget, QToolTip, QMessageBox, QTextEdit, QLabel,
                             QPushButton, QApplication, QMainWindow, QAction,
                             QGridLayout,
                             QLineEdit, QInputDialog, QFileDialog, QCheckBox, QGroupBox)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import QSize
from config import configs
try:
    from take_picture import take_picture
except ModuleNotFoundError:
    take_picture = lambda: configs['picture']['picture_index']


PATH = os.path.abspath('.')
_IP = configs['IP']
_BPS = {}


def connector(method, **kw):
    global _IP
    rs = None
    ip = _IP + '/%s/' % method + kw['subject']

    class MyThread(Thread):
        def __init__(self, func, name=''):
            Thread.__init__(self)
            self.name = name
            self.func = func
            self.result = self.func()

        def get_result(self):
            try:
                return self.result
            except Exception as e:
                return e

    def threader(fn):
        thread_01 = MyThread(func=fn)
        thread_01.start()
        return thread_01.get_result()
    if method == 'in' or method == 'update':
        rs = threader(lambda: requests.post(ip, kw))
    elif method == 'out':
        if list(kw.keys()) == ['subject']:
            rs = threader((lambda: requests.get(ip+'/all/all')))
        else:
            ip = ip + '/%s/%s' % (list(kw.keys())[1], list(kw.values())[1])
            rs = threader((lambda: requests.get(ip)))
    elif method == 'del':
        ip = ip + '/%s' % kw['id']
        rs = threader(lambda: requests.get(ip))
    else:
        raise KeyError
    return rs


class ReactFunc(object):

    def go_blank(self):
        self.belong_to.setText('')
        self.check_box_D.setCheckState(0)
        self.check_box_C.setCheckState(0)
        self.check_box_B.setCheckState(0)
        self.check_box_A.setCheckState(0)
        self.text.setPlainText('')
        self.status.setText('')
        self.addition.setPlainText('')
        self.picture.setPixmap(self.pix_index)
        self.present_result = {'belong_to': '', 'level': 0,
                               'text': '', 'addition': ''}
        self.present_id = None
        self.image_address = None

    def check_change(self):
        try:
            try:
                self.load_result
            except:
                return
            if self.present_result != {'belong_to': self.belong_to.text(), 'level': self.level_number, 'text': self.text.toPlainText(), 'addition': self.addition.toPlainText()}:
                a = self.warn_event('warning', 'are you sure to exit without save')
                if not a:
                    try:
                        self.upd()
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)

    def check_level(self, itself, n):
        if itself.isChecked():
            self.level_number += n
        else:
            self.level_number -= n

    def choose_load_result(self, n):
        self.check_change()
        try:
            self.num += n
            self.load_result[self.num]()
        except AttributeError:
            return
        except IndexError:
            if self.num > 0:
                self.num = 0
                self.load_result[self.num]()
            elif self.num < 0:
                self.num = -1
                self.load_result[self.num]()
            else:
                self.num = 0
                self.load_result[0]()


    def save(self):
        try:
            rs = connector('in', subject=self.subject, belong_to=self.belong_to.text(),
                           level=self.level_number, text=self.text.toPlainText(),
                           addition=self.addition.toPlainText(), image_address=self.image_address)
            if rs.text == '404: Not Found' or rs.text is None or rs.text == 'wrong input':
                self.status.setText('Warning: Wrong Connection')
            else:
                self.status.setText('have saved')
        except Exception as e:
            print(e)

    def upd(self):
        try:
            rs = connector('update', subject=self.subject, id=self.present_id, belong_to=self.belong_to.text(),
                           level=self.level_number, text=self.text.toPlainText(),
                           addition=self.addition.toPlainText(), image_address=self.image_address)
            self.present_result = {'belong_to': self.belong_to.text(), 'level': self.level_number,
                                   'text': self.text.toPlainText(),
                                   'addition': self.addition.toPlainText()}
            if rs.text == '404: Not Found' or rs.text is None or rs.text == 'wrong input':
                self.status.setText('Warning: Wrong Connection')
            else:
                self.status.setText('have update')
            self.load_function(*self.present_search)
        except Exception as e:
            print(e)

    def dele(self):
        if self.warn_event('warning', 'are you sure to delete it?'):
            rs = connector('del', subject=self.subject, id=self.present_id)
            if rs.text == '404: Not Found' or rs.text is None or rs.text == 'wrong input':
                self.status.setText('Warning: Wrong Connection')
            else:
                self.status.setText('have delete')
            self.load_function(*self.present_search)

    def load_function(self, title, text, where):
        self.check_change()
        self.present_search = (title, text, where)
        result, ok = QInputDialog.getText(self, title, text)
        if result == '' and where != 'all':
            return
        if ok:
            if where == 'all':
                rs = connector('out', subject=self.subject)
            else:
                rs = connector('out', subject=self.subject, **{where: result})
            if rs.text == '404: Not Found' or rs.text is None or rs.text == 'wrong input':
                self.status.setText('Warning: Wrong Connection')
            else:
                self.status.setText('loading')
            if rs.text == '[]':
                self.status.setText('nothing found like %s = %s' % (where, result))
                return
            self.load_result = self.show_loaded(rs)
            self.num = 0
            self.load_result[0]()

    def show_loaded(self, result):
        def result_fn(rs):
            def z():
                self.belong_to.setText(rs['belong_to'])
                levels = str(bin(int(rs['level'])))[2:]
                while len(levels) < 4:
                    levels = '0' + levels
                self.check_box_D.setCheckState(0)
                self.check_box_C.setCheckState(0)
                self.check_box_B.setCheckState(0)
                self.check_box_A.setCheckState(0)
                self.level_number = 0
                self.check_box_D.setCheckState(int(levels[0])*2)
                self.check_box_C.setCheckState(int(levels[1])*2)
                self.check_box_B.setCheckState(int(levels[2])*2)
                self.check_box_A.setCheckState(int(levels[3])*2)
                self.text.setPlainText(rs['text'])
                self.addition.setPlainText(rs['addition'])
                if rs['image_address'] is not None:
                    img = QImage(rs['image_address'])
                    size = QSize(100, 100)
                    im = QPixmap.fromImage(img.scaled(size))
                    self.picture.resize(100, 100)
                    self.picture.setPixmap(QPixmap(im))
                else:
                    self.picture.setPixmap(self.pix_index)
                self.present_id = rs['id']
                self.present_result = {'belong_to': rs['belong_to'], 'level': rs['level'], 'text': rs['text'], 'addition': rs['addition']}
            return z

        result_list = []
        for rs in json.loads(result.text):
            result_list.append(result_fn(rs))
        return result_list

    def get_picture(self):
        rs = take_picture()
        self.image_address = rs
        img = QImage(rs)
        size = QSize(100, 100)
        rs = QPixmap.fromImage(img.scaled(size))
        self.picture.resize(100, 100)
        self.picture.setPixmap(QPixmap(rs))

    def check_close(self):
        self.check_change()
        self.exit()

class ModelClass(object):
    def _height_and_weight(self, i, j):
        self._desktop = QApplication.desktop()
        if 0 <= i <= 1 and 0 <= j <= 1:
            return self._desktop.width()*i, self._desktop.height()*j
        else:
            print('Warning')
            return self._desktop.width()*0.2, self._desktop.height()*0.2

    def init_frame(self, title, picture, text, h, w, x, y):

        # frame include size, title, icon, tip,
        self.setGeometry(*self._height_and_weight(x, y), *self._height_and_weight(h, w))
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(picture))
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip(text)

    def init_button(self, name, text, height, weight, grid=False, fn=None, parent=None, shortcut=None):
        if parent is None:
            parent = self
        btn = QPushButton(name, parent)
        btn.setToolTip(text)
        btn.clicked.connect(fn)
        btn.resize(btn.sizeHint())
        if shortcut is not None:
            btn.setShortcut(shortcut)
        if grid:
            self.grid.addWidget(btn, height, weight)
        else:
            btn.move(*self._height_and_weight(height, weight))
        return btn

    def init_grid(self):
        grid = QGridLayout()
        return grid

    def grid_add_Edit_line(self, title_name, x1, y1, x2, y2, w, h):

        title = QLabel(title_name)
        titleEdit = QLineEdit()
        self.grid.addWidget(title, x1, y1,)
        self.grid.addWidget(titleEdit, x2, y2, w, h)
        return titleEdit

    def grid_add_Edit_text(self, title_name, x1, y1, x2, y2, w, h):
        title = QLabel(title_name)
        titleEdit = QTextEdit()
        self.grid.addWidget(title, x1, y1,)
        self.grid.addWidget(titleEdit, x2, y2, w, h)
        return titleEdit

    def slot_btn_function(self, next_windows):
        # warning there will be a great bug here
        self.s = next_windows
        self.s.show()

    def showDialog(self, where, title, text):
        result, ok = QInputDialog.getText(self, title, text)
        if ok:
            where.setText(str(result))

    def warn_event(self, title, message):
        reply = QMessageBox.question(self, title,
                                     message, QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def exit(self):
        rs = self.warn_event('exit', 'Are you sure to exit?')
        if rs:
            self.close()

    def init_check_box(self, name, fn, height, weight, grid= None):
        cb = QCheckBox(name, self)
        cb.toggle()
        if grid:
            self.grid.addWidget(cb, height, weight)
        else:
            cb.move(*self._height_and_weight(height, weight))
        cb.stateChanged.connect(fn)
        return cb

    def init_group_box(self):
        groupBox = QGroupBox("Checkboxes")
        groupBox.setFlat(False)
        return groupBox

    def create_check_box(self, name, fn, height, weight, grid=False, set_init=False):
        check_box = QCheckBox(name)
        check_box.setChecked(set_init)
        if grid:
            self.grid.addWidget(check_box, height, weight)
        else:
            check_box.move(*self._height_and_weight(height, weight))
        check_box.stateChanged.connect(lambda: fn(check_box))
        return check_box


class BaseClass(QMainWindow, ModelClass):

    def init_main_centrals(self, name):
        self.statusBar()
        menu_bar = self.menuBar()
        menu_object = menu_bar.addMenu('&%s' % name)
        return menu_object

    def init_main_central(self, name, picture, short_cut, tip, fn, belongs):
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)
        action = QAction(QIcon(picture), name, self)
        action.setShortcut(short_cut)
        action.setStatusTip(tip)
        action.triggered.connect(fn)
        belongs.addAction(action)
        return action

    def init_tool(self, name, fn):
        toolbar = self.addToolBar(name)
        toolbar.addAction(fn)
        return toolbar

    def show_file(self, where, path):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', path)
        if file_name[0]:
            f = open(file_name[0], 'r')
            with f:
                data = f.read()
                where.setText(data)

        
class App(QWidget, ModelClass, ReactFunc):
        
    def _construction(self):
        self.grid = self.init_grid()
        self.group_box = self.init_group_box()
        # check box
        self.check_box_A = self.create_check_box('level_1', lambda itself: self.check_level(itself, 1), 20, 10, grid=True)
        self.check_box_B = self.create_check_box('level_2', lambda itself: self.check_level(itself, 2), 20, 11, grid=True)
        self.check_box_C = self.create_check_box('level_4', lambda itself: self.check_level(itself, 4), 20, 12, grid=True)
        self.check_box_D = self.create_check_box('level_8', lambda itself: self.check_level(itself, 8), 20, 13, grid=True)
        # edit line&text
        self.belong_to = self.grid_add_Edit_line('belong_to', 10, 0, 10, 10, 1, 10)
        self.status = self.grid_add_Edit_line('status', 20, 14, 20, 14, 1, 6)
        self.status.setReadOnly(True)
        self.text = self.grid_add_Edit_text('text', 30, 0, 30, 10, 1, 10)
        self.addition = self.grid_add_Edit_text('addition', 40, 0, 40, 10, 1, 5)
        # button
        self.init_button('save', 'save all these information', 0, 0.1, fn=self.save, shortcut='Alt+S')
        self.init_button('find_l', 'find level', 0, 0.15, fn=lambda: self.load_function('search', 'search level', 'level' ), shortcut='Alt+L')
        self.init_button('find_b', 'find belong_to', 0, 0.20,
                         fn=lambda: self.load_function('search', 'search belong_to', 'belong_to'), shortcut='Alt+B')
        self.init_button('find_a', 'find all', 0, 0.25,
                         fn=lambda: self.load_function('search', 'search all', 'all'), shortcut='Alt+A')
        self.init_button('update', 'update these all', 0, 0.30,
                         fn=self.upd, shortcut='Alt+U')
        self.init_button('delate', 'del this', 0, 0.35,
                         fn=self.dele, shortcut='Alt+D')
        self.init_button('go blank', 'go blank', 0, 0.45, fn=self.go_blank, shortcut='Alt+Shift+N')
        self.init_button('take_picture', 'take_picture', 0, 0.55, fn=self.get_picture, shortcut='Alt+T')
        self.init_button('last', 'last result', 0, 0.65, fn=lambda: self.choose_load_result(-1), shortcut='Alt+UP')
        self.init_button('next', 'next result', 0, 0.75, fn=lambda: self.choose_load_result(1), shortcut='Alt+DOWN')
        self.init_button('quit', 'quit', 0, 0.99, fn=self.check_close, shortcut='Alt+Shift+q')
        try:
            self.pix_index = QPixmap(configs['picture']['picture_index'])
            self.picture = QLabel(self)
            self.grid.addWidget(self.picture, 40, 15, 1, 5)
            self.picture.setPixmap(self.pix_index)
            self.picture.setScaledContents(True)
        except Exception as e:
            print(e)
        # show
        self.init_frame(self.subject, self.subject, self.subject, 1, 0.84, 0, 0.16)
        self.setLayout(self.grid)

    def __init__(self, subject):
        self.image_address = None
        self.level_number = 0
        super().__init__()
        self.subject = subject
        self._construction()


class Base(BaseClass):
    def _construction(self):
        self.statusBar().showMessage('This is GUI main interface')
        # create menu
        file_menu = self.init_main_centrals('File')
        view_menu = self.init_main_centrals('View')
        edit_menu = self.init_main_centrals('Edit')

        # create command
        exit_command = self.init_main_central('exit', configs['ico']['ico_exit'],
                                              'Alt+q', 'check me to exit', self.close, file_menu)
        Chinese_command = \
            self.init_main_central('open_Chinese',
                                   configs['ico']['ico_index'],
                                   'Alt+1', 'Chinese',
                                   lambda: self.slot_btn_function(App('Chinese')),
                                   file_menu, )
        Math_command = \
            self.init_main_central('open_Math',
                                   configs['ico']['ico_index'],
                                   'Alt+2', 'Math',
                                   lambda: self.slot_btn_function(App('Math')),
                                   file_menu, )
        English_command = \
            self.init_main_central('open_English',
                                   configs['ico']['ico_index'],
                                   'Alt+3', 'English',
                                   lambda: self.slot_btn_function(App('English')),
                                   file_menu, )
        Physics_command = \
            self.init_main_central('open_Physics',
                                   configs['ico']['ico_index'],
                                   'Alt+4', 'Physics',
                                   lambda: self.slot_btn_function(App('Physics')),
                                   file_menu, )

        Chemistry_normal_command = \
            self.init_main_central('open_chemistry_normal',
                                   configs['ico']['ico_index'],
                                   'Alt+5', 'Chemistry_normal',
                                   lambda: self.slot_btn_function(App('Chemistry_normal')),
                                   file_menu, )
        Biology_command = \
            self.init_main_central('open_Biology',
                                   configs['ico']['ico_index'],
                                   'Alt+6', 'Biology',
                                   lambda: self.slot_btn_function(App('Biology')),
                                   file_menu, )
        Chemistry_competition_command = \
            self.init_main_central('open_chemistry_competition',
                                   configs['ico']['ico_index'],
                                   'Alt+9', 'Chemistry_competition',
                                   lambda: self.slot_btn_function(App('Chemistry_competition')),
                                   file_menu, )
        Others_command = \
            self.init_main_central('open_Others',
                                   configs['ico']['ico_index'],
                                   'Alt+0', 'Others',
                                   lambda: self.slot_btn_function(App('Others')),
                                   file_menu, )
        # tool
        self.init_tool('exit', exit_command)
        self.init_tool('Chinese', Chinese_command)
        self.init_tool('Math', Math_command)
        self.init_tool('English', English_command)
        self.init_tool('Physics', Physics_command)
        self.init_tool('Chemistry_normal', Chemistry_normal_command)
        self.init_tool('Biology', Biology_command)
        self.init_tool('Chemistry_competition', Chemistry_competition_command)
        self.init_tool('Others', Others_command)
        # and show now
        self.init_frame('AtomHeart', configs['ico']['ico_index'], 'Base', 1, 1, 0, 0)
        self.show()

    def __init__(self):
        super().__init__()
        self._construction()


app = QApplication(sys.argv)
a = Base()
sys.exit(app.exec_())
