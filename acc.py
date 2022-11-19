import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
from accounhistory import OfficialAccount
import sqlite3

class Account(QDialog):
    def __init__(self,p='',parent=None):
        super().__init__()
        uic.loadUi('./ui/acc.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Official Acount")
        self.addb.clicked.connect(self.addS)
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.tableWidget.setHorizontalHeaderLabels(["ID","Account Name","Description","Acc Number","Balance"])
        self.tableWidget.setColumnWidth(2,260)
        self.loadData()
        self.deleteb.clicked.connect(self.deleteData)
        self.tableWidget.doubleClicked.connect(self.ddbclick)
        self.id =""
        self.updateb.clicked.connect(self.updateData)
        self.viewb.clicked.connect(self.viesh)
    
    def viesh(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(1)
        name = NewInd.data()        
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Please Select any row column"),
             QMessageBox.Cancel)
        else:
            self.data = OfficialAccount(id,name)
            self.data.show()

    def updateData(self):
        name = self.name.text()
        type = self.type.text()
        desc = self.desc.text()   
        acc = self.acc.text()
        if(name==""):
            QMessageBox.warning(None, ("Required"), 
            ("Name Required"),
             QMessageBox.Cancel)
        elif(self.id==""):
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data before update"),
             QMessageBox.Cancel)   
        else:    
            result = self.cur.execute("UPDATE account SET name=?,type=?,desc=?,accnumber=? WHERE id=?",(name,type,desc,acc,self.id,))
            self.conn.commit()
            if(result):
                self.loadData()
                self.id=""
                self.name.setText("")
                self.desc.setText("")
                self.acc.setText(" ")
                QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
            else:
                QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Cancel) 

    def loadData(self):
        result = self.cur.execute("SELECT id,name,desc,accnumber,val FROM account ORDER BY id DESC")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 
    def ddbclick(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if(id):
            result = self.cur.execute("SELECT * FROM account WHERE id=? ",(id,))
            if(result):
                data = result.fetchone()
                self.name.setText(data[1])
                self.type.setText(data[2])
                self.desc.setText(data[3])
                self.acc.setText(data[5])
                self.id=data[0]

    def addS(self):
        name = self.name.text()
        type = self.type.text()
        desc = self.desc.text()
        val = "0"
        acc = self.acc.text()
        if(name==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Name Required"),
             QMessageBox.Cancel) 
        else:    
            result = self.cur.execute("INSERT INTO account(name,type,desc,val,accnumber)VALUES(?,?,?,?,?)",(name,type,desc,val,acc,))
            self.conn.commit()
            if(result):
                self.name.setText("")
                self.desc.setText("")
                self.acc.setText("")
                QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok)  
                self.loadData()           
            else:
                self.loadData()
                QMessageBox.warning(None, ("Failed"), ("Data not added "),QMessageBox.Cancel)    
   
    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row"),QMessageBox.Yes,QMessageBox.No) 
        if(reply == QMessageBox.Yes):
            result = self.cur.execute("DELETE FROM account WHERE id=?",(id,))
            self.conn.commit()
            if(result):
                self.cur.execute("DELETE FROM cash WHERE type='Official' AND accid=?",(id,))
                self.conn.commit()
                QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
                self.loadData()



