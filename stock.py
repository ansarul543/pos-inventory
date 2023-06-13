import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from productledger import ProductLedger
import sqlite3

class Stocks(QDialog):
    def __init__(self,id='',type='',parent=None):
        super().__init__()
        uic.loadUi('./ui/stock.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Stock Reports")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.tableWidget.setHorizontalHeaderLabels(["ID","Product Name","Category","Stock Quantity","Purchase Rate","Sales Rate","Wholesale","Total Amount"])
        self.tableWidget2.setHorizontalHeaderLabels(["ID","Product Name","Category","Stock Quantity","Purchase Rate","Sales Rate","Wholesale","Re Order Qtn"])
        self.searchv.textChanged.connect(self.search)
        self.reloadall.clicked.connect(self.allb)
        self.categoryData()
        self.proData()
        self.loadData2()
        self.category.currentTextChanged.connect(self.catChange)
        self.product.currentTextChanged.connect(self.proChange)
        self.ledgerb.clicked.connect(self.details)
        self.tableWidget.doubleClicked.connect(self.details)

    def details(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(1)
        name = NewInd.data()        
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data "),
             QMessageBox.Ok) 
        else:
            self.da = ProductLedger(id)
            self.da.show() 

    def catChange(self):
        sv = self.category.currentText()
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,name,category,unit,CAST(qtn as DOUBLE) as qtn,buyrate,salerate,wholesale,reorder FROM products WHERE name LIKE ? OR id LIKE ? OR category LIKE ? OR unit LIKE ? ORDER BY qtn DESC",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        result=result.fetchall()
        self.tableWidget.setRowCount(len(result))
        value = 0
        whole =0
        retail=0
        for index, i in enumerate(result):
            total = float(i[4]) * float(i[5])
            value+=float(total)
            wholes = float(i[4]) * float(i[7])
            whole+=wholes
            retails = float(i[4]) * float(i[6])
            retail+=retails
            self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(str(i[4]) +" "+ str(i[3])))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[5]))
            self.tableWidget.setItem(index,5,QTableWidgetItem(i[6]))
            self.tableWidget.setItem(index,6,QTableWidgetItem(i[7]))
            self.tableWidget.setItem(index,7,QTableWidgetItem(str(total)))
            if float(i[4])<=float(i[8]):
                self.tableWidget.item(index, 3).setBackground(QtGui.QColor(255, 200, 192))
            else:
                self.tableWidget.item(index, 3).setBackground(QtGui.QColor(184, 234, 238))               
        self.total.setText(str(value))  
        self.wholesale.setText(str(whole )) 
        self.retail.setText(str(retail ))
        cur.close()

    def proChange(self):
        sv = self.product.currentText()
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,name,category,unit,CAST(qtn as DOUBLE) as qtn,buyrate,salerate,wholesale,reorder FROM products WHERE name LIKE ? OR id LIKE ? OR category LIKE ? OR unit LIKE ? ORDER BY qtn DESC",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        result=result.fetchall()
        self.tableWidget.setRowCount(len(result))
        value = 0
        whole =0
        retail=0
        for index, i in enumerate(result):
            total = float(i[4]) * float(i[5])
            value+=float(total)
            wholes = float(i[4]) * float(i[7])
            whole+=wholes
            retails = float(i[4]) * float(i[6])
            retail+=retails
            self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(str(i[4]) +" "+ str(i[3])))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[5]))
            self.tableWidget.setItem(index,5,QTableWidgetItem(i[6]))
            self.tableWidget.setItem(index,6,QTableWidgetItem(i[7]))
            self.tableWidget.setItem(index,7,QTableWidgetItem(str(total)))
            if float(i[4])<=float(i[8]):
                self.tableWidget.item(index, 3).setBackground(QtGui.QColor(255, 200, 192))
            else:
                self.tableWidget.item(index, 3).setBackground(QtGui.QColor(184, 234, 238))               
        self.total.setText(str(value))  
        self.wholesale.setText(str(whole )) 
        self.retail.setText(str(retail )) 
        cur.close()

    def categoryData(self):
        cur = self.conn.cursor()
        data = cur.execute("SELECT * FROM category")
        result = data.fetchall()
        for i in result:
            self.category.addItem(i[1])
        cur.close()  

    def proData(self):
        cur = self.conn.cursor()
        data = cur.execute("SELECT * FROM products")
        result = data.fetchall()       
        for i in result:
            self.product.addItem(i[1])
        cur.close()    

    def allb(self):
        self.loadData()

    def loadData2(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,name,category,unit,CAST(qtn as DOUBLE) as qtn,buyrate,salerate,wholesale,CAST(reorder as DOUBLE) as reorder FROM products WHERE CAST(reorder as DOUBLE)>=CAST(qtn as DOUBLE) OR qtn='0.0' ORDER BY qtn asc  ")
        result=result.fetchall()
        length = len(result)
        self.tableWidget2.setRowCount(length)
        for index, i in enumerate(result):
            qtn = float(i[4])
            reqtn = float(i[8])
            self.tableWidget2.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.tableWidget2.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget2.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget2.setItem(index,3,QTableWidgetItem(str(i[4]) +" "+ str(i[3])))
            self.tableWidget2.setItem(index,4,QTableWidgetItem(i[5]))
            self.tableWidget2.setItem(index,5,QTableWidgetItem(i[6]))
            self.tableWidget2.setItem(index,6,QTableWidgetItem(i[7]))
            self.tableWidget2.setItem(index,7,QTableWidgetItem(str(i[8]) +" "+ str(i[3])))
            self.tableWidget2.item(index, 3).setBackground(QtGui.QColor(255, 200, 192))
            self.tableWidget2.item(index, 7).setBackground(QtGui.QColor(184, 234, 238))

        cur.close()
           

    def loadData(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,name,category,unit,CAST(qtn as DOUBLE) as qtn,buyrate,salerate,wholesale,reorder FROM products ORDER BY qtn DESC")
        result=result.fetchall()
        self.tableWidget.setRowCount(len(result))
        value = 0
        whole =0
        retail=0
        for index, i in enumerate(result):
            total = float(i[4]) * float(i[5])
            value+=float(total)
            wholes = float(i[4]) * float(i[7])
            whole+=wholes
            retails = float(i[4]) * float(i[6])
            retail+=retails
            self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(str(i[4]) +" "+ str(i[3])))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[5]))
            self.tableWidget.setItem(index,5,QTableWidgetItem(i[6]))
            self.tableWidget.setItem(index,6,QTableWidgetItem(i[7]))
            self.tableWidget.setItem(index,7,QTableWidgetItem(str(total)))
            if float(i[4])<=float(i[8]):
                self.tableWidget.item(index, 3).setBackground(QtGui.QColor(255, 200, 192))
            else:
                self.tableWidget.item(index, 3).setBackground(QtGui.QColor(184, 234, 238))            

        self.total.setText(str(value))  
        self.wholesale.setText(str(whole )) 
        self.retail.setText(str(retail ))
        cur.close()


    def search(self):
        sv = self.searchv.text()    
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,name,category,unit,CAST(qtn as DOUBLE) as qtn,buyrate,salerate,wholesale,reorder FROM products WHERE name LIKE ? OR id LIKE ? OR category LIKE ? OR unit LIKE ? ORDER BY qtn DESC",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        result=result.fetchall()
        self.tableWidget.setRowCount(len(result))
        value = 0
        whole =0
        retail=0
        for index, i in enumerate(result):
            total = float(i[4]) * float(i[5])
            value+=float(total)
            wholes = float(i[4]) * float(i[7])
            whole+=wholes
            retails = float(i[4]) * float(i[6])
            retail+=retails
            self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(str(i[4]) +" "+ str(i[3])))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[5]))
            self.tableWidget.setItem(index,5,QTableWidgetItem(i[6]))
            self.tableWidget.setItem(index,6,QTableWidgetItem(i[7]))
            self.tableWidget.setItem(index,7,QTableWidgetItem(str(total)))
            if float(i[4])<=float(i[8]):
                self.tableWidget.item(index, 3).setBackground(QtGui.QColor(255, 200, 192))
            else:
                self.tableWidget.item(index, 3).setBackground(QtGui.QColor(184, 234, 238))               
        self.total.setText(str(value))  
        self.wholesale.setText(str(whole )) 
        self.retail.setText(str(retail )) 
        cur.close()


