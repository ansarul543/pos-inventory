import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3
from customerdetails import CustomerDetails
from msgdue import DueMessage
from customerbalance import CustomerBalance
balcus = CustomerBalance()

class CustomerLedger(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/customerledger.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Customer Ledger")
        self.conn = sqlite3.connect('./database/data.db')
        self.c = self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.customerdue.setHorizontalHeaderLabels(["Customer ID","Customer Name","Contact No","Address","Due Balance"])
        self.customerdue.setColumnWidth(3,234)

        self.suppliers.textChanged.connect(self.dueSearchCus)
        self.customerb.clicked.connect(self.cusAll)
        self.detailsb.clicked.connect(self.details)
        self.msgb.clicked.connect(self.messageB)
        self.customerdue.doubleClicked.connect(self.details)

    def messageB(self):
        NewInd = self.customerdue.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        NewInd = self.customerdue.currentIndex().siblingAtColumn(1)
        name = NewInd.data()        
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select customer to sent message "),
             QMessageBox.Ok) 
        else:
            self.das = DueMessage(id)
            self.das.show() 

    def details(self):
        NewInd = self.customerdue.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        NewInd = self.customerdue.currentIndex().siblingAtColumn(1)
        name = NewInd.data()        
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data "),
             QMessageBox.Ok) 
        else:
            self.da = CustomerDetails(id)
            self.da.show() 


    def cusAll(self):
        self.customerDue()

    def dueSearchCus(self):
        sv = self.suppliers.text()
        if sv!="":
            result = self.cur.execute("SELECT id,name,phone,address FROM customer WHERE id LIKE ? OR name LIKE ? OR partycode LIKE ? ",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
            result=result.fetchall()
            self.customerdue.setRowCount(len(result))
            for index, i in enumerate(result):
                self.customerdue.setItem(index,0,QTableWidgetItem(str(i[0])))
                self.customerdue.setItem(index,1,QTableWidgetItem(i[1]))
                self.customerdue.setItem(index,2,QTableWidgetItem(i[2]))
                self.customerdue.setItem(index,3,QTableWidgetItem(i[3]))  
                bal = balcus.bal(i[0])   
                self.customerdue.setItem(index,4,QTableWidgetItem(str(bal)))       

    def customerDue(self):
        result = self.cur.execute("SELECT id,name,phone,address FROM customer ")
        result=result.fetchall()
        self.customerdue.setRowCount(len(result))
        for index, i in enumerate(result):
            self.customerdue.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.customerdue.setItem(index,1,QTableWidgetItem(i[1]))
            self.customerdue.setItem(index,2,QTableWidgetItem(i[2]))
            self.customerdue.setItem(index,3,QTableWidgetItem(i[3]))
            bal = balcus.bal(i[0])   
            self.customerdue.setItem(index,4,QTableWidgetItem(str(bal))) 
 

       



