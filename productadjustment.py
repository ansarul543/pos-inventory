import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3

class ProductAdjutment(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/productadjustment.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Product Adjustment")
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)          
        self.addb.clicked.connect(self.addS)
        self.uid = uid
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.tableWidget.setHorizontalHeaderLabels(["ID","Product Name","Product ID","Quantity","Type","Description","Date","Prepared By"])
        self.searchv.textChanged.connect(self.search)
        self.deleteb.clicked.connect(self.deleteData)
        self.searchv_2.textChanged.connect(self.loadDataSearch)
        self.viewb.clicked.connect(self.loadDataDate)
        self.allb.clicked.connect(self.alldata)
        self.id =""
        self.quantity =""
        self.sale="0"

    def alldata(self):
        self.loadData()    

    def loadDataDate(self):
        self.name.setText("")
        self.stock.setText("")
        self.id = ""
        self.quantity =""  
        sv = self.searchv_2.text() 
        time = QTime.currentTime()
        currenttime = '23:58:00'
        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date
        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime               
        if sv=="":
            result = self.cur.execute("SELECT proadjust.id,products.name,products.id,proadjust.qtn,proadjust.type,proadjust.des,strftime('%d/%m/%Y',proadjust.date),users.name FROM proadjust INNER JOIN products ON proadjust.pid=products.id LEFT JOIN users ON proadjust.uid=users.id WHERE proadjust.date BETWEEN ? AND ?",(fromd,tod,))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        else:      
            result = self.cur.execute("SELECT proadjust.id,products.name,products.id,proadjust.qtn,proadjust.type,proadjust.des,strftime('%d/%m/%Y',proadjust.date),users.name FROM proadjust INNER JOIN products ON proadjust.pid=products.id LEFT JOIN users ON proadjust.uid=users.id WHERE products.name LIKE ? OR products.id LIKE ? OR products.itemcode LIKE ? and proadjust.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",fromd,tod,))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number,column_number, QTableWidgetItem(str(data)))

    def loadData(self):
        self.name.setText("")
        self.stock.setText("")
        self.id = ""
        self.quantity =""      
        self.sale="0"  
        result = self.cur.execute("SELECT proadjust.id,products.name,products.id,proadjust.qtn,proadjust.type,proadjust.des,strftime('%d/%m/%Y',proadjust.date),users.name FROM proadjust INNER JOIN products ON proadjust.pid=products.id LEFT JOIN users ON proadjust.uid=users.id ORDER BY proadjust.id DESC")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,
                        column_number, QTableWidgetItem(str(data))) 

    def loadDataSearch(self):
        self.name.setText("")
        self.stock.setText("")
        self.id = ""
        self.quantity =""  
        sv = self.searchv_2.text()     
        if sv=="":
            a=0
        else:      
            result = self.cur.execute("SELECT proadjust.id,products.name,products.id,proadjust.qtn,proadjust.type,proadjust.des,strftime('%d/%m/%Y',proadjust.date),users.name FROM proadjust INNER JOIN products ON proadjust.pid=products.id LEFT JOIN users ON proadjust.uid=users.id WHERE products.name LIKE ? OR products.id LIKE ? OR products.itemcode LIKE ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number,column_number, QTableWidgetItem(str(data)))

    def addS(self):
        name = self.name.text()
        id = self.id
        des = self.des.text()
        if(name=="" and id==""):
            QMessageBox.warning(None, ("Name Required"), 
            ("Product Name is Required"),
             QMessageBox.Cancel)
        elif self.qtn.text()=="":
            QMessageBox.warning(None, ("Required"), 
            ("Product Qtn is Required"),
             QMessageBox.Cancel)                  
        else:    
            qtns = float(self.qtn.text())
            selectdata = self.select()
            if selectdata=="Product Minus":
                proad = self.cur.execute("INSERT INTO proadjust(pid,qtn,des,type,uid)VALUES(?,?,?,?,?)",(self.id,qtns,des,selectdata,self.uid,))
                self.conn.commit()
                quantity = float(self.quantity)
                qtn = quantity-qtns
                result = self.cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn,id))
                self.conn.commit()
                if(result):
                    id = proad.lastrowid
                    query3 = ("Product Minus",self.id,id,self.uid,self.sale,qtns,)
                    self.cur.execute("INSERT INTO pledger(type,pid,adsujt_id,uid,price,qtn)VALUES(?,?,?,?,?,?)",query3)
                    self.conn.commit()                      
                    QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok) 
                else:
                    QMessageBox.information(None, ("Failed"), ("Data not added "),QMessageBox.Ok)     
                self.loadData()
                self.qtn.setText("0")
                self.des.setText("")
            if selectdata=="Product Increae":
                proad = self.cur.execute("INSERT INTO proadjust(pid,qtn,des,type,uid)VALUES(?,?,?,?,?)",(self.id,qtns,des,selectdata,self.uid,))
                self.conn.commit()
                quantity = float(self.quantity)
                qtn = quantity+qtns
                result = self.cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn,id))
                self.conn.commit()
                if(result):
                    id = proad.lastrowid
                    query3 = ("Product Increase",self.id,id,self.uid,self.sale,qtns,)
                    self.cur.execute("INSERT INTO pledger(type,pid,adsujt_id,uid,price,qtn)VALUES(?,?,?,?,?,?)",query3)
                    self.conn.commit()                     
                    QMessageBox.information(None, ("Successful"), ("Data added successfully"),QMessageBox.Ok) 
                else:
                    QMessageBox.information(None, ("Failed"), ("Data not added "),QMessageBox.Ok)     
                self.loadData()
                self.qtn.setText("0")
                self.des.setText("")

    def search(self):
        sv = self.searchv.text()    
        if sv=="":
            self.name.setText("")
            self.stock.setText("")
            self.id = ""
            self.quantity =""
            self.sale="0"
        else:    
            result = self.cur.execute("SELECT id,name,unit,qtn,buyrate FROM products WHERE id LIKE ? OR name LIKE ? ",("%"+sv+"%","%"+sv+"%",))
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
        
    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(2)
        pid = NewInd.data()  
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(3)
        qtn = NewInd.data()    
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(4)
        type = NewInd.data()              
        res = self.cur.execute("SELECT id,qtn FROM products WHERE id=?",(pid,))
        data = res.fetchone()              
        reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row"),QMessageBox.Yes,QMessageBox.No) 
        if(reply == QMessageBox.Yes):          
            if type=="Product Minus":
                if id=="":
                    QMessageBox.warning(None, ("Warning"), ("Please select any row"),QMessageBox.Ok)
                else:   
                    qtn = float(qtn) 
                    self.cur.execute("DELETE FROM proadjust WHERE id=?",(id,))
                    self.conn.commit()
                    quantity = float(data[1])
                    qtn = quantity+qtn
                    result = self.cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn,pid))
                    self.conn.commit()
                    if(result):
                        self.cur.execute("DELETE FROM pledger WHERE adsujt_id=?",(id,))
                        self.conn.commit()                          
                        QMessageBox.information(None, ("Successful"), ("Data Delete successfully"),QMessageBox.Ok) 
                    else:
                        QMessageBox.information(None, ("Failed"), ("Data not Delete "),QMessageBox.Ok)     
                    self.loadData()
            if type=="Product Increae":
                if id=="":
                    QMessageBox.warning(None, ("Warning"), ("Please select any row"),QMessageBox.Ok)
                else:        
                    qtn = float(qtn)         
                    self.cur.execute("DELETE FROM proadjust WHERE id=?",(id,))
                    self.conn.commit()                
                    quantity = float(data[1])
                    qtn = quantity-qtn
                    result = self.cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn,pid))
                    self.conn.commit()
                    if(result):
                        self.cur.execute("DELETE FROM pledger WHERE adsujt_id=?",(id,))
                        self.conn.commit()                                                 
                        QMessageBox.information(None, ("Successful"), ("Data Deleted successfully"),QMessageBox.Ok) 
                    else:
                        QMessageBox.information(None, ("Failed"), ("Data not added "),QMessageBox.Ok)     
                    self.loadData()  

    def select(self):
        if(self.minus.isChecked()):
            return "Product Minus"      
        if(self.plus.isChecked()):
            return "Product Increae" 

