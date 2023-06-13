import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem
import random
import sqlite3

class AddCustomer(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/addcustomer.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("New Customer")
        self.addCusBtn.clicked.connect(self.addCus)
        self.uid=uid  
        self.tableWidget.setHorizontalHeaderLabels(["ID","Name","Email","Phone","Type","Website","Address","Party Code","Discount %"])
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.due.setValidator(self.onlynumber)        
        self.loadData()
        self.tableWidget.doubleClicked.connect(self.ddbclick)
        self.deleteb.clicked.connect(self.deleteData)
        self.searchv.textChanged.connect(self.search)
        self.updateb.clicked.connect(self.updateCus)
        self.id=""

    def updateCus(self):
        name = self.name.text()
        email = self.email.text()
        phone = self.phone.text()
        type = self.select()
        website = self.website.text()
        address = self.address.toPlainText()
        partycode = self.partycode.text()
        discount = self.discount.text()
        if(name==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Name Required"),
             QMessageBox.Ok)
        elif(phone==""):
            QMessageBox.warning(None, ("Phone is required"), 
            ("Phone is required"),
             QMessageBox.Ok)  
        elif(discount==""):
            QMessageBox.warning(None, ("Discount is required"), 
            ("Discount is required"),
             QMessageBox.Ok)             
        else:    
            cur = self.conn.cursor()
            result = cur.execute("UPDATE customer SET name=?,email=?,phone=?,type=?,website=?,address=?,partycode=?,discount=? WHERE id=?",(name,email,phone,type,website,address,partycode,discount,self.id,))
            self.conn.commit()
            if(result):
                self.loadData()
                self.name.setText("")
                self.email.setText("")
                self.phone.setText("")
                self.website.setText("")
                self.address.setPlainText("")
                self.partycode.setText("")         
                self.discount.setText("0")    
                cur.close()      
                QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
            else:
                QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Ok)    

    def search(self):
        sv = self.searchv.text()  
        cur = self.conn.cursor()  
        result = cur.execute("SELECT * FROM customer WHERE name LIKE ? OR id LIKE ? OR partycode LIKE ? ORDER BY id DESC",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
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
            self.id = id
            cur = self.conn.cursor()
            result = cur.execute("SELECT * FROM customer WHERE id=?",(self.id,))
            if(result):
                data = result.fetchone()
                self.name.setText(data[1])
                self.email.setText(data[2])
                self.phone.setText(data[3])
                self.website.setText(data[5])
                self.address.setPlainText(data[6])
                self.discount.setText(data[8])
                if(data[4]=="Retail"):
                    self.type.setChecked(True)    
                if(data[4]=="Wholesale"):
                    self.type2.setChecked(True)
                self.partycode.setText(data[7])    
                cur.close()

    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        self.loadData()
        cur = self.conn.cursor()
        if id==None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row"),QMessageBox.Ok)
        elif id=="0":
            QMessageBox.warning(None, ("Warning"), ("Do not permission to delete 0 id . its default"),QMessageBox.Ok)
        else:          
            reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row .\n you can lose your all customer related data from other table"),QMessageBox.Yes,QMessageBox.No) 
            if(reply == QMessageBox.Yes):
                result = cur.execute("DELETE FROM customer WHERE id=?",(id,))
                self.conn.commit()
                if(result):
                    cur.execute("DELETE FROM sinvoice WHERE cid=?",(id,))
                    self.conn.commit()                     
                    cur.execute("DELETE FROM sales WHERE cid=?",(id,))
                    self.conn.commit() 
                    cur.execute("DELETE FROM cash WHERE type='Customer' AND accid=?",(id,))
                    self.conn.commit() 
                    cur.execute("DELETE FROM sss WHERE cid=?",(id,))
                    self.conn.commit()     
                    cur.execute("DELETE FROM pledger WHERE cid=?",(id,))
                    self.conn.commit()   
                    cur.close()                                                                  
                    QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
                    self.loadData()            
    def addCus(self):
        name = self.name.text()
        email = self.email.text()
        phone = self.phone.text()
        type = self.select()
        website = self.website.text()
        address = self.address.toPlainText()
        partycode = self.partycode.text()
        discount = self.discount.text()
        if(name==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Name Required"),
             QMessageBox.Ok)
        elif(phone==""):
            QMessageBox.warning(None, ("Phone is required"), 
            ("Phone is required"),
             QMessageBox.Ok)   
        elif(discount==""):
            QMessageBox.warning(None, ("Discount is required"), 
            ("Discount is required"),
             QMessageBox.Ok)              
        else: 
            cur = self.conn.cursor()   
            due = self.due.text()
            if due=="" or due=="0":           
                result = cur.execute("INSERT INTO customer(name,email,phone,type,website,address,partycode,discount)VALUES(?,?,?,?,?,?,?,?)",(name,email,phone,type,website,address,partycode,discount,))
                self.conn.commit()
                if(result):
                    self.loadData()
                    self.name.setText("")
                    self.email.setText("")
                    self.phone.setText("")
                    self.website.setText("")
                    self.address.setPlainText("")
                    self.partycode.setText("")
                    self.due.setText("0")
                    self.discount.setText("0")
                    cur.close()
                    self.loadData()
                    QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok) 
                else:
                    self.loadData()
                    QMessageBox.warning(None, ("Failed"), ("Data not added "),QMessageBox.Ok)    
            else:
                invoice = str(random.randint(10000, 100000))
                result = cur.execute("INSERT INTO customer(name,email,phone,type,website,address,partycode)VALUES(?,?,?,?,?,?,?)",(name,email,phone,type,website,address,partycode,))
                self.conn.commit()
                if(result):
                    cid = result.lastrowid
                    query = (cid,due,invoice,self.uid,)
                    result2 = cur.execute("INSERT INTO sinvoice(cid,total,invoice,uid)VALUES(?,?,?,?)",query)
                    if (result2):
                        self.conn.commit()
                        id = result2.lastrowid
                        cur.execute("INSERT INTO sss(type,invoice_id,cid,uid)VALUES(?,?,?,?)",("Previous Due",id,cid,self.uid,))
                        self.conn.commit() 
                    self.loadData()
                    self.name.setText("")
                    self.email.setText("")
                    self.phone.setText("")
                    self.website.setText("")
                    self.address.setPlainText("")
                    self.partycode.setText("")
                    self.due.setText("0")
                    self.loadData()
                    QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok) 
                else:
                    self.loadData()
                    QMessageBox.warning(None, ("Failed"), ("Data not added "),QMessageBox.Ok)        
            cur.close()                        

    def select(self):
        if(self.type.isChecked()):
            return "Retail"      
        if(self.type2.isChecked()):
            return "Wholesale" 


    def loadData(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT * FROM customer ORDER BY id DESC")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
 
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data)))   
        cur.close()             


