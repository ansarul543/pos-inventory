import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3
from customerbalance import CustomerBalance
bal = CustomerBalance()

class CustomerReturn(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/customerreturn.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Sales Return")
        self.uid = uid
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        date = QDate.currentDate()
        self.dateEdit.setDate(date)
        self.fromd.setDate(date)
        self.tod.setDate(date)          
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.sale.setValidator(self.onlynumber)
        self.qtn.setValidator(self.onlynumber)
        self.discount_p.setValidator(self.onlynumber)    
        self.paid.setValidator(self.onlynumber)   
        self.sv.textChanged.connect(self.searchCustomer)
        self.pv.textChanged.connect(self.searchP)
        self.cid =""
        self.pricep="0"          
        self.wholesalep="0"
        self.pid=""
        self.retail.clicked.connect(self.selectDataOnChange)
        self.wholesale.clicked.connect(self.selectDataOnChange)
        self.qtn.textChanged.connect(self.changeD)
        self.discount_p.textChanged.connect(self.changeD)
        self.ppercent.stateChanged.connect(self.changeD)
        self.ppercentamount="0"        
        self.stockshow.setAlignment(QtCore.Qt.AlignRight)
        self.discount_p.setAlignment(QtCore.Qt.AlignRight)
        self.qtn.setAlignment(QtCore.Qt.AlignRight)
        self.sale.setAlignment(QtCore.Qt.AlignRight)
        self.paid.setAlignment(QtCore.Qt.AlignRight)
        self.itemvalue.setAlignment(QtCore.Qt.AlignRight)
        self.additemb.clicked.connect(self.submitB)
        self.tableWidget.setHorizontalHeaderLabels(["ID","Product Name","Price","Qtn","Discount","Total Amount","Return Cash Amount","Prepared By","Date"])
        self.deleteb.clicked.connect(self.deletebD)
        self.allb.clicked.connect(self.allData)
        self.searchv_2.textChanged.connect(self.searchD)
        self.viewb.clicked.connect(self.loadDataDate)        

    def allData(self):
        self.loadDa()
    def deletebD(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        cur = self.conn.cursor()
        if id==None:
            QMessageBox.warning(None, ("Warning"), ("Please Select Any row column"),QMessageBox.Ok)
        else:
            data = cur.execute("SELECT * FROM sreturn WHERE id=?",(id,))
            data1 = data.fetchone()
            qtns = float(data1[4])
            pro = cur.execute("SELECT id,qtn FROM products WHERE id=?",(data1[2],))
            prodata = pro.fetchone()
            pid = prodata[0]
            qtn = float(prodata[1])
            totalqtn = qtn-qtns  
            reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected invoice row"),QMessageBox.Yes,QMessageBox.No) 
            if(reply == QMessageBox.Yes):    
                result = self.cur.execute("DELETE FROM sreturn WHERE id=?",(id,))
                self.conn.commit()
                if result:
                    cur.execute("UPDATE products SET qtn=? WHERE id=?",(totalqtn,pid,))
                    self.conn.commit()
                    cur.execute("DELETE FROM sss WHERE return_id=?",(id,))
                    self.conn.commit()     
                    cur.execute("DELETE FROM pledger WHERE sreturn_id=?",(id,))
                    self.conn.commit()                                     
                    self.loadDa()
                    QMessageBox.information(None, ("Success"), ("Sales Return Delete success"),QMessageBox.Ok)   
                else:
                    QMessageBox.information(None, ("Failed"), ("Sales Return Delete Failed"),QMessageBox.Ok)  
        cur.close()            

    def loadDa(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT sreturn.id,sreturn.price,sreturn.qtn,sreturn.discount,sreturn.paid,products.unit,products.name,strftime('%d/%m/%Y',sreturn.date),users.name FROM sreturn INNER JOIN products ON sreturn.pid=products.id LEFT JOIN users ON sreturn.uid=users.id ORDER BY sreturn.id DESC")
        data = result.fetchall()
        self.tableWidget.setRowCount(len(data))
        for index,i in enumerate(data):
            price = float(i[1])
            qtn = float(i[2])
            total = price*qtn
            dis = float(i[3])
            totalamount = total-dis
            self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[6]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(str(i[2] +" "+i[5])))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[3]))
            self.tableWidget.setItem(index,5,QTableWidgetItem(str(totalamount)))
            self.tableWidget.setItem(index,6,QTableWidgetItem(i[4]))
            self.tableWidget.setItem(index,7,QTableWidgetItem(i[8]))
            self.tableWidget.setItem(index,8,QTableWidgetItem(i[7]))
        cur.close()    

    def searchD(self):
        sv = self.searchv_2.text()
        cur = self.conn.cursor()
        if sv=="":
            a=0
        else:
            result = cur.execute("SELECT sreturn.id,sreturn.price,sreturn.qtn,sreturn.discount,sreturn.paid,products.unit,products.name,strftime('%d/%m/%Y',sreturn.date),users.name FROM sreturn INNER JOIN products ON sreturn.pid=products.id LEFT JOIN users ON sreturn.uid=users.id WHERE products.name LIKE ? OR products.id LIKE ?",("%"+sv+"%","%"+sv+"%",))
            data = result.fetchall()
            self.tableWidget.setRowCount(len(data))
            for index,i in enumerate(data):
                price = float(i[1])
                qtn = float(i[2])
                total = price*qtn
                dis = float(i[3])
                totalamount = total-dis
                self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
                self.tableWidget.setItem(index,1,QTableWidgetItem(i[6]))
                self.tableWidget.setItem(index,2,QTableWidgetItem(i[1]))
                self.tableWidget.setItem(index,3,QTableWidgetItem(str(i[2] +" "+i[5])))
                self.tableWidget.setItem(index,4,QTableWidgetItem(i[3]))
                self.tableWidget.setItem(index,5,QTableWidgetItem(str(totalamount)))
                self.tableWidget.setItem(index,6,QTableWidgetItem(i[4]))
                self.tableWidget.setItem(index,7,QTableWidgetItem(i[8]))   
                self.tableWidget.setItem(index,8,QTableWidgetItem(i[7]))
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
            result = cur.execute("SELECT sreturn.id,sreturn.price,sreturn.qtn,sreturn.discount,sreturn.paid,products.unit,products.name,strftime('%d/%m/%Y',sreturn.date),users.name FROM sreturn INNER JOIN products ON sreturn.pid=products.id LEFT JOIN users ON sreturn.uid=users.id WHERE sreturn.date BETWEEN ? AND ?",(fromd,tod,))
            data = result.fetchall()
            self.tableWidget.setRowCount(len(data))
            for index,i in enumerate(data):
                price = float(i[1])
                qtn = float(i[2])
                total = price*qtn
                dis = float(i[3])
                totalamount = total-dis
                self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
                self.tableWidget.setItem(index,1,QTableWidgetItem(i[6]))
                self.tableWidget.setItem(index,2,QTableWidgetItem(i[1]))
                self.tableWidget.setItem(index,3,QTableWidgetItem(str(i[2] +" "+i[5])))
                self.tableWidget.setItem(index,4,QTableWidgetItem(i[3]))
                self.tableWidget.setItem(index,5,QTableWidgetItem(str(totalamount)))
                self.tableWidget.setItem(index,6,QTableWidgetItem(i[4]))
                self.tableWidget.setItem(index,7,QTableWidgetItem(i[8])) 
                self.tableWidget.setItem(index,8,QTableWidgetItem(i[7]))            
        else:
            result = cur.execute("SELECT sreturn.id,sreturn.price,sreturn.qtn,sreturn.discount,sreturn.paid,products.unit,products.name,strftime('%d/%m/%Y',sreturn.date),users.name FROM sreturn INNER JOIN products ON sreturn.pid=products.id LEFT JOIN users ON sreturn.uid=users.id WHERE products.name LIKE ? OR products.id LIKE ? and sreturn.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%",fromd,tod,))
            data = result.fetchall()
            self.tableWidget.setRowCount(len(data))
            for index,i in enumerate(data):
                price = float(i[1])
                qtn = float(i[2])
                total = price*qtn
                dis = float(i[3])
                totalamount = total-dis
                self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
                self.tableWidget.setItem(index,1,QTableWidgetItem(i[6]))
                self.tableWidget.setItem(index,2,QTableWidgetItem(i[1]))
                self.tableWidget.setItem(index,3,QTableWidgetItem(str(i[2] +" "+i[5])))
                self.tableWidget.setItem(index,4,QTableWidgetItem(i[3]))
                self.tableWidget.setItem(index,5,QTableWidgetItem(str(totalamount)))
                self.tableWidget.setItem(index,6,QTableWidgetItem(i[4]))
                self.tableWidget.setItem(index,7,QTableWidgetItem(i[8])) 
                self.tableWidget.setItem(index,8,QTableWidgetItem(i[7])) 
        cur.close()        

    def submitB(self):
        qtn = self.qtn.text()
        paid = self.paid.text()
        sale = self.sale.text()
        discount_p = self.discount_p.text()
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')     
        date_current = self.dateEdit.date() 
        date = date_current.toString("yyyy-MM-dd")
        dateandtime = date+" "+currenttime        
        cur = self.conn.cursor()
        if self.cid=="":
            QMessageBox.warning(None, ("Warning"), ("Customer is required"),QMessageBox.Ok)
        elif self.pid=="":
            QMessageBox.warning(None, ("Warning"), ("Product is required"),QMessageBox.Ok)    
        elif qtn=="" or qtn=="0" and self.discount_p.text()=="" :
            QMessageBox.warning(None, ("Warning"), ("Quantity not be Empty and Discount not be empty"),QMessageBox.Ok)    
        elif qtn=="0":
            QMessageBox.warning(None, ("Warning"), ("Quantity not be 0 "),QMessageBox.Ok)              
        elif paid=="":
            QMessageBox.warning(None, ("Warning"), ("Paid from cash not be  Empty"),QMessageBox.Ok) 
        else:
            pdata = cur.execute("SELECT id,qtn FROM products WHERE id=?",(self.pid,))
            pdata2 = pdata.fetchone()
            pid = pdata2[0]
            qtnp = float(pdata2[1])
            totalqtn = qtnp+float(qtn)
            pp = self.selectPercentPro()
            if pp=="1":
                query = (self.cid,self.pid,sale,qtn,self.ppercentamount,paid,dateandtime,self.uid,discount_p,)
                result = cur.execute("INSERT INTO sreturn(cid,pid,price,qtn,discount,paid,date,uid,discount_percent) VALUES(?,?,?,?,?,?,?,?,?)",query) 
                self.conn.commit()     
                if result:
                    id = result.lastrowid
                    cur.execute("UPDATE products SET qtn=? WHERE id=?",(totalqtn,pid,))   
                    self.conn.commit()  
                    cur.execute("INSERT INTO sss(type,return_id,cid,date,uid)VALUES(?,?,?,?,?)",("RETURN",id,self.cid,dateandtime,self.uid,))
                    self.conn.commit()  
                    query3 = ("Sales Return",self.pid,id,self.cid,self.uid,sale,qtn,self.ppercentamount,discount_p,)
                    cur.execute("INSERT INTO pledger(type,pid,sreturn_id,cid,uid,price,qtn,dicount,discount_percent)VALUES(?,?,?,?,?,?,?,?,?)",query3)
                    self.conn.commit()                     
                    self.refreshD()
                    self.loadDa()
                    QMessageBox.information(None, ("Success"), ("Sales Return success"),QMessageBox.Ok)   
                else:
                    QMessageBox.information(None, ("Failed"), ("Sales Return Failed"),QMessageBox.Ok)    
            else:
                query = (self.cid,self.pid,sale,qtn,discount_p,paid,dateandtime,self.uid,"0",)
                result = cur.execute("INSERT INTO sreturn(cid,pid,price,qtn,discount,paid,date,uid,discount_percent) VALUES(?,?,?,?,?,?,?,?,?)",query) 
                self.conn.commit()     
                if result:
                    id = result.lastrowid
                    cur.execute("UPDATE products SET qtn=? WHERE id=?",(totalqtn,pid,))   
                    self.conn.commit()  
                    cur.execute("INSERT INTO sss(type,return_id,cid,date,uid)VALUES(?,?,?,?,?)",("RETURN",id,self.cid,dateandtime,self.uid,))
                    self.conn.commit()  
                    query3 = ("Sales Return",self.pid,id,self.cid,self.uid,sale,qtn,discount_p,"0",)
                    cur.execute("INSERT INTO pledger(type,pid,sreturn_id,cid,uid,price,qtn,dicount,discount_percent)VALUES(?,?,?,?,?,?,?,?,?)",query3)
                    self.conn.commit()                     
                    self.refreshD()
                    self.loadDa()
                    QMessageBox.information(None, ("Success"), ("Sales Return success"),QMessageBox.Ok)   
                else:
                    QMessageBox.information(None, ("Failed"), ("Sales Return Failed"),QMessageBox.Ok)   
            cur.close()                               

    def refreshD(self):
        self.pn.setText("")  
        self.pid =""  
        self.unit.setText("")
        self.sale.setText("")
        self.pricep="0"
        self.sale.setText("0")
        self.wholesalep="0"       
        self.itemvalue.setText("")    
        self.qtn.setText("0")
        self.discount_p.setText("0")
        self.stockshow.setText("0")
        self.paid.setText("0")
        self.cid=""
        self.cn.setText("")
        self.mobile.setText("")
        self.cdue.setText("")
        self.ppercentamount="0"

    def changeD(self):
        self.itemTotal()

    def selectDataOnChange(self):
        if(self.retail.isChecked()):
            self.sale.setText(self.pricep)  
            self.itemTotal()                 
        if(self.wholesale.isChecked()):
            self.sale.setText(self.wholesalep)
            self.itemTotal()
         
    def selectDataOnChange(self):
        if(self.retail.isChecked()):
            self.sale.setText(self.pricep)  
            self.itemTotal()  
            
        if(self.wholesale.isChecked()):
            self.sale.setText(self.wholesalep)
            self.itemTotal()

    def selectPercentPro(self):
        if(self.ppercent.isChecked()):
            return "1"     
        else:
            return "0" 

    def itemTotal(self):
        if self.sale.text()=="":
            sale = self.sale.text()
        if self.discount_p.text()=="":
            sale = self.sale.text()            
        elif self.qtn.text()=="":
            qtn = self.qtn.text()
        else:    
            if self.ppercent.isChecked():
                stockshow = float(self.stockshow.text())
                sale = float(self.sale.text())
                qtn = float(self.qtn.text())    
                discount_p = float(self.discount_p.text())
                total = qtn*sale 
                pay = total*discount_p/100
                self.ppercentamount=pay
                v = total-pay
                self.itemvalue.setText(str(v))
                self.paid.setText(str(v))
                if qtn<=stockshow:
                    ok = stockshow
                else:
                    self.qtn.setText(str(stockshow))
                    QMessageBox.warning(None, ("Warning"), ("Quantity must be Smaller then From Stocks"),QMessageBox.Ok)
            else:    
                stockshow = float(self.stockshow.text())
                sale = float(self.sale.text())
                qtn = float(self.qtn.text())    
                discount_p = float(self.discount_p.text())
                total = qtn*sale 
                pay = total-discount_p
                self.ppercentamount=discount_p
                self.itemvalue.setText(str(pay))
                self.paid.setText(str(pay))
                if qtn<=stockshow:
                    ok = stockshow
                else:
                    self.qtn.setText(str(stockshow))
                    QMessageBox.warning(None, ("Warning"), ("Quantity must be Smaller then From Stocks"),QMessageBox.Ok)

    def searchP(self):
        value = self.pv.text()
        cur = self.conn.cursor()
        if value=="":
            value = value
            self.pn.setText("")  
            self.pid =""  
            self.unit.setText("") 
            self.stockshow.setText("")
            self.sale.setText("0")
            self.pricep="0"
            self.wholesalep="0"
            self.ppercentamount="0"
        else:
            result = cur.execute("SELECT * FROM products WHERE name LIKE ? OR id LIKE ? OR barcode LIKE ? ",("%"+value+"%","%"+value+"%","%"+value+"%",))
            data = result.fetchone()
            if data:
                self.pn.setText(data[1])
                self.pid = data[0]
                self.unit.setText(data[4])
                self.stockshow.setText(data[8])
                self.itemTotal()
                self.pricep=data[6]
                self.wholesalep=data[7]
                self.ppercentamount="0"
                if self.retail.isChecked():
                    self.sale.setText(data[6])
                    self.itemTotal()
                if self.wholesale.isChecked():
                    self.sale.setText(data[7])    
                    self.itemTotal()
            else:
                self.pn.setText("")  
                self.pid =""  
                self.unit.setText("")
                self.stockshow.setText("")
                self.sale.setText("")
                self.pricep="0"
                self.sale.setText("0")
                self.wholesalep="0"       
                self.itemvalue.setText("")    
                self.qtn.setText("0")
                self.discount_p.setText("0")
                self.paid.setText("0")
                self.ppercentamount="0"
        cur.close()        


    def searchCustomer(self):
        value = self.sv.text()
        cur = self.conn.cursor()
        if value!="":
            result = cur.execute("SELECT * FROM customer WHERE name LIKE ? OR id LIKE ? ",("%"+value+"%","%"+value+"%",))
            data = result.fetchone()
            if data:
                self.cn.setText(data[1])
                self.cid = data[0]
                due = bal.bal(data[0])
                self.mobile.setText(data[3])
                self.cdue.setText(str(due))
            else:
                self.cn.setText("")  
                self.cid ="" 
                self.mobile.setText("") 
                self.cdue.setText("")
        cur.close()        


