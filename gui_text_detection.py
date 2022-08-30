from PyQt5 import QtCore , QtGui , QtWidgets , uic

import sys

class SecondUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(SecondUI, self).__init__()
        uic.loadUi('ui_files/secondwindow.ui' , self)
        
        self.label_2 = self.findChild(QtWidgets.QLabel , 'label_2')
        self.label_3 = self.findChild(QtWidgets.QLabel , 'label_3')

        # self.show()
    
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
        
        self.show()
        
        
    def on_click(self):
        self.secondUI = SecondUI()
        self.secondUI.display_info()

if __name__ =="__main__":
    app=QtWidgets.QApplication(sys.argv)
    main = UI()
    sys.exit(app.exec_())
    