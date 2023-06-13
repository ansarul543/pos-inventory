import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import random
import sqlite3

from supplierbalance import SupplierBalance
balsup = SupplierBalance()

class QuickPurchase(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/quickpurchase.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Purchase Without Products")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.invoice.setText(str(random.randint(10000, 100000)))
        date = QDate.currentDate()
        self.dateEdit.setDate(date)        
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.total.setValidator(self.onlynumber)  
        self.paid.setValidator(self.onlynumber)  
        self.total.setAlignment(QtCore.Qt.AlignRight)
        self.paid.setAlignment(QtCore.Qt.AlignRight)
        self.sv.textChanged.connect(self.searchSupplier)
        self.saveb.clicked.connect(self.saveData)
        self.uid=uid     
        self.sid="" 

    def saveData(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')
        sid = self.sid
        invoice = self.invoice.text()
        date_current = self.dateEdit.date() 
        date = date_current.toString("yyyy-MM-dd")
        dateandtime = date+" "+currenttime
        paid = self.paid.text()  
        total = self.total.text()  
        previousdue = self.previousdue.text()
        cur = self.conn.cursor()
        if sid=="" and self.sn.text()=="":
            QMessageBox.warning(None, ("Required"), 
            ("Supplier Name is Required"),
             QMessageBox.Ok)
        elif invoice=="":
            QMessageBox.warning(None, ("Required"), 
            ("Invoice number not be empty . please fill "),
             QMessageBox.Ok)             
        elif paid=="" or total=="":
            QMessageBox.warning(None, ("All 0 field is Required"), 
            ("All 0 Zero field not be empty minimum 0 is required"),
             QMessageBox.Ok)   
        else:
            query = (sid,total,invoice,paid,dateandtime,self.uid,previousdue,)
            result = cur.execute("INSERT INTO pinvoice(sid,total,invoice,paid,date,uid,previus_due)VALUES(?,?,?,?,?,?,?)",query)
            self.conn.commit()     
            if result:
                id = result.lastrowid
                cur.execute("INSERT INTO ppp(type,invoice_id,sid,date,uid)VALUES(?,?,?,?,?)",("PURCHASE",id,sid,dateandtime,self.uid,))
                self.conn.commit()
                QMessageBox.information(None, ("Successful"), ("Data added and saved successfully"),QMessageBox.Ok) 
                self.total.setText("0")
                self.paid.setText("0")
                self.sid=""
                self.sn.setText("")
                self.previousdue.setText("")
                self.invoice.setText(str(random.randint(10000, 100000)))
            else:
                QMessageBox.warning(None, ("Failed"), ("Data not saved"),QMessageBox.Ok)       
        cur.close()                     
                                      

    def searchSupplier(self):
        value = self.sv.text()
        cur = self.conn.cursor()
        if value!="":
            result = cur.execute("SELECT * FROM supplier WHERE name LIKE ? OR id LIKE ? OR partycode LIKE ? ",("%"+value+"%","%"+value+"%","%"+value+"%",))
            data = result.fetchone()
            if data:
                self.sn.setText(data[1])
                self.sid = data[0]
                bal = balsup.bal(data[0])
                self.previousdue.setText(str(bal))
            else:
                self.sn.setText("")  
                self.sid =""  
                self.previousdue.setText("0")
        else:
            self.sn.setText("")  
            self.sid =""  
            self.previousdue.setText("0")  
        cur.close()    




  


