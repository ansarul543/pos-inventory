import sys
from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
import sqlite3


class Setting(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/setting.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Shop Settings")
        self.uid = uid
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.loadData()
        self.updateb.clicked.connect(self.updateData)

    def loadData(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        if(result):
            data = result.fetchone()
            self.name.setText(data[1])
            self.website.setText(data[4])
            self.phone.setText(data[2])
            self.email.setText(data[3])
            self.licence.setText(data[5])
            self.address.setText(data[6])
            self.msg.setText(data[7])
        else:
            self.close()    
        cur.close()    

    def updateData(self):
        name = self.name.text()
        licence = self.licence.text()
        phone = self.phone.text()
        email = self.email.text()
        website = self.website.text()
        address = self.address.toPlainText()
        msg = self.msg.toPlainText()
        cur = self.conn.cursor()
        if(self.uid==""):
            QMessageBox.warning(None, ("Required"), 
            ("Login expired please login again after close window"),
             QMessageBox.Cancel)  
        elif(name==""  and phone==""):
            QMessageBox.warning(None, ("Required"), 
            ("Please Fill shop name  and phone  Field"),
             QMessageBox.Cancel)  
        else:    
            try:
                result = cur.execute("UPDATE settings SET name=?,phone=?,email=?,website=?,licence=?,address=?,msg=? WHERE id=?",(name,phone,email,website,licence,address,msg,1,))
                self.conn.commit()
                if(result):
                    self.loadData()
                    QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
                else:
                    QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Cancel)       
            except:
                QMessageBox.warning(None, ("Failed"), ("Data not updated Database Error "),QMessageBox.Cancel)                                
        cur.close()

