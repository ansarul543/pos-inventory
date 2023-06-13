import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3

class ProductDamage(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/damage.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Damage Product Entry")
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)        
        self.uid = uid
        self.addb.clicked.connect(self.addS)
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.tableWidget.setHorizontalHeaderLabels(["ID","Product Name","Product ID","Quantity","Description","Date","Prepared By"])
        self.searchv.textChanged.connect(self.search)
        self.deleteb.clicked.connect(self.deleteData)
        self.allb.clicked.connect(self.allData)
        self.viewb.clicked.connect(self.loadDataDate)
        self.searchv_2.textChanged.connect(self.searchD)
        self.id =""
        self.quantity =""
        self.sale="0"

    def allData(self):
        self.loadData()

    def searchD(self):
        sv = self.searchv_2.text()    
        if sv =="":
            a =0
        else:    
            cur = self.conn.cursor()
            result = cur.execute("SELECT damage.id,products.name,products.id,damage.qtn,damage.des,strftime('%d/%m/%Y',damage.date),users.name FROM damage INNER JOIN products ON damage.pid=products.id LEFT JOIN users ON damage.uid=users.id WHERE products.name LIKE ? OR products.id LIKE ?",("%"+sv+"%","%"+sv+"%",))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number,column_number, QTableWidgetItem(str(data))) 
            cur.close()        

    def loadData(self):
        self.name.setText("")
        self.stock.setText("")
        self.id = ""
        self.quantity =""  
        cur = self.conn.cursor()      
        result = cur.execute("SELECT damage.id,products.name,products.id,damage.qtn,damage.des,strftime('%d/%m/%Y',damage.date),users.name FROM damage INNER JOIN products ON damage.pid=products.id LEFT JOIN users ON damage.uid=users.id ORDER BY damage.id DESC")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 
        cur.close()        

    def loadDataDate(self):    
        sv = self.searchv_2.text()
        time = QTime.currentTime()
        currenttime = '23:58:00'
        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date
        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime   
        cur = self.conn.cursor() 
        if sv=="":
            result = cur.execute("SELECT damage.id,products.name,products.id,damage.qtn,damage.des,strftime('%d/%m/%Y',damage.date),users.name FROM damage INNER JOIN products ON damage.pid=products.id LEFT JOIN users ON damage.uid=users.id WHERE damage.date BETWEEN ? AND ?",(fromd,tod,))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number,column_number, QTableWidgetItem(str(data))) 
        else:
            result = cur.execute("SELECT damage.id,products.name,products.id,damage.qtn,damage.des,strftime('%d/%m/%Y',damage.date),users.name FROM damage INNER JOIN products ON damage.pid=products.id LEFT JOIN users ON damage.uid=users.id WHERE products.name LIKE ? OR products.id LIKE ? and damage.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%",fromd,tod,))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number,column_number, QTableWidgetItem(str(data)))    
        cur.close()                                 

    def addS(self):
        name = self.name.text()
        id = self.id
        des = self.des.text()
        cur = self.conn.cursor()
        if(name=="" and id==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Product Name is Required"),
             QMessageBox.Ok)
        elif self.qtn.text()=="":
            QMessageBox.warning(None, ("Required"), 
            ("Product Qtn is Required"),
             QMessageBox.Ok)                  
        else:    
            qtn = float(self.qtn.text())
            cur.execute("INSERT INTO damage(pid,qtn,des,uid)VALUES(?,?,?,?)",(self.id,qtn,des,self.uid,))
            self.conn.commit()
            quantity = float(self.quantity)
            qtns = quantity-qtn
            result = cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtns,id))
            self.conn.commit()
            if(result):
                damageid = result.lastrowid
                query3 = ("Damage",self.id,damageid,self.uid,self.sale,str(qtn),)
                cur.execute("INSERT INTO pledger(type,pid,damage_id,uid,price,qtn)VALUES(?,?,?,?,?,?)",query3)
                self.conn.commit()     
                QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok) 
            else:
                QMessageBox.information(None, ("Failed"), ("Data not added "),QMessageBox.Ok)     
            self.loadData()
            self.qtn.setText("0")
            self.des.setText("")
            self.sale="0"
            cur.close()


    def search(self):
        sv = self.searchv.text()  
        cur = self.conn.cursor()  
        if sv=="":
            self.name.setText("")
            self.stock.setText("")
            self.id = ""
            self.quantity =""
            self.sale="0"
        else:    
            result = cur.execute("SELECT id,name,unit,qtn,buyrate FROM products WHERE id LIKE ? OR name LIKE ? ",("%"+sv+"%","%"+sv+"%",))
            data = result.fetchone()
            if data:
                self.name.setText(str(data[1]))
                self.stock.setText(str(data[2]+" "+data[3]))
                self.id = data[0]
                self.quantity = data[3]
                self.sale=data[4]
            else:
                self.name.setText("")
                self.stock.setText("") 
                self.id = ""  
                self.quantity =""
                self.sale="0"
        cur.close()        
        
    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(2)
        pid = NewInd.data()  
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(3)
        qtn = NewInd.data()  
        cur = self.conn.cursor()           
        res = cur.execute("SELECT id,qtn FROM products WHERE id=?",(pid,))
        data = res.fetchone()              
        reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row"),QMessageBox.Yes,QMessageBox.No) 
        if(reply == QMessageBox.Yes):          
                if id=="":
                    QMessageBox.warning(None, ("Warning"), ("Please select any row"),QMessageBox.Ok)
                else:   
                    qtn = float(qtn) 
                    cur.execute("DELETE FROM damage WHERE id=?",(id,))
                    self.conn.commit()
                    quantity = float(data[1])
                    qtn = quantity+qtn
                    result = cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn,pid))
                    self.conn.commit()
                    if(result):
                        cur.execute("DELETE FROM pledger WHERE damage_id=?",(id,))
                        self.conn.commit()                          
                        QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
                    else:
                        QMessageBox.information(None, ("Failed"), ("Data not deleted "),QMessageBox.Ok)     
                    self.loadData()
                cur.close()    

    def select(self):
        if(self.minus.isChecked()):
            return "Product Minus"      
        if(self.plus.isChecked()):
            return "Product Increae" 


