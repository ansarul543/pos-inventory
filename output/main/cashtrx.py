import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 
import requests
import sqlite3
from cashmsg import CashMessage
from supplierbalance import SupplierBalance
balsup = SupplierBalance()

from customerbalance import CustomerBalance
balcus = CustomerBalance()

class CashTrx(QDialog):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/cashtrx.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Cash Transaction")
        self.uid = uid
        self.tableWidget.setHorizontalHeaderLabels(["ID","Date","Account Type","Payment Type","Description","In Amount","Out Amount","Prepared By"])
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.due.hide()
        self.textEdit.hide()
        self.acctype.currentTextChanged.connect(self.acctypeV)
        self.searchv.textChanged.connect(self.searchV)
        self.id =""
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.amount.setValidator(self.onlynumber)
        self.resetb.clicked.connect(self.resetall)
        self.saveb.clicked.connect(self.add)
        self.amount.setAlignment(QtCore.Qt.AlignRight)
        date = QDate.currentDate()
        self.date.setDate(date)
        self.fromd.setDate(date)
        self.tod.setDate(date)
        self.submitb.clicked.connect(self.paydate)
        self.printb.clicked.connect(self.printData)
        self.allb.clicked.connect(self.allData)
        self.msgb.clicked.connect(self.msgData)
        self.acctype.currentTextChanged.connect(self.trChange)
        self.smsapi()
        self.automsg=""
        self.msg=""
        self.label.hide()
        self.trtype.hide()        
    
    def trChange(self):
        type = self.acctype.currentText()
        if type=="Customer" or type=="Supplier":
            self.label.hide()
            self.trtype.hide()
            print(type)
        if type=="Official":
            self.label.show()
            self.trtype.show()  
            print(type)  

    def msgData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        type = self.tableWidget.currentIndex().siblingAtColumn(2)
        type = type.data()
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        if id is None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row to do print"),QMessageBox.Ok)
        elif type!="Customer":
            QMessageBox.warning(None, ("Warning"), ("Message Sent Allow Only Customer"),QMessageBox.Ok)
        else:
            self.ms = CashMessage(id)
            self.ms.show()

    def smsapi(self):
        result = self.cur.execute("SELECT * FROM bulksetting WHERE id=? ",(1,))
        if(result):
            data = result.fetchone()
            api = data[1]
            username = data[2]
            password = data[3]
            number = data[4]
            self.automsg=data[5]
            self.msg=data[7]
            url = f"{api}?username={username}&password={password}&number={number}&message=Test"
            return url

    def allData(self):
        self.loadData()
    def printData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        type = self.tableWidget.currentIndex().siblingAtColumn(2)
        type = type.data()
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        if id is None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row to do print"),QMessageBox.Ok)
        else:
            if type=="Customer":
                data = self.cur.execute("SELECT cash.type,cash.paytype,cash.amount,cash.des,strftime('%d/%m/%Y',cash.date),customer.name,cash.bankname,cash.chqnumber,cash.trxid FROM cash INNER JOIN customer ON cash.cid=customer.id WHERE cash.id=?",(id,))   
                invo = data.fetchone()
                with open("html/cashtrx.html") as file:
                    self.textEdit.setText(Template(file.read()).render(data=invo,setting=setting))                    
            if type=="Supplier":
                data = self.cur.execute("SELECT cash.type,cash.paytype,cash.amount,cash.des,strftime('%d/%m/%Y',cash.date),supplier.name,cash.bankname,cash.chqnumber,cash.trxid  FROM cash INNER JOIN supplier ON cash.sid=supplier.id WHERE cash.id=?",(id,))   
                invo = data.fetchone()
                with open("html/cashtrx.html") as file:
                    self.textEdit.setText(Template(file.read()).render(data=invo,setting=setting))                
            if type=="Official":
                data = self.cur.execute("SELECT cash.type,cash.paytype,cash.amount,cash.des,strftime('%d/%m/%Y',cash.date),account.name,cash.bankname,cash.chqnumber,cash.trxid  FROM cash INNER JOIN account ON cash.accid=account.id WHERE cash.id=?",(id,))   
                invo = data.fetchone()    
                with open("html/cashtrx.html") as file:
                    self.textEdit.setText(Template(file.read()).render(data=invo,setting=setting))       
            printer = QPrinter(QPrinter.HighResolution)
            previewDialog = QPrintPreviewDialog(printer, self)
            previewDialog.paintRequested.connect(self.print_preview)
            previewDialog.exec_()                                 
    
    def print_preview(self, printer):
        self.textEdit.print_(printer)  

    def loadData(self):
        self.cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),cash.type,cash.paytype,cash.des,cash.amount,users.name FROM cash LEFT JOIN users ON cash.uid=users.id ORDER BY cash.id DESC")
        data = self.cur.fetchall()
        self.tableWidget.setRowCount(len(data))
        amountin =0
        amountout=0
        for index, i in enumerate(data):
            self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(i[3]))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[4]))
            if i[3]=="Cash Receive" or i[3]=="Deposit":
                total = float(i[5])
                amountin+=float(total)
                self.tableWidget.setItem(index,5,QTableWidgetItem(i[5]))
            else:
                self.tableWidget.setItem(index,5,QTableWidgetItem("0.00"))    
            if i[3]=="Cash Payment" or i[3]=="Withdrew":
                total = float(i[5])
                amountout+=float(total)                
                self.tableWidget.setItem(index,6,QTableWidgetItem(i[5]))
            else:
                self.tableWidget.setItem(index,6,QTableWidgetItem("0.00"))  
            self.tableWidget.setItem(index,7,QTableWidgetItem(i[6]))    
        self.outamount.setText(str(amountout))       
        self.inamount.setText(str(amountin))     

    def paydate(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')

        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date

        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime           
        self.cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),cash.type,cash.paytype,cash.des,cash.amount,users.name FROM cash LEFT JOIN users ON cash.uid=users.id WHERE cash.date BETWEEN ? AND ? ORDER BY cash.id DESC",(fromd,tod,))
        data = self.cur.fetchall()
        self.tableWidget.setRowCount(len(data))
        amountin =0
        amountout=0
        for index, i in enumerate(data):
            self.tableWidget.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(i[3]))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[4]))
            if i[3]=="Cash Receive" or i[3]=="Deposit":
                total = float(i[5])
                amountin+=float(total)
                self.tableWidget.setItem(index,5,QTableWidgetItem(i[5]))
            else:
                self.tableWidget.setItem(index,5,QTableWidgetItem("0.00"))    
            if i[3]=="Cash Payment" or i[3]=="Withdrew":
                total = float(i[5])
                amountout+=float(total)                
                self.tableWidget.setItem(index,6,QTableWidgetItem(i[5]))
            else:
                self.tableWidget.setItem(index,6,QTableWidgetItem("0.00"))  
            self.tableWidget.setItem(index,7,QTableWidgetItem(i[6]))    
        self.outamount.setText(str(amountout))       
        self.inamount.setText(str(amountin)) 

    def add(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')

        date_current = self.date.date() 
        date = date_current.toString("yyyy-MM-dd")
        dateandtime = date+" "+currenttime
        
        typecheck = self.acctype.currentText()
        pay = self.trtype.currentText()
        accid = self.id
        name = self.name.text()
        des = self.des.text()
        amount = float(self.amount.text())
        bank = self.bank.text()
        check = self.check.text()
        trxid = self.trxid.text()
        url = self.smsapi()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'} 

        if typecheck=="Customer":           
            pays = "Cash Receive"
            result = self.cur.execute("SELECT id,phone FROM customer WHERE id=? ",(accid,))
            cdata = result.fetchone()
            query = (typecheck,pays,accid,name,amount,des,dateandtime,self.uid,bank,check,trxid,)
            if self.id == "" and name=="":
                QMessageBox.warning(None, ("Warning"), ("Customer name is required"),QMessageBox.Ok)
            elif amount=="":
                QMessageBox.warning(None, ("Warning"), ("Amount not be empty"),QMessageBox.Ok)    
            else:
                if pays=="Cash Receive":
                    result = self.cur.execute("INSERT INTO cash(type,paytype,cid,accname,amount,des,date,uid,bankname,chqnumber,trxid)VALUES(?,?,?,?,?,?,?,?,?,?,?)",query)
                    self.conn.commit()
                    id = result.lastrowid
                    self.cur.execute("INSERT INTO sss(type,cash_id,cid,date,uid)VALUES(?,?,?,?,?)",("CASH",id,accid,dateandtime,self.uid,))
                    self.conn.commit()   
                    if self.automsg=="1":
                        try:
                            payload  = {"number":phone,
                            "message": f" Hi {name}, \n your payment amount {amount} Taka recieved  \n {self.msg}"}
                            response = requests.request("POST", url, headers=headers, data = payload)        
                            print('ok')
                        except:
                            error=0        
                            print('error')                                       
                    QMessageBox.information(None, ("Info"), ("Transaction success"),QMessageBox.Ok)
                    self.paydate()
                    self.resetall()
                elif pays=="Cash Payment":
                    QMessageBox.warning(None, ("Info"), ("Customer Cash Recieve Allow Only"),QMessageBox.Ok)
                         
        if typecheck=="Supplier":
            pays="Cash Payment"
            query = (typecheck,pays,accid,name,amount,des,dateandtime,self.uid,bank,check,trxid,)            
            if self.id == "" and name=="":
                QMessageBox.warning(None, ("Warning"), ("Supplier name is required"),QMessageBox.Ok)
            elif amount=="":
                QMessageBox.warning(None, ("Warning"), ("Amount not be empty"),QMessageBox.Ok)    
            else:
                if pays=="Cash Payment":
                    result = self.cur.execute("INSERT INTO cash(type,paytype,sid,accname,amount,des,date,uid,bankname,chqnumber,trxid)VALUES(?,?,?,?,?,?,?,?,?,?,?)",query)
                    self.conn.commit()
                    id = result.lastrowid
                    self.cur.execute("INSERT INTO ppp(type,cash_id,sid,date,uid)VALUES(?,?,?,?,?)",("CASH",id,accid,dateandtime,self.uid,))
                    self.conn.commit()                     
                    QMessageBox.information(None, ("Info"), ("Transaction success"),QMessageBox.Ok)
                    self.loadData()
                    self.resetall()
                elif pays=="Cash Receive":
                    QMessageBox.warning(None, ("Info"), ("Supplier Cash Payment Allow Only"),QMessageBox.Ok)     


        if typecheck=="Official":        
            query = (typecheck,pay,accid,name,amount,des,dateandtime,self.uid,bank,check,trxid,)            
            if self.id == "" and name=="":
                QMessageBox.warning(None, ("Warning"), ("Official name is required"),QMessageBox.Ok)
            elif amount=="":
                QMessageBox.warning(None, ("Warning"), ("Amount not be empty"),QMessageBox.Ok)    
            else:
                if pay=="Cash Receive" or pay=="Deposit":
                    self.cur.execute("INSERT INTO cash(type,paytype,accid,accname,amount,des,date,uid,bankname,chqnumber,trxid)VALUES(?,?,?,?,?,?,?,?,?,?,?)",query)
                    self.conn.commit()
                    cus = self.cur.execute("SELECT id,val FROM account WHERE id=?",(accid,))
                    data = cus.fetchone()
                    due = float(data[1])
                    totaldue = due+amount
                    self.cur.execute("UPDATE account SET val=? WHERE id=?",(totaldue,accid,))
                    self.conn.commit()
                    QMessageBox.information(None, ("Info"), ("Transaction success"),QMessageBox.Ok)
                    self.loadData()
                    self.resetall()
                elif pay=="Cash Payment" or pay=="Withdrew":
                    self.cur.execute("INSERT INTO cash(type,paytype,accid,accname,amount,des,date,uid,bankname,chqnumber,trxid)VALUES(?,?,?,?,?,?,?,?,?,?,?)",query)
                    self.conn.commit()
                    cus = self.cur.execute("SELECT id,val FROM account WHERE id=?",(accid,))
                    data = cus.fetchone()
                    due = float(data[1])
                    totaldue = due-amount
                    self.cur.execute("UPDATE account SET val=? WHERE id=?",(totaldue,accid,))
                    self.conn.commit()
                    QMessageBox.information(None, ("Info"), ("Transaction success"),QMessageBox.Ok)     
                    self.loadData()
                    self.resetall()


    def resetall(self):
        self.id =""
        self.searchv.setText("")
        self.name.setText("")
        self.amount.setText("0")
        self.bank.setText("")
        self.check.setText("")
        self.trxid.setText("")
        self.due.hide() 
        self.paydate() 

    def searchV(self):
        typecheck = self.acctype.currentText()
        sv = self.searchv.text()
        if typecheck=="Customer":
            if sv!="":
                self.cur.execute("SELECT id,name FROM customer WHERE id LIKE ? OR name LIKE ? OR partycode LIKE ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
                data = self.cur.fetchone()
                if data:
                    self.name.setText(data[1])
                    bal = balcus.bal(data[0])
                    self.duev.setText(str(bal))
                    self.id = data[0]
                    self.due.show()
                else:
                    self.name.setText("")
                    self.duev.setText("")
                    self.id = ""
                    self.due.hide()                       
            else:
                self.name.setText("")
                self.duev.setText("")   
                self.id=""    
                self.due.hide()              
        if typecheck=="Supplier":
            if sv!="":
                self.cur.execute("SELECT id,name FROM supplier WHERE id LIKE ? OR name LIKE ? OR partycode LIKE ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
                data = self.cur.fetchone()
                if data:
                    self.name.setText(data[1])
                    bal = balsup.bal(data[0])
                    self.duev.setText(str(bal))
                    self.id = data[0]
                    self.due.show()
                else:
                    self.name.setText("")
                    self.duev.setText("")
                    self.id = ""
                    self.due.hide()                       
            else:
                self.name.setText("")
                self.duev.setText("")   
                self.id=""    
                self.due.hide() 
        if typecheck=="Official":
            if sv!="":
                self.cur.execute("SELECT id,name FROM account WHERE id LIKE ? OR name LIKE ?",("%"+sv+"%","%"+sv+"%",))
                data = self.cur.fetchone()
                if data:
                    self.name.setText(data[1])
                    self.id = data[0]
                    self.due.hide()
                else:
                    self.name.setText("")
                    self.id = ""
                    self.due.hide()                       
            else:
                self.name.setText("")
                self.id=""    
                self.due.hide()     

    def acctypeV(self):
        self.id =""
        self.searchv.setText("")
        self.name.setText("")
        self.amount.setText("0")
        self.due.hide() 
        value = self.acctype.currentText()
         
        
     




