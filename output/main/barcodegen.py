import sys,os
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QFileDialog, QFileDialog,QWidget,QMainWindow
import barcode 
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter,ImageFont
import sqlite3
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtGui import QPixmap,QPainter
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from reportlab.graphics import renderPM

font = ImageFont.load_default()


class Barcode(QDialog):
    def __init__(self,p='',parent=None):
        super().__init__()
        uic.loadUi('./ui/barcode.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Product Barcode")
        self.setFixedSize(800, 1000)
        self.searchp.textChanged.connect(self.searchPro)
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.pn =""
        self.number =""
        self.showb.clicked.connect(self.showBarcodes)
        #self.bars.setPixmap(QPixmap("./images/barexample.png"))
        self.printb.clicked.connect(self.print_widget)
        #self.showb.hide()
        self.businessname=""
        self.loadData()
        
    def loadData(self):
        result = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        if(result):
            data = result.fetchone()
            self.businessname=data[1]
        else:
            self.close()    

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
            result = self.cur.execute("SELECT id,name,unit,category,barcode,salerate FROM products WHERE name LIKE ? OR id LIKE ? OR barcode LIKE ? ",("%"+value+"%","%"+value+"%","%"+value+"%",))
            data = result.fetchone()
            if data:
                self.pname.setText(data[1])   
                self.unit.setText(data[2]) 
                self.category.setText(data[3])
                self.barcode.setText(data[4])
                self.pn=data[1]
                number = str(data[4])
                my_code = barcode.get('ean13', number, writer=ImageWriter())   
                my_code.save("./images/barcode") 

                self.shop_name.setText(self.businessname)
                self.proname.setText(data[1])
                self.bars1.setPixmap(QPixmap("./images/barcode.png")) 
                self.price.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_2.setText(self.businessname)
                self.proname_2.setText(data[1])
                self.bars2.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_2.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_3.setText(self.businessname)
                self.proname_3.setText(data[1])
                self.bars3.setPixmap(QPixmap("./images/barcode.png"))
                self.price_3.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_4.setText(self.businessname)
                self.proname_4.setText(data[1])
                self.bars4.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_4.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_5.setText(self.businessname)
                self.proname_5.setText(data[1])
                self.bars5.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_5.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_6.setText(self.businessname)
                self.proname_6.setText(data[1])
                self.bars6.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_6.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_7.setText(self.businessname)
                self.proname_7.setText(data[1])
                self.bars7.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_7.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)") 

                self.shop_name_8.setText(self.businessname)
                self.proname_8.setText(data[1])
                self.bars8.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_8.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_9.setText(self.businessname)
                self.proname_9.setText(data[1])
                self.bars9.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_9.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_10.setText(self.businessname)
                self.proname_10.setText(data[1])
                self.bars10.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_10.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_11.setText(self.businessname)
                self.proname_11.setText(data[1])
                self.bars11.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_11.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_12.setText(self.businessname)
                self.proname_12.setText(data[1])
                self.bars12.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_12.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_13.setText(self.businessname)
                self.proname_13.setText(data[1])
                self.bars13.setPixmap(QPixmap("./images/barcode.png"))
                self.price_13.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_14.setText(self.businessname)
                self.proname_14.setText(data[1])
                self.bars14.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_14.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_15.setText(self.businessname)
                self.proname_15.setText(data[1])
                self.bars15.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_15.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_16.setText(self.businessname)
                self.proname_16.setText(data[1])
                self.bars16.setPixmap(QPixmap("./images/barcode.png"))  
                self.price_16.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_17.setText(self.businessname)
                self.proname_17.setText(data[1])
                self.bars17.setPixmap(QPixmap("./images/barcode.png"))
                self.price_17.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_18.setText(self.businessname)
                self.proname_18.setText(data[1])
                self.bars18.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_18.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_19.setText(self.businessname)
                self.proname_19.setText(data[1])
                self.bars19.setPixmap(QPixmap("./images/barcode.png"))  
                self.price_19.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_20.setText(self.businessname)
                self.proname_20.setText(data[1])
                self.bars20.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_20.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_21.setText(self.businessname)
                self.proname_21.setText(data[1])
                self.bars21.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_21.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_22.setText(self.businessname)
                self.proname_22.setText(data[1])
                self.bars22.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_22.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")



                self.shop_name_23.setText(self.businessname)
                self.proname_23.setText(data[1])
                self.bars26.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_23.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_24.setText(self.businessname)
                self.proname_24.setText(data[1])
                self.bars27.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_24.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_25.setText(self.businessname)
                self.proname_25.setText(data[1])
                self.bars28.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_25.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_26.setText(self.businessname)
                self.proname_26.setText(data[1])
                self.bars29.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_26.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")


                self.shop_name_27.setText(self.businessname)
                self.proname_27.setText(data[1])
                self.bars31.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_27.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_28.setText(self.businessname)
                self.proname_28.setText(data[1])
                self.bars32.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_28.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_29.setText(self.businessname)
                self.proname_29.setText(data[1])
                self.bars33.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_29.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")

                self.shop_name_30.setText(self.businessname)
                self.proname_30.setText(data[1])
                self.bars34.setPixmap(QPixmap("./images/barcode.png")) 
                self.price_30.setText("TK."+f'{float(data[5]):.2f}'+"(Inc.VAT)")


                    
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
                self.shop_name.setText("")
                self.proname.setText("")
                self.price.setText("")
                self.bars1.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_2.setText("")
                self.proname_2.setText("")
                self.price_2.setText("")
                self.bars2.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_3.setText("")
                self.proname_3.setText("")
                self.price_3.setText("")                
                self.bars3.setPixmap(QPixmap("./images/barexample.png"))

                self.shop_name_4.setText("")
                self.proname_4.setText("")
                self.price_4.setText("")
                self.bars4.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_5.setText("")
                self.proname_5.setText("")
                self.price_5.setText("")
                self.bars5.setPixmap(QPixmap("./images/barexample.png"))

                self.shop_name_6.setText("")
                self.proname_6.setText("")
                self.price_6.setText("") 
                self.bars6.setPixmap(QPixmap("./images/barexample.png"))

                self.shop_name_7.setText("")
                self.proname_7.setText("")
                self.price_7.setText("") 
                self.bars7.setPixmap(QPixmap("./images/barexample.png"))  

                self.shop_name_8.setText("")
                self.proname_8.setText("")
                self.price_8.setText("")
                self.bars8.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_9.setText("")
                self.proname_9.setText("")
                self.price_9.setText("")
                self.bars9.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_10.setText("")
                self.proname_10.setText("")
                self.price_10.setText("")
                self.bars10.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_11.setText("")
                self.proname_11.setText("")
                self.price_11.setText("")
                self.bars11.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_12.setText("")
                self.proname_12.setText("")
                self.price_12.setText("")
                self.bars12.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_13.setText("")
                self.proname_13.setText("")
                self.price_13.setText("")
                self.bars13.setPixmap(QPixmap("./images/barexample.png"))

                self.shop_name_14.setText("")
                self.proname_14.setText("")
                self.price_14.setText("")
                self.bars14.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_15.setText("")
                self.proname_15.setText("")
                self.price_15.setText("")
                self.bars15.setPixmap(QPixmap("./images/barexample.png"))

                self.shop_name_16.setText("")
                self.proname_16.setText("")
                self.price_16.setText("") 
                self.bars16.setPixmap(QPixmap("./images/barexample.png"))  

                self.shop_name_17.setText("")
                self.proname_17.setText("")
                self.price_17.setText("")
                self.bars17.setPixmap(QPixmap("./images/barexample.png"))

                self.shop_name_18.setText("")
                self.proname_18.setText("")
                self.price_18.setText("")
                self.bars18.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_19.setText("")
                self.proname_19.setText("")
                self.price_19.setText("")
                self.bars19.setPixmap(QPixmap("./images/barexample.png"))  

                self.shop_name_20.setText("")
                self.proname_20.setText("")
                self.price_20.setText("")
                self.bars20.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_21.setText("")
                self.proname_21.setText("")
                self.price_21.setText("")
                self.bars21.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_22.setText("")
                self.proname_22.setText("")
                self.price_22.setText("")
                self.bars22.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_23.setText("")
                self.proname_23.setText("")
                self.price_23.setText("")
                self.bars26.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_24.setText("")
                self.proname_24.setText("")
                self.price_24.setText("")
                self.bars27.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_25.setText("")
                self.proname_25.setText("")
                self.price_25.setText("")
                self.bars28.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_26.setText("")
                self.proname_26.setText("")
                self.price_26.setText("")
                self.bars29.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_30.setText("")
                self.proname_30.setText("")
                self.price_30.setText("")
                self.bars31.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_27.setText("")
                self.proname_27.setText("")
                self.price_27.setText("")
                self.bars32.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_28.setText("")
                self.proname_28.setText("")
                self.price_28.setText("")
                self.bars33.setPixmap(QPixmap("./images/barexample.png")) 

                self.shop_name_29.setText("")
                self.proname_29.setText("")
                self.price_29.setText("")
                self.bars34.setPixmap(QPixmap("./images/barexample.png")) 

                


