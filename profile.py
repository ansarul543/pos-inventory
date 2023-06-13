import sys
from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
import sqlite3
from werkzeug.security import generate_password_hash

class Profile(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/profile.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Profile")
        self.uid = uid
        self.loadData()
        self.updateb.clicked.connect(self.updateData)
        
    def loadData(self):
        conn = sqlite3.connect('./database/data.db')
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM users WHERE id=? ",(self.uid,))
        if(result):
            data = result.fetchone()
            self.name.setText(data[1])
            self.username.setText(data[2])
            self.phone.setText(data[3])
            self.email.setText(data[4])
        else:
            self.close()    

    def updateData(self):
        conn = sqlite3.connect('./database/data.db')
        cur = conn.cursor()
        name = self.name.text()
        username = self.username.text()
        phone = self.phone.text()
        email = self.email.text()
        password = self.password.text()
        password2 = generate_password_hash(password, "sha256")

        if(self.uid==""):
            QMessageBox.warning(None, ("Required"), 
            ("Login expired please login again after close window"),
             QMessageBox.Cancel)  
        elif(name=="" and username=="" and phone==""):
            QMessageBox.warning(None, ("Required"), 
            ("Please Fill name username and phone  Field"),
             QMessageBox.Cancel)  
        else:    
            if(password):
                try:
                    result = cur.execute("UPDATE users SET name=?,username=?,phone=?,email=?,password=? WHERE id=?",(name,username,phone,email,password2,self.uid,))
                    conn.commit()
                    if(result):
                        cur.close()
                        self.loadData()
                        QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
                    else:
                        QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Cancel)   
                except:
                    QMessageBox.warning(None, ("Failed"), ("Data not updated Database Error "),QMessageBox.Cancel)                     
            else:
                try:
                    result = cur.execute("UPDATE users SET name=?,username=?,phone=?,email=? WHERE id=?",(name,username,phone,email,self.uid,))    
                    conn.commit()
                    if(result):
                        cur.close()
                        self.loadData()
                        QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
                    else:
                        QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Cancel) 
                except:
                    QMessageBox.warning(None, ("Failed"), ("Data not updated Database Error "),QMessageBox.Cancel)   



 