import sys
from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
import sqlite3
import requests

class InvoiceMessage(QDialog):
    def __init__(self,id='',parent=None):
        super().__init__()
        uic.loadUi('./ui/message.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Meassge ")
        self.invoice = id
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.sentb.clicked.connect(self.sentData)
        self.smsapi()
        self.load()
        self.phones=""
        self.msg=''
        
      
    def smsapi(self):
        result1 = self.cur.execute("SELECT customer.name,customer.phone,sinvoice.paid,sinvoice.total FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id WHERE sinvoice.invoice=?",(self.invoice,))
        if result1:
            data=result1.fetchone()
            self.phones=data[1]   
        result = self.cur.execute("SELECT * FROM bulksetting WHERE id=? ",(1,))
        if(result):
            data = result.fetchone()
            api = data[1]
            username = data[2]
            password = data[3]
            number = data[4]
            self.msg=data[6]
            url = f"{api}?username={username}&password={password}&number={number}&message=Test"
            return url
   
    def load(self):
        result = self.cur.execute("SELECT customer.name,customer.phone,sinvoice.paid,sinvoice.total,sinvoice.invoice FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id WHERE sinvoice.invoice=?",(self.invoice,))
        if result:
            data=result.fetchone()
            self.phones=data[1]
            ms = f"Hi {data[0]} \nyour invoice {data[4]} amount {data[3]} Taka Paid amount {data[2]} Taka \n{self.msg}"
            self.messages.setText(ms)   

    def sentData(self):
        msg = self.messages.toPlainText()
        url = self.smsapi()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        result = self.cur.execute("SELECT id,name,phone FROM customer")
        data = result.fetchall()
       
        if msg=="":
            QMessageBox.warning(None, ("Required"), ("Message Text is required"),QMessageBox.Ok)  
        else:      
            try:
                payload  = {"number":self.phones,
                "message": f"{msg}"}
                response = requests.request("POST", url, headers=headers, data = payload)
                QMessageBox.information(None, ("Successful"), ("Message sent to customer successfully"),QMessageBox.Ok)      
            except:
                QMessageBox.warning(None, ("Failed"), ("Something Went wrong "),QMessageBox.Ok)    
                             






