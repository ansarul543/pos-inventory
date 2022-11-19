import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3
from supplierdetails import SupplierDetails
from supplierbalance import SupplierBalance
balsup = SupplierBalance()

class SupplierLedger(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/supplierledger.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Supplier Ledger")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.supplierdue.setHorizontalHeaderLabels(["Supplier ID","Supplier Name","Contact No","Address","Due Balance"])
        self.supplierdue.setColumnWidth(3,234)

        self.suppliers.textChanged.connect(self.dueSearchSup)
        self.supplierb.clicked.connect(self.supAll)
        self.detailsb.clicked.connect(self.details)
        self.supplierdue.doubleClicked.connect(self.details)


    def details(self):
        NewInd = self.supplierdue.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        NewName = self.supplierdue.currentIndex().siblingAtColumn(1)
        name = NewName.data()
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data "),
             QMessageBox.Ok) 
        else:
            self.data = SupplierDetails(id)
            self.data.show() 


    def supAll(self):
        self.supplierDue()

    def dueSearchSup(self):
        sv = self.suppliers.text()
        if sv!="":
            result = self.cur.execute("SELECT id,name,phone,address FROM supplier WHERE id LIKE ? OR name LIKE ? OR partycode LIKE ? ",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
            result=result.fetchall()
            self.supplierdue.setRowCount(len(result))
            for index, i in enumerate(result):
                self.supplierdue.setItem(index,0,QTableWidgetItem(str(i[0])))
                self.supplierdue.setItem(index,1,QTableWidgetItem(i[1]))
                self.supplierdue.setItem(index,2,QTableWidgetItem(i[2]))
                self.supplierdue.setItem(index,3,QTableWidgetItem(i[3]))  
                bal = balsup.bal(i[0])  
                self.supplierdue.setItem(index,4,QTableWidgetItem(str(bal)))       

    def supplierDue(self):
        result = self.cur.execute("SELECT id,name,phone,address FROM supplier ")
        result=result.fetchall()
        self.supplierdue.setRowCount(len(result))
        for index, i in enumerate(result):
            self.supplierdue.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.supplierdue.setItem(index,1,QTableWidgetItem(i[1]))
            self.supplierdue.setItem(index,2,QTableWidgetItem(i[2]))
            self.supplierdue.setItem(index,3,QTableWidgetItem(i[3]))
            bal = balsup.bal(i[0])  
            self.supplierdue.setItem(index,4,QTableWidgetItem(str(bal))) 

       


