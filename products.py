import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from productledger import ProductLedger
import sqlite3
import uuid
from hrate import rateHide

class Products(QWidget):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/product1.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Products")
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.buy.setValidator(self.onlynumber)
        self.wholesale.setValidator(self.onlynumber)
        self.sales.setValidator(self.onlynumber)
        self.pqtn.setValidator(self.onlynumber)
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.category.addItem("Select Category")
        self.categoryData()
        self.barcode = str(uuid.uuid4().int)[:12]
        self.unit.addItem("Select Unit")
        self.unitData()
        self.uid=uid
        self.role=role
        self.addb.clicked.connect(self.updateData)
        self.loadData()
        self.tableWidget.setHorizontalHeaderLabels(["ID","Item Code","Barcode","Price Status","Product Name","Category","Unit","Purchase Rate","Wholesale","Sales Rate","Re Order Qtn"])
        self.searchv.textChanged.connect(self.search)
        self.tableWidget.doubleClicked.connect(self.ddbclick)
        self.deleteb.clicked.connect(self.deleteData)
        self.ledgerb.clicked.connect(self.ledgerpro)
        self.id=""
        self.buy.textChanged.connect(self.buySet)

    def buySet(self):
        val = rateHide(self.buy.text())
        self.hrate.setText(val)

    def ledgerpro(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if(id):
            self.ledger =ProductLedger(id)
            self.ledger.show()
        else:
            QMessageBox.warning(None, ("Required"), 
            ("Please Select any row or column to see Product Ledger"),
             QMessageBox.Ok)    

    def updateData(self):
        name = self.name.text()
        model = self.model.text()
        category = self.category.currentText()
        unit = self.unit.currentText()
        buyrate = self.buy.text()
        salerate = self.sales.text()
        wholesale = self.wholesale.text()
        tax = self.vat.text()
        discount = "0"
        reorder = self.reorder.text()
        status = self.status.currentText()
        itemcode = self.itemcode.text()
        hrate = self.hrate.text()
        cur = self.conn.cursor()
        if(name==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Name Required"),
             QMessageBox.Ok)
        elif(buyrate=="" or salerate=="" or wholesale=="" or tax=="" or discount==""):
            QMessageBox.warning(None, ("All 0 field is Required"), 
            ("All 0 Zero field not be empty minimum 0 is required"),
             QMessageBox.Ok)             
        elif(self.category.currentText()=="Select Category"):
            QMessageBox.warning(None, ("Category is required"), 
            ("Category is required"),
             QMessageBox.Ok)  
        elif(self.unit.currentText()=="Select Unit"):
            QMessageBox.warning(None, ("Unit is required"), 
            ("Unit is required"),
             QMessageBox.Ok)   
        elif(self.vat.text()==""):
            QMessageBox.warning(None, ("Vat is required"), 
            ("Vat is required not be empty"),
             QMessageBox.Ok)               
        elif(reorder==""):
            QMessageBox.warning(None, ("Required"), 
            ("Reorder not be empty please fill atleat 0"),
             QMessageBox.Ok)               
        else:    
            if self.id !="":
                result = cur.execute("UPDATE products SET name=?,model=?,category=?,unit=?,buyrate=?,salerate=?,wholesale=?,tax=?,discount=?,reorder=?,status=?,itemcode=?,hrate=? WHERE id=?",(name,model,category,unit,buyrate,salerate,wholesale,tax,discount,reorder,status,itemcode,hrate,self.id,))
                self.conn.commit()
                if(result):
                    self.loadData()
                    self.category.setCurrentText("Select Category")
                    self.unit.setCurrentText("Select Unit")
                    self.loadData()
                    self.categoryData()
                    self.unitData()
                    self.name.setText("")
                    self.model.setText("")
                    self.buy.setText("0")
                    self.sales.setText("0")
                    self.wholesale.setText("0")
                    self.pqtn.setText("0")
                    self.reorder.setText("0")
                    self.vat.setText("0")
                    self.id=""
                    self.itemcode.setText("")
                    self.status.setCurrentText("Fixed") 
                    cur.close()               
                    QMessageBox.information(None, ("Successful"), ("Data updated successfully"),QMessageBox.Ok) 
                else:
                    QMessageBox.warning(None, ("Failed"), ("Data not updated "),QMessageBox.Ok)   
            else:
                self.addData()                     


    def ddbclick(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if(id):
            cur = self.conn.cursor()
            result = cur.execute("SELECT * FROM products WHERE id=? ",(id,))
            if(result):
                data = result.fetchone()
                self.name.setText(data[1])
                self.model.setText(data[2])
                self.buy.setText(data[5])
                self.sales.setText(data[6])
                self.wholesale.setText(data[7])
                self.category.setCurrentText(data[3])
                self.unit.setCurrentText(data[4])
                self.reorder.setText(data[13])
                self.itemcode.setText(data[16])
                self.status.setCurrentText(data[15])
                self.id=data[0]
                self.vat.setText(data[9])
                self.hrate.setText(data[17])
                cur.close()

    def loadData(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,itemcode,barcode,status,name,category,unit,buyrate,wholesale,salerate,reorder,strftime('%d/%m/%Y',date) FROM products ORDER BY id DESC")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 
        cur.close()

    def search(self):
        sv = self.searchv.text()    
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,itemcode,barcode,status,name,category,unit,buyrate,wholesale,salerate,reorder,strftime('%d/%m/%Y',date) FROM products WHERE name LIKE ? OR model LIKE ? OR itemcode LIKE ? ORDER BY id DESC",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 
        cur.close()        

    def categoryData(self):
        data = self.cur.execute("SELECT * FROM category")
        result = data.fetchall()
        for i in result:
            self.category.addItem(i[1])
    def unitData(self):
        data = self.cur.execute("SELECT * FROM unit")
        result = data.fetchall()       
        for i in result:
            self.unit.addItem(i[1])

    def addData(self):
        name = self.name.text()
        model = self.model.text()
        category = self.category.currentText()
        unit = self.unit.currentText()
        buyrate = self.buy.text()
        salerate = self.sales.text()
        wholesale = self.wholesale.text()
        tax = self.vat.text()
        discount = "0"
        pqtn = self.pqtn.text()
        reorder = self.reorder.text()
        status = self.status.currentText()
        itemcode = self.itemcode.text()
        hrate = self.hrate.text()
        cur = self.conn.cursor()
        if(name==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Name Required"),
             QMessageBox.Ok)
        elif(buyrate=="" or salerate=="" or wholesale=="" or tax=="" or discount==""):
            QMessageBox.warning(None, ("All 0 field is Required"), 
            ("All 0 Zero field not be empty minimum 0 is required"),
             QMessageBox.Ok)              
        elif(self.category.currentText()=="Select Category"):
            QMessageBox.warning(None, ("Category is required"), 
            ("Category is required"),
             QMessageBox.Ok)  
        elif(self.unit.currentText()=="Select Unit"):
            QMessageBox.warning(None, ("Unit is required"), 
            ("Unit is required"),
             QMessageBox.Ok)   
        elif(self.vat.text()==""):
            QMessageBox.warning(None, ("Vat is required"), 
            ("Vat is required not be empty"),
             QMessageBox.Ok)                
        elif(reorder==""):
            QMessageBox.warning(None, ("Required"), 
            ("Reorder not be empty please fill atleat 0"),
             QMessageBox.Ok)                         
        else:    
            if pqtn=="0" or pqtn=="":
                result = cur.execute("INSERT INTO products(name,model,category,unit,buyrate,salerate,wholesale,tax,discount,barcode,reorder,status,itemcode,hrate)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(name,model,category,unit,buyrate,salerate,wholesale,tax,discount,self.barcode,reorder,status,itemcode,hrate,))
                self.conn.commit()
                if(result):
                    self.category.setCurrentText("Select Category")
                    self.unit.setCurrentText("Select Unit")
                    self.loadData()
                    self.categoryData()
                    self.unitData()
                    self.name.setText("")
                    self.model.setText("")
                    self.buy.setText("0")
                    self.sales.setText("0")
                    self.wholesale.setText("0")
                    self.pqtn.setText("0")
                    self.reorder.setText("0")
                    self.itemcode.setText("")
                    self.vat.setText("0")
                    self.hrate.setText("")
                    self.status.setCurrentText("Fixed")
                    self.barcode = str(uuid.uuid4().int)[:12]
                    cur.close()
                    QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok) 
            
                else:
                    self.loadData()
                    QMessageBox.warning(None, ("Failed"), ("Data not added "),QMessageBox.Ok)    
            else:
                result = cur.execute("INSERT INTO products(name,model,category,unit,buyrate,salerate,wholesale,qtn,tax,discount,barcode,reorder,status,itemcode)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(name,model,category,unit,buyrate,salerate,wholesale,pqtn,tax,discount,self.barcode,reorder,status,itemcode,))
                self.conn.commit()
                if(result):
                    id = result.lastrowid
                    self.cur.execute("INSERT INTO proadjust(pid,qtn,des,type,uid)VALUES(?,?,?,?,?)",(id,pqtn,"Previous Stock Qtn","Product Increae",self.uid,))
                    self.conn.commit()
                    self.category.setCurrentText("Select Category")
                    self.unit.setCurrentText("Select Unit")
                    self.loadData()
                    self.categoryData()
                    self.unitData()
                    self.name.setText("")
                    self.hrate.setText("")
                    self.model.setText("")
                    self.buy.setText("0")
                    self.sales.setText("0")
                    self.wholesale.setText("0")
                    self.pqtn.setText("0")
                    self.reorder.setText("0")
                    self.itemcode.setText("")
                    self.vat.setText("0")
                    self.status.setCurrentText("Fixed")
                    self.barcode = str(uuid.uuid4().int)[:12]
                    cur.close()
                    QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok) 
            
                else:
                    self.loadData()
                    QMessageBox.warning(None, ("Failed"), ("Data not added "),QMessageBox.Ok)  

    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row"),QMessageBox.Yes,QMessageBox.No) 
        if(reply == QMessageBox.Yes):
            cur = self.conn.cursor()
            purch = cur.execute("SELECT * FROM purchase WHERE pid=?",(id,))
            pdata = purch.fetchall()
            sal = cur.execute("SELECT * FROM sales WHERE pid=?",(id,))
            sdata = sal.fetchall()
            if len(pdata)>0 or len(sdata)>0:
                QMessageBox.warning(None, ("Warning"), ("You can't delete this product its purchase or sales history len geater then 0"),QMessageBox.Ok)
            else:    
                result = cur.execute("DELETE FROM products WHERE id=?",(id,))
                self.conn.commit()        
                if(result):
                    cur.execute("DELETE FROM purchase WHERE pid=?",(id,))
                    self.conn.commit()  
                    cur.execute("DELETE FROM sales WHERE pid=?",(id,))
                    self.conn.commit()                 
 
                    cur.execute("DELETE FROM proadjust WHERE pid=?",(id,))
                    self.conn.commit()   

                    cur.execute("DELETE FROM damage WHERE pid=?",(id,))
                    self.conn.commit()   

                    cur.execute("DELETE FROM pledger WHERE pid=?",(id,))
                    self.conn.commit()  

                    self.category.setCurrentText("Select Category")
                    self.unit.setCurrentText("Select Unit")
                    
                    self.loadData()
                    QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
                    self.loadData()
            cur.close()        


