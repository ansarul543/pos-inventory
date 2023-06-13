import sys
from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
import sqlite3


class BulkSetting(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/bulksetting.ui', self)
        #self.setFixedSize(849, 645)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Bulk SMS Settings")
        self.uid = uid
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.loadData()
        self.updateb.clicked.connect(self.updateData)

    def loadData(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT * FROM bulksetting WHERE id=? ",(1,))
        if(result):
            data = result.fetchone()
            self.api.setText(data[1])
            self.number.setText(data[4])
            self.username.setText(data[2])
            self.password.setText(data[3])
            if data[5]=="0":
                self.offb.setChecked(True)
            else:
                self.onb.setChecked(True)    
            self.invoice.setText(data[6])
            self.cash.setText(data[7])
            self.due.setText(data[8])
        else:
            self.close()    

    def select(self):
        if(self.offb.isChecked()):
            return "0"      
        if(self.onb.isChecked()):
            return "1"

    def updateData(self):
        api = self.api.text()
        username = self.username.text()
        password = self.password.text()
        number = self.number.text()
        auto = self.select()
        invoice = self.invoice.toPlainText()
        cash = self.cash.toPlainText()
        due = self.due.toPlainText()
        cur = self.conn.cursor()
        if(self.uid==""):
            QMessageBox.warning(None, ("Required"), 
            ("Login expired please login again after close window"),
             QMessageBox.Ok)  
        elif(api==""  and username=="" and password=="" and number==""):
            QMessageBox.warning(None, ("Required"), 
            ("Please Fill api url and username and password and number  Field"),
             QMessageBox.Ok)  
        else:    
            try:
                result = cur.execute("UPDATE bulksetting SET api=?,username=?,password=?,number=?,auto=?,invoice=?,cash=?,due=? WHERE id=?",(api,username,password,number,auto,invoice,cash,due,1,))
                self.conn.commit()
                if(result):
                    self.loadData()
                    QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
                else:
                    QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Ok)       
            except:
                QMessageBox.warning(None, ("Failed"), ("Data not updated Database Error "),QMessageBox.Ok)  
        cur.close()                                      



