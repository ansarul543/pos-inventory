import sys
from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
import sqlite3
import requests

class Extramessage(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/extramessage.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Meassge ")
        self.uid = uid
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.sentb.clicked.connect(self.sentData)
        self.allb.clicked.connect(self.select)
        self.oneb.clicked.connect(self.select)
        self.sv.textChanged.connect(self.searchCustomer)
        self.smsapi()


    def searchCustomer(self):
        value = self.sv.text()
        result = self.cur.execute("SELECT * FROM customer WHERE name LIKE ? OR id LIKE ? ",("%"+value+"%","%"+value+"%",))
        data = result.fetchone()
        if data:
            self.cn.setText(data[1])
            self.mobile.setText(data[3])
        else:
            self.cn.setText("")  
            self.mobile.setText("") 

    def smsapi(self):
        result = self.cur.execute("SELECT * FROM bulksetting WHERE id=? ",(1,))
        if(result):
            data = result.fetchone()
            api = data[1]
            username = data[2]
            password = data[3]
            number = data[4]
            url = f"{api}?username={username}&password={password}&number={number}&message=Test"
            return url
  

    def select(self):
        if(self.allb.isChecked()):
            self.groupBox.hide()
            return "all"      
        if(self.oneb.isChecked()):
            self.groupBox.show()
            return "one"

    def sentData(self):
        name = self.cn.text()
        phone = self.mobile.text()
        checkcustomer = self.select()
        msg = self.msg.toPlainText()
        url = self.smsapi()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if checkcustomer=="all":
            result = self.cur.execute("SELECT id,name,phone FROM customer")
            data = result.fetchall()
            if msg=="" :
                QMessageBox.warning(None, ("Required"), ("Message Text is required"),QMessageBox.Ok)  
            else:      
                try:
                    for index,i in enumerate(data):
                        names = i[1]
                        payload  = {"number":i[2],
                            "message": f" Hi {names}, \n {msg}"}
                        response = requests.request("POST", url, headers=headers, data = payload)
                    QMessageBox.information(None, ("Successful"), ("Message sent to customer successfully"),QMessageBox.Ok)      
                except:
                    QMessageBox.warning(None, ("Failed"), ("Something Went wrong "),QMessageBox.Ok)    
        else:   
            if phone=="":
                QMessageBox.warning(None, ("Required"), ("Number is required"),QMessageBox.Ok) 
            elif msg=="" :
                QMessageBox.warning(None, ("Required"), ("Message Text is required"),QMessageBox.Ok)  
            else:      
                try:
                    payload  = {"number":phone,
                       "message": f" Hi {name}, \n {msg}"}
                    response = requests.request("POST", url, headers=headers, data = payload)   
                    QMessageBox.information(None, ("Successful"), ("Message sent to customer successfully"),QMessageBox.Ok)      
                except:
                    QMessageBox.warning(None, ("Failed"), ("Something Went wrong "),QMessageBox.Ok)                                



