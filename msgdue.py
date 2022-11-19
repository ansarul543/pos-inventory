import sys
from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
import sqlite3
import requests

from customerbalance import CustomerBalance
balcus = CustomerBalance()

class DueMessage(QDialog):
    def __init__(self,id='',parent=None):
        super().__init__()
        uic.loadUi('./ui/message.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Meassge ")
        self.cid = id
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.sentb.clicked.connect(self.sentData)
        self.smsapi()
        self.load()
        self.phones=""
        self.msg=''
        
      
    def smsapi(self):
        self.cur.execute("SELECT phone FROM customer WHERE id=?",(self.cid,))
        data = self.cur.fetchone()
        if data:
            self.phones=data[0]   
        result = self.cur.execute("SELECT * FROM bulksetting WHERE id=? ",(1,))
        if(result):
            data = result.fetchone()
            api = data[1]
            username = data[2]
            password = data[3]
            number = data[4]
            self.msg=data[8]
            url = f"{api}?username={username}&password={password}&number={number}&message=Test"
            return url
   
    def load(self):
        self.cur.execute("SELECT id,name,phone FROM customer WHERE id=?",(self.cid,))
        data = self.cur.fetchone()
        if data:
            bal = balcus.bal(data[0])
            self.phones=data[2]
            ms = f"Hi {data[1]} \nYour Due Balance {bal} Taka \n{self.msg}"
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
                             



if __name__=="__main__":
        app = QApplication(sys.argv)
        data = DueMessage()
        data.show()
        sys.exit(app.exec_())    


