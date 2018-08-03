import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication,QInputDialog,QLineEdit
from PyQt5.QtGui import QIcon,QFont
 
 
class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI() 
        
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 220)  
        self.setWindowTitle('come to yuri')
        self.setWindowIcon(QIcon('test.jpg'))
        text,okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)

        QToolTip.setFont(QFont('SansSerif',0))
        self.setToolTip('This is a <b>QWidget</b> widget')
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_()) 
