from PyQt5 import QtCore , QtGui , QtWidgets , uic

import sys
from text_face_detection import *

class SecondUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(SecondUI, self).__init__()
        uic.loadUi('ui_files/secondwindow.ui' , self)
        
        self.label_2 = self.findChild(QtWidgets.QLabel , 'label_2')
        self.label_3 = self.findChild(QtWidgets.QLabel , 'label_3')
        self.pushButton_3 = self.findChild(QtWidgets.QPushButton , 'pushButton_3')
        self.pushButton = self.findChild(QtWidgets.QPushButton , 'pushButton')
        self.textEdit = self.findChild(QtWidgets.QTextEdit , 'textEdit')
        
        
        self.pushButton_3.clicked.connect(self.close_window)
        self.pushButton.clicked.connect(self.de_Identification)
        # self.show()

    def de_Identification(self):
        result_path = rectangle_detect(self.fname)
        self.qPixmapVar = QtGui.QPixmap()
        self.qPixmapVar.load(f'{result_path}.jpg')
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(500)
        
        self.label_3.setPixmap(self.qPixmapVar)
        with open(f'{result_path}.txt', 'r', encoding='UTF-8') as f:
            text = f.read()
            f.close()
        self.textEdit.setText(text)
        
    def close_window(self):
        self.close()
        
    def display_info(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image" , 'C:/apps/gui_text_detection/images','Image files(*.jpg  *.png)')
        print(fname[0])
        self.fname = fname[0]
        self.label_2.setText(self.fname)
        
        self.qPixmapVar = QtGui.QPixmap()
        self.qPixmapVar.load(fname[0])
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(500)
        
        self.label_3.setPixmap(self.qPixmapVar)
        self.show()
        
    
        
class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('ui_files/mainwindow.ui' , self)
        
        self.label_2 = self.findChild(QtWidgets.QLabel, 'label_2')
        
        self.open_btn = self.findChild(QtWidgets.QPushButton , "openButton")
        self.exit_btn = self.findChild(QtWidgets.QPushButton , "exitButton")
        
        
        self.qPixmapVar = QtGui.QPixmap()
        self.qPixmapVar.load('images/mainimage.png')
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(500)
        
        self.label_2.setPixmap(self.qPixmapVar)
        
        
        self.open_btn.clicked.connect(self.on_click)
        self.exit_btn.clicked.connect(self.close_window)
        
        self.show()
        
    def close_window(self):
        self.close()
       
    def on_click(self):
        self.secondUI = SecondUI()
        self.secondUI.display_info()

if __name__ =="__main__":
    app=QtWidgets.QApplication(sys.argv)
    main = UI()
    sys.exit(app.exec_())
    