import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3
from werkzeug.security import generate_password_hash

class User(QDialog):
    def __init__(self,p='',parent=None):
        super().__init__()
        uic.loadUi('./ui/users.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Users List")
        self.addb.clicked.connect(self.addS)
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.tableWidget.setHorizontalHeaderLabels(["ID","Name","Username","Phone","Email","Type"])
        self.loadData()
        self.searchv.textChanged.connect(self.search)
        self.deleteb.clicked.connect(self.deleteData)
        self.tableWidget.doubleClicked.connect(self.ddbclick)
        self.id =""


    def addS(self):
        if self.id !="":
            name = self.name.text()
            username = self.username.text()
            phone = self.phone.text()
            email = self.email.text()
            password = self.password.text()
            password2 = generate_password_hash(password, "sha256")

            role = self.selectData()
            if(self.id==""):
                QMessageBox.warning(None, ("Required"), 
                ("Data not selected yet Please select data before update"),
                QMessageBox.Cancel)  
            elif(name=="" and username=="" and phone==""):
                QMessageBox.warning(None, ("Required"), 
                ("Please Fill name username and phone  Field"),
                QMessageBox.Cancel)  
            else:    
                if(password):
                    cur = self.conn.cursor()
                    result = cur.execute("UPDATE users SET name=?,username=?,phone=?,email=?,password=?,role=? WHERE id=?",(name,username,phone,email,password2,role,self.id,))
                    self.conn.commit()
                    if(result):
                        cur.close()
                        self.loadData()
                        self.id=""
                        self.name.setText("")
                        self.username.setText("")
                        self.phone.setText("")
                        self.email.setText("")
                        self.password.setText("")
                        QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
                    else:
                        QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Cancel)                
                else:
                    cur = self.conn.cursor()
                    result = cur.execute("UPDATE users SET name=?,username=?,phone=?,email=?,role=? WHERE id=?",(name,username,phone,email,role,self.id,))    
                    self.conn.commit()
                    if(result):
                        cur.close()
                        self.loadData()
                        self.id=""
                        self.name.setText("")
                        self.username.setText("")
                        self.phone.setText("")
                        self.email.setText("")
                        self.password.setText("")
                        QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
                    else:
                        QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Cancel) 
        else:    
            name = self.name.text()
            username = self.username.text()
            phone = self.phone.text()
            email = self.email.text()
            password = self.password.text()
            password2 = generate_password_hash(password, "sha256")
            role = self.selectData()

            if(name=="" and username=="" and phone=="" and password==""):
                QMessageBox.warning(None, ("Required"), 
                ("Please Fill name username and phone and Password Field"),
                QMessageBox.Cancel) 
            else:    
                cur = self.conn.cursor()
                result = cur.execute("INSERT INTO users(name,username,phone,email,password,role)VALUES(?,?,?,?,?,?)",(name,username,phone,email,password2,role,))
                self.conn.commit()
                if(result):
                    cur.close()
                    self.name.setText("")
                    self.username.setText("")
                    self.phone.setText("")
                    self.email.setText("")
                    self.password.setText("")
                    QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok)  
                    self.loadData()           
                else:
                    self.loadData()
                    QMessageBox.warning(None, ("Failed"), ("Data not added "),QMessageBox.Cancel)  

                


    def loadData(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT * FROM users ORDER BY id DESC")
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
        if(id):
            cur = self.conn.cursor()
            result = cur.execute("SELECT * FROM users WHERE id=? ",(id,))
            if(result):
                data = result.fetchone()
                self.name.setText(data[1])
                self.username.setText(data[2])
                self.phone.setText(data[3])
                self.email.setText(data[4])
                if(data[5]=="Admin"):
                    self.admin.setChecked(True)
                if(data[5]=="SalesMan"):
                    self.user.setChecked(True)    
                if(data[5]=="Manager"):
                    self.manager.setChecked(True)    
                self.id=data[0]
            cur.close()


    def selectData(self):
        if(self.admin.isChecked()):
           return "Admin"
        if(self.user.isChecked()):
            return "SalesMan"   
        if(self.manager.isChecked()):
            return "Manager" 

    def search(self):
        sv = self.searchv.text()  
        cur = self.conn.cursor()  
        result = cur.execute("SELECT * FROM users WHERE name LIKE ? OR phone LIKE ?  ORDER BY id DESC",("%"+sv+"%","%"+sv+"%",))
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
        reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row"),QMessageBox.Yes,QMessageBox.No) 
        if(reply == QMessageBox.Yes):
            cur = self.conn.cursor()
            result = cur.execute("DELETE FROM users WHERE id=?",(id,))
            self.conn.commit()
            if(result):
                cur.execute("DELETE FROM loginhistory WHERE uid=?",(id,))
                self.conn.commit()
                QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok)
                cur.close() 
                self.loadData()

