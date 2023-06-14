import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3

class Unit(QDialog):
    def __init__(self,p='',parent=None):
        super().__init__()
        uic.loadUi('./ui/unit.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Unit")
        self.addb.clicked.connect(self.addS)
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.tableWidget.setHorizontalHeaderLabels(["ID","Unit Name"])
        self.tableWidget.setColumnWidth(1,350)
        self.loadData()
        self.searchv.textChanged.connect(self.search)
        self.deleteb.clicked.connect(self.deleteData)
        self.tableWidget.doubleClicked.connect(self.ddbclick)
        self.id =""


    def updateData(self):
        name = self.u_name.text()       
        cur = self.conn.cursor()
        if(name==""):
            QMessageBox.warning(None, ("Required"), 
            ("Name Required"),
             QMessageBox.Cancel)
        elif(self.id==""):
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data before update"),
             QMessageBox.Cancel)   
        else:    
            result = cur.execute("UPDATE unit SET unit_name=? WHERE id=?",(name,self.id,))
            self.conn.commit()
            if(result):
                self.loadData()
                self.id=""
                self.u_name.setText("")
                QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
            else:
                QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Cancel) 
        cur.close()        

    def loadData(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT * FROM unit ORDER BY id DESC")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 
        cur.close()

    def ddbclick(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        cur = self.conn.cursor()
        if(id):
            result = cur.execute("SELECT * FROM unit WHERE id=? ",(id,))
            if(result):
                data = result.fetchone()
                self.u_name.setText(data[1])
                self.id=data[0]
            cur.close()
        

    def addS(self):
        name = self.u_name.text()
        cur = self.conn.cursor()
        if(name==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Name Required"),
             QMessageBox.Cancel) 
        else:    
            if self.id=="":
                result = cur.execute("INSERT INTO unit(unit_name)VALUES(?)",(name,))
                self.conn.commit()
                if(result):
                    self.u_name.setText("")
                    QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok)  
                    self.loadData()           
                else:
                    self.loadData()
                    QMessageBox.warning(None, ("Failed"), ("Data not added "),QMessageBox.Cancel)    
                cur.close()      
            else:
                self.updateData()      
   
    def search(self):
        sv = self.searchv.text()  
        cur = self.conn.cursor()  
        result = cur.execute("SELECT * FROM unit WHERE unit_name LIKE ? ORDER BY id DESC",("%"+sv+"%",))
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 
        cur.close()

    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        cur = self.conn.cursor()
        reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row"),QMessageBox.Yes,QMessageBox.No) 
        if(reply == QMessageBox.Yes):
            result = cur.execute("DELETE FROM unit WHERE id=?",(id,))
            self.conn.commit()
            if(result):
                QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
                self.loadData()
            cur.close()    



