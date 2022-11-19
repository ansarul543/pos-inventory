import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
import sqlite3

class History(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/history.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Login and Logout History")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.tableWidget.setHorizontalHeaderLabels(["Name","User Type","Login Time","Logout Time"])
        self.tableWidget.setColumnWidth(3,250)
        self.tableWidget.setColumnWidth(4,250)
        self.loadData()
        self.uid = uid
        self.role = role
        self.deleteb.clicked.connect(self.deleteData)

    def loadData(self):
        result = self.cur.execute("SELECT users.name,users.role,loginhistory.login,loginhistory.logout FROM loginhistory INNER JOIN users  ON loginhistory.uid=users.id ORDER BY loginhistory.id DESC")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 


    def deleteData(self):
        if self.role=="Admin":
            reply = QMessageBox.question(None, ("Warning"), ("Do you want to clear all history"),QMessageBox.Yes,QMessageBox.No) 
            if(reply == QMessageBox.Yes):
                result = self.cur.execute("DELETE FROM loginhistory",)
                self.conn.commit()
                if(result):  
                    self.loadData()
                    QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
                else:
                    QMessageBox.information(None, ("Failed"), ("Data not deleted successfully"),QMessageBox.Ok)    
        else:
            QMessageBox.information(None, ("Failed"), ("Do not permission to delete without Admin"),QMessageBox.Ok)             
                
