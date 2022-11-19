import sys,os
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QFileDialog, QFileDialog,QWidget,QMainWindow
import barcode 
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter
import sqlite3
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtGui import QPixmap,QPainter
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from reportlab.graphics import renderPM



class Barcode(QDialog):
    def __init__(self,p='',parent=None):
        super().__init__()
        uic.loadUi('./ui/barcode.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Product Barcode")
        self.setFixedSize(987, 700)
        self.searchp.textChanged.connect(self.searchPro)
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.pn =""
        self.number =""
        self.showb.clicked.connect(self.showBarcodes)
        #self.bars.setPixmap(QPixmap("./images/barexample.png"))
        self.printb.clicked.connect(self.print_widget)

    def print_widget(self):
        printer = QPrinter()
        painter = QPainter()
        painter.begin(printer)
        screen = self.groupBox_2.grab()
        painter.drawPixmap(10, 10, screen)
        painter.end()

    def searchPro(self):
        value = self.searchp.text()
        if value=="":
            self.pname.setText("")   
            self.unit.setText("") 
            self.category.setText("")
            self.barcode.setText("")
            self.pn=""
            self.number =""
            self.showDefaultbars()
   
        else:
            result = self.cur.execute("SELECT id,name,unit,category,barcode FROM products WHERE name LIKE ? OR id LIKE ? OR barcode LIKE ? ",("%"+value+"%","%"+value+"%","%"+value+"%",))
            data = result.fetchone()
            if data:
                self.pname.setText(data[1])   
                self.unit.setText(data[2]) 
                self.category.setText(data[3])
                self.barcode.setText(data[4])
                self.pn=data[1]
                number = str(data[4])
                my_code = barcode.get('ean13', number, writer=ImageWriter())
                my_code.save("./images/barcode",{"module_width":0.35, "module_height":10, "font_size": 18, "text_distance": 1, "quiet_zone": 2}) 
           
                self.bars1.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars2.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars3.setPixmap(QPixmap("./images/barcode.png"))
                self.bars4.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars5.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars6.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars7.setPixmap(QPixmap("./images/barcode.png"))  
                self.bars8.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars9.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars10.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars11.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars12.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars13.setPixmap(QPixmap("./images/barcode.png"))
                self.bars14.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars15.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars16.setPixmap(QPixmap("./images/barcode.png"))  
                self.bars17.setPixmap(QPixmap("./images/barcode.png"))
                self.bars18.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars19.setPixmap(QPixmap("./images/barcode.png"))  
                self.bars20.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars21.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars22.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars23.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars24.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars25.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars26.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars27.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars28.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars29.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars30.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars31.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars32.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars33.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars34.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars35.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars36.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars37.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars38.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars39.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars40.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars41.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars42.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars43.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars44.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars45.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars46.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars47.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars48.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars49.setPixmap(QPixmap("./images/barcode.png")) 
                self.bars50.setPixmap(QPixmap("./images/barcode.png")) 
                    
            else:
                self.pname.setText("")   
                self.unit.setText("") 
                self.category.setText("")
                self.barcode.setText("")
                self.pn=""
                self.number =""
                self.showDefaultbars()

    def showBarcodes(self):
        if self.pn=="":
            QMessageBox.warning(None, ("Required"), ("Product name is required Please search any product"),QMessageBox.Cancel)
        else:    
            file_name = os.path.basename('./images/barcode.png')
            name = QFileDialog.getSaveFileName(self, 'Save Image', r""+self.pn,"*.png")
            newname = os.path.basename(name[0])
            file_name=newname

            if newname!="":
                img = Image.open('./images/barcode.png')
                print(img)
                dirname = os.path.dirname(name[0])
                pathsdes = dirname+'/'+file_name
                img.save(pathsdes) 
            
            #print(os.path.splitext(file_name)[0])
            #print(pathsdes)
            #print(file_name) 
            #print(os.path.dirname(name[0]))  
            #  
    def showDefaultbars(self):
                self.bars1.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars2.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars3.setPixmap(QPixmap("./images/barexample.png"))
                self.bars4.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars5.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars6.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars7.setPixmap(QPixmap("./images/barexample.png"))  
                self.bars8.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars9.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars10.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars11.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars12.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars13.setPixmap(QPixmap("./images/barexample.png"))
                self.bars14.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars15.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars16.setPixmap(QPixmap("./images/barexample.png"))  
                self.bars17.setPixmap(QPixmap("./images/barexample.png"))
                self.bars18.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars19.setPixmap(QPixmap("./images/barexample.png"))  
                self.bars20.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars21.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars22.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars23.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars24.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars25.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars26.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars27.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars28.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars29.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars30.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars31.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars32.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars33.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars34.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars35.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars36.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars37.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars38.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars39.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars40.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars41.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars42.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars43.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars44.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars45.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars46.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars47.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars48.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars49.setPixmap(QPixmap("./images/barexample.png")) 
                self.bars50.setPixmap(QPixmap("./images/barexample.png"))                 


