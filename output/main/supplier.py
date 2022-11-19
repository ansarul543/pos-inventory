import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem
import random
import sqlite3

class Supplier(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/supplier.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("New Supplier")
        self.tableWidget.setHorizontalHeaderLabels(["ID","Name","Email","Phone","Type","Website","Address","Party Code"])
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.due.setValidator(self.onlynumber)  
        self.uid=uid      
        self.loadData()
        self.deleteb.clicked.connect(self.deleteData)
        self.editb.clicked.connect(self.savedata)
        self.searchb.textChanged.connect(self.search)
        self.tableWidget.doubleClicked.connect(self.ddbclick)
        self.pushButton.clicked.connect(self.addS)
        self.id=""

    def savedata(self):
        name = self.name.text()
        email = self.email.text()
        phone = self.phone.text()
        type = self.select()
        website = self.website.text()
        address = self.address.toPlainText()
        partycode = self.partycode.text()
        if(name==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Name Required"),
             QMessageBox.Ok)
        elif(phone==""):
            QMessageBox.warning(None, ("Phone is required"), 
            ("Phone is required"),
             QMessageBox.Ok)   
        else:    
            result = self.cur.execute("UPDATE supplier SET name=?,email=?,phone=?,type=?,website=?,address=?,partycode=? WHERE id=?",(name,email,phone,type,website,address,partycode,self.id,))
            self.conn.commit()
            if(result):
                self.name.setText("")
                self.email.setText("")
                self.phone.setText("")
                self.website.setText("")
                self.address.setPlainText("")
                self.partycode.setText("")
                self.loadData()
                QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
            else:
                QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Ok)    
    def select(self):
        if(self.sup.isChecked()):
            return "Supplier"      
        if(self.agent.isChecked()):
            return "Agent" 
        if(self.dis.isChecked()):
            return "Distributor"  

    def addS(self):
        name = self.name.text()
        email = self.email.text()
        phone = self.phone.text()
        type = self.select()
        website = self.website.text()
        address = self.address.toPlainText()
        partycode = self.partycode.text()
        if(name==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Name Required"),
             QMessageBox.Ok)
        elif(phone==""):
            QMessageBox.warning(None, ("Phone is required"), 
            ("Phone is required"),
             QMessageBox.Ok)   
        else:    
            due = self.due.text()
            if due=="" or due=="0":
                result = self.cur.execute("INSERT INTO supplier(name,email,phone,type,website,address,partycode)VALUES(?,?,?,?,?,?,?)",(name,email,phone,type,website,address,partycode,))
                self.conn.commit()
                if(result):
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
            else:
                invoice = str(random.randint(10000, 100000))
                result = self.cur.execute("INSERT INTO supplier(name,email,phone,type,website,address,partycode)VALUES(?,?,?,?,?,?,?)",(name,email,phone,type,website,address,partycode,))
                self.conn.commit()
                if(result):
                    sid = result.lastrowid
                    query = (sid,due,invoice,self.uid,)
                    result2 = self.cur.execute("INSERT INTO pinvoice(sid,total,invoice,uid)VALUES(?,?,?,?)",query)
                    if (result2):
                        self.conn.commit()
                        id = result2.lastrowid
                        self.cur.execute("INSERT INTO ppp(type,invoice_id,sid,uid)VALUES(?,?,?,?)",("Previous Due",id,sid,self.uid,))
                        self.conn.commit() 
                    
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

    def ddbclick(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if(id):
            result = self.cur.execute("SELECT * FROM supplier WHERE id=?",(id,))
            data = result.fetchone()
            self.id=data[0]
            self.name.setText(data[1])
            self.email.setText(data[2])
            self.phone.setText(data[3])
            self.website.setText(data[5])
            self.address.setPlainText(data[6])
            if(data[4]=="Supplier"):
                self.sup.setChecked(True)    
            if(data[4]=="Agent"):
                self.agent.setChecked(True)
            if(data[4]=="Distributor"):
                self.dis.setChecked(True)
            self.partycode.setText(data[7])    
                        
    def editButton(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if(id):
            self.dataedit = EditSupplier(id)
            self.dataedit.show()
        else:
            QMessageBox.information(None, ("Alert"), ("Selected Row is required"),QMessageBox.Ok)  

  
    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if id==None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row"),QMessageBox.Ok)
        elif id=="0":
            QMessageBox.warning(None, ("Warning"), ("Do not permission to delete 0 id . its default"),QMessageBox.Ok)
        else:          
            reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row.\n you can lose your all supplier related data from other table"),QMessageBox.Yes,QMessageBox.No) 
            if(reply == QMessageBox.Yes):      
                result = self.cur.execute("DELETE FROM supplier WHERE id=?",(id,))
                self.conn.commit()
                if(result):
                    self.cur.execute("DELETE FROM pinvoice WHERE sid=?",(id,))
                    self.conn.commit()                       
                    self.cur.execute("DELETE FROM purchase WHERE sid=?",(id,))
                    self.conn.commit()               
                    self.cur.execute("DELETE FROM cash WHERE type='Supplier' AND accid=?",(id,))
                    self.conn.commit() 
                    self.cur.execute("DELETE FROM ppp WHERE sid=?",(id,))
                    self.conn.commit()    
                    self.cur.execute("DELETE FROM pledger WHERE sid=?",(id,))
                    self.conn.commit()                                                         
                    QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
                    self.loadData()


    def loadData(self):
        result = self.cur.execute("SELECT * FROM supplier ORDER BY id DESC")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data)))        

    def search(self):
        sv = self.searchb.text()    
        result = self.cur.execute("SELECT * FROM supplier WHERE name LIKE ? OR id LIKE ? OR partycode LIKE ? ORDER BY id DESC",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 

