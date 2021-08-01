#!/usr/bin python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import (QWidget, QToolTip, QMessageBox, QTextEdit, QLabel,
                             QPushButton, QApplication, QMainWindow, QAction,
                             QGridLayout,
                             QLineEdit, QInputDialog, QFileDialog, QCheckBox, QGroupBox)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import QSize


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

        
