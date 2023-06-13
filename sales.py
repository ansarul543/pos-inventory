import sys
from playsound import playsound
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3
import random
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 
import requests

from customerbalance import CustomerBalance
balcus = CustomerBalance()

class Sales(QWidget):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/sales1.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Sales Entry")
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.uid = uid
        self.tableWidget.setHorizontalHeaderLabels(["Product Name","Sale Price","Qtn","Value","Discount","Total"])
        self.invoice.setText(str(random.randint(10000, 100000)))
        date = QDate.currentDate()
        self.dateEdit.setDate(date)
        self.dateEdit.dateChanged.connect(self.onDateChanged)
        self.pv.textChanged.connect(self.searchP)
        self.sv.textChanged.connect(self.searchCustomer)
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.sale.setValidator(self.onlynumber)
        self.qtn.setValidator(self.onlynumber)
        self.discount_p.setValidator(self.onlynumber)
        self.paid.setValidator(self.onlynumber)
        self.vat.setValidator(self.onlynumber)
        self.labour.setValidator(self.onlynumber)
        self.discount.setValidator(self.onlynumber)
        self.deleteb.clicked.connect(self.removeData)
        self.paidtext.setAlignment(QtCore.Qt.AlignRight)
        self.grand.setAlignment(QtCore.Qt.AlignRight)
        self.less.setAlignment(QtCore.Qt.AlignRight)
        self.total.setAlignment(QtCore.Qt.AlignRight)
        self.paid.setAlignment(QtCore.Qt.AlignRight)
        self.vat.setAlignment(QtCore.Qt.AlignRight)
        self.stockshow.setAlignment(QtCore.Qt.AlignRight)
        self.labour.setAlignment(QtCore.Qt.AlignRight)
        self.discount_p.setAlignment(QtCore.Qt.AlignRight)
        self.discount.setAlignment(QtCore.Qt.AlignRight)
        self.qtn.setAlignment(QtCore.Qt.AlignRight)
        self.sale.setAlignment(QtCore.Qt.AlignRight)
        self.previousdue.setAlignment(QtCore.Qt.AlignRight)
        self.totalpp.setAlignment(QtCore.Qt.AlignRight)        
        self.itemvalue.setAlignment(QtCore.Qt.AlignRight)
        self.purchaseb.clicked.connect(self.submitData)
        self.paid.textChanged.connect(self.paidData)
        self.vat.textChanged.connect(self.vatData)
        self.labour.textChanged.connect(self.labourData)
        self.discount.textChanged.connect(self.discountData)
        self.qtn.textChanged.connect(self.itemTotal)
        self.discount_p.textChanged.connect(self.itemTotal)
        self.comboproduct.addItem("Products")
        self.combocustomer.addItem("Customers")        
        self.pid =""
        self.cid ="0"
        self.roles=role
        self.data=[]
        self.loadData()
        self.additemb.clicked.connect(self.addItem)
        self.clearb.clicked.connect(self.clearWindow)
        self.pricep ="0"
        self.wholesalep="0"
        self.stype.currentTextChanged.connect(self.selectDataOnChange)
        self.textEdit.hide()
        self.saveonlyb.clicked.connect(self.saveonly)
        self.smsapi()
        self.automsg=""
        self.msg=""
        self.vatpercent="0"
        self.disd="0"
        self.ppercent.stateChanged.connect(self.itemTotal)
        self.discountpercent.stateChanged.connect(self.discountData)
        self.peoductsData()
        self.comboproduct.currentIndexChanged.connect(self.productDataChange)
        self.cussData()
        self.combocustomer.currentIndexChanged.connect(self.cussDataChange)

    def cussData(self):
        data = self.cur.execute("SELECT * FROM customer")
        result = data.fetchall()
        for i in result:
            self.combocustomer.addItem(str(i[0])+" , "+i[1])
    def cussDataChange(self):
        d = self.combocustomer.currentText()
        x = d.split(", ")
        if(len(x)>1):
            self.sv.setText(x[0])     
            cur = self.conn.cursor() 
            result = cur.execute("SELECT * FROM customer WHERE id=?",(x[0],))
            data = result.fetchone()
            if data:
                self.cn.setText(data[1])
                self.sid = data[0]
                bal = balcus.bal(data[0])
                self.previousdue.setText(str(bal))
                self.caddress.setText(data[6])
            else:
                self.cn.setText("")  
                self.cid =""  
                self.previousdue.setText("0")
                self.caddress.setText("")
            cur.close()    
        else:
           self.sv.setText("")      
           self.searchCustomer()  

    def peoductsData(self):
        data = self.cur.execute("SELECT * FROM products")
        result = data.fetchall()
        for i in result:
            self.comboproduct.addItem(str(i[0])+" , "+i[1])
    def productDataChange(self):
        da = self.comboproduct.currentText()  
        y = da.split(", ")
        if(len(y)>1):
           self.pv.setText(y[0])  
           self.searchP()    
        else:
            self.pv.setText("")   
            self.searchP() 

    def smsapi(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT * FROM bulksetting WHERE id=? ",(1,))
        if(result):
            data = result.fetchone()
            api = data[1]
            username = data[2]
            password = data[3]
            number = data[4]
            self.automsg=data[5]
            self.msg=data[6]
            url = f"{api}?username={username}&password={password}&number={number}&message=Test"
            cur.close()
            return url

    def selectDataOnChange(self):
        stype = self.stype.currentText()
        if(stype=="Retail"):
            self.sale.setText(self.pricep)  
            self.itemTotal()  
            self.loadData()                 
        if(stype=="Wholesale"):
            self.sale.setText(self.wholesalep)
            self.itemTotal()
            self.loadData()

    def itemTotal(self):
        stockshow = 0
        if(self.stockshow.text()!=""):
            stockshow=float(self.stockshow.text())
        if self.sale.text()=="":
            sale = self.sale.text()
        elif self.qtn.text()=="":
            qtn = self.qtn.text()
        else:    
            sale = float(self.sale.text())
            qtn = float(self.qtn.text())    
            total = qtn*sale 
            total2 = str(total)
            self.itemvalue.setText(str(total2))
            if self.discount_p.text()=="":
                self.totalpp.setText(str(total2))
            else:
                if self.ppercent.isChecked():
                    di = float(self.discount_p.text())
                    t = total*di/100
                    v = total-t
                    self.totalpp.setText(str(v))  
                else:
                    di = float(self.discount_p.text())
                    t = total-di
                    self.totalpp.setText(str(t))   
            if qtn<=stockshow:
                ok = stockshow
            else:
                self.qtn.setText(str(stockshow))
                QMessageBox.warning(None, ("Warning"), ("Quantity must be Smaller then From Stocks"),QMessageBox.Ok)

    def clearWindow(self):
        self.close()
        self.win = Sales()
        self.win.show()

    def paidData(self):
        self.loadData()
    def vatData(self):
        self.loadData()
    def labourData(self):
        self.loadData()
    def discountData(self):
        self.loadData()

    def saveonly(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')
        stype = self.select()
        cid = self.cid
        invoice = self.invoice.text()
        date_current = self.dateEdit.date() 
        date = date_current.toString("yyyy-MM-dd")
        dateandtime = date+" "+currenttime
        paid = self.paid.text()
        vat = self.vat.text()
        labour = self.labour.text()
        discount = self.discount.text()
        total = self.grand.text()
        paytype = self.paytype.currentText()
        previousdue = self.previousdue.text()
        addressarea = ""
        paribahan = "" 
        discountpd = self.discountPercent()

        phone = self.mobile.text()
        name = self.cn.text()
        url = self.smsapi()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        cur = self.conn.cursor()
        if cid=="" and self.cn.text()=="":
            QMessageBox.warning(None, ("Required"), 
            ("Customer Name is Required"),
             QMessageBox.Ok)
        elif invoice=="":
            QMessageBox.warning(None, ("Required"), 
            ("Invoice number not be empty . please fill "),
             QMessageBox.Ok)             
        elif paid=="" or vat=="" or labour=="" or discount=="":
            QMessageBox.warning(None, ("All 0 field is Required"), 
            ("All 0 Zero field not be empty minimum 0 is required"),
             QMessageBox.Ok)                   
        else:
            if len(self.data)>0:
                query = (cid,total,invoice,vat,labour,self.disd,paid,paytype,dateandtime,self.uid,addressarea,paribahan,previousdue,)
                result = cur.execute("INSERT INTO sinvoice(cid,total,invoice,vat,labour,discount,paid,paytype,date,uid,area,paribahan,previus_due)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",query)
                self.conn.commit()
                if result:
                    id = result.lastrowid
                    for i in self.data:
                        pid = i["pid"]
                        query2 = (cid,pid,id,i["qtn"],i["sale"],i["type"],invoice,i["discount_p"],dateandtime,self.uid,i["ppercent"],i["vatpercent"],)
                        dd = cur.execute("INSERT INTO sales(cid,pid,sinvoice_id,qtn,price,type,invoice,discount,date,uid,discountpercent,vatpercent)VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",query2)
                        self.conn.commit()
                        salesid = dd.lastrowid
                        result2 = cur.execute("SELECT * FROM products WHERE id=?",(pid,)) 
                        data = result2.fetchone()
                        qtns = data[8]
                        qtn2 = float(qtns)-float(i["qtn"])
                        cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn2,pid,))
                        self.conn.commit()
                        query3 = ("Sales",pid,salesid,cid,self.uid,i["sale"],i["qtn"],i["discount_p"],i["ppercent"],)
                        cur.execute("INSERT INTO pledger(type,pid,sales_id,cid,uid,price,qtn,dicount,discount_percent)VALUES(?,?,?,?,?,?,?,?,?)",query3)
                        self.conn.commit()                          
                    cur.execute("INSERT INTO sss(type,invoice_id,cid,date,uid)VALUES(?,?,?,?,?)",("SALES",id,cid,dateandtime,self.uid,))
                    self.conn.commit()   
                    if self.automsg=="1":
                        try:
                            payload  = {"number":phone,
                            "message": f" Hi {name}, \n your invoice {invoice} amount {total} Taka paid amount {paid} Taka \n {self.msg}"}
                            response = requests.request("POST", url, headers=headers, data = payload)       
                        except:
                            error=0                    
                    QMessageBox.information(None, ("Successful"), ("Data added and saved successfully"),QMessageBox.Ok)  
                    self.data=[]    
                    self.loadData()
                    self.invoice.setText(str(random.randint(10000, 100000)))
                    self.paid.setText("0")
                    self.labour.setText("0")
                    self.vat.setText("0")
                    self.discount.setText("0")  
                    self.combocustomer.setCurrentText("Customers")       
                    cur.close()                                
                else:
                    QMessageBox.warning(None, ("Failed"), ("Data not saved try again"),QMessageBox.Ok)        
            else:
                QMessageBox.warning(None, ("Required"), ("Product item is required"),QMessageBox.Ok)     
           
    def submitData(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')
        stype = self.select()
        cid = self.cid
        invoice = self.invoice.text()
        date_current = self.dateEdit.date() 
        date = date_current.toString("yyyy-MM-dd")
        dateandtime = date+" "+currenttime
        paid = self.paid.text()
        vat = self.vat.text()
        labour = self.labour.text()
        discount = self.discount.text()
        total = self.grand.text()
        paytype = self.paytype.currentText()
        previousdue = self.previousdue.text()
        addressarea = ""
        paribahan = "" 
        discountpd = self.discountPercent()
        phone = self.mobile.text()
        name = self.cn.text()
        url = self.smsapi()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}  
        cur = self.conn.cursor()      
        if cid=="" and self.cn.text()=="":
            QMessageBox.warning(None, ("Required"), 
            ("Customer Name is Required"),
             QMessageBox.Ok)
        elif invoice=="":
            QMessageBox.warning(None, ("Required"), 
            ("Invoice number not be empty . please fill "),
             QMessageBox.Ok)             
        elif paid=="" or vat=="" or labour=="" or discount=="":
            QMessageBox.warning(None, ("All 0 field is Required"), 
            ("All 0 Zero field not be empty minimum 0 is required"),
             QMessageBox.Ok)                   
        else:
            if len(self.data)>0:
                query = (cid,total,invoice,vat,labour,self.disd,paid,paytype,dateandtime,self.uid,addressarea,paribahan,previousdue,)
                result = cur.execute("INSERT INTO sinvoice(cid,total,invoice,vat,labour,discount,paid,paytype,date,uid,area,paribahan,previus_due)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",query)
                self.conn.commit()
                if result:
                    id = result.lastrowid
                    for i in self.data:
                        pid = i["pid"]
                        query2 = (cid,pid,id,i["qtn"],i["sale"],i["type"],invoice,i["discount_p"],dateandtime,self.uid,i["ppercent"],i["vatpercent"],)
                        dd = cur.execute("INSERT INTO sales(cid,pid,sinvoice_id,qtn,price,type,invoice,discount,date,uid,discountpercent,vatpercent)VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",query2)
                        self.conn.commit()
                        salesid = dd.lastrowid
                        result2 = cur.execute("SELECT * FROM products WHERE id=?",(pid,)) 
                        data = result2.fetchone()
                        qtns = data[8]
                        qtn2 = float(qtns)-float(i["qtn"])
                        cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn2,pid,))
                        self.conn.commit()
                        query3 = ("Sales",pid,salesid,cid,self.uid,i["sale"],i["qtn"],i["discount_p"],i["ppercent"],)
                        cur.execute("INSERT INTO pledger(type,pid,sales_id,cid,uid,price,qtn,dicount,discount_percent)VALUES(?,?,?,?,?,?,?,?,?)",query3)
                        self.conn.commit()                          
                    cur.execute("INSERT INTO sss(type,invoice_id,cid,date,uid)VALUES(?,?,?,?,?)",("SALES",id,cid,dateandtime,self.uid,))
                    self.conn.commit()   
                    if self.automsg=="1":
                        try:
                            payload  = {"number":phone,
                            "message": f" Hi {name}, \n your invoice {invoice} amount {total} Taka paid amount {paid} Taka \n {self.msg}"}
                            response = requests.request("POST", url, headers=headers, data = payload)        
                            print('ok')
                        except:
                            error=0        
                            print('error')                                   
                    QMessageBox.information(None, ("Successful"), ("Data added and saved successfully"),QMessageBox.Ok)  
                    s = cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
                    setting = s.fetchone()
                    invoiced = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,customer.address,customer.phone,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype,customer.id as cid,sinvoice.previus_due,sinvoice.area,sinvoice.paribahan,sinvoice.status FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id WHERE sinvoice.invoice=?",(invoice,))   
                    invoicedata = invoiced.fetchone()
                    result = cur.execute("SELECT sales.invoice,strftime('%d/%m/%Y',sales.date),customer.name as cname,products.name as pname,sales.price,sales.qtn,products.unit,sales.discount,sales.type,sales.vatpercent,sales.discountpercent FROM sales INNER JOIN customer ON sales.cid=customer.id INNER JOIN products ON sales.pid=products.id WHERE sales.invoice=?",(invoice,))
                    datas = result.fetchall() 
                    value = 0
                    for index, i in enumerate(datas):
                        total = float(i[5])*float(i[4])
                        totalv = total-float(i[7])
                        value+=float(totalv)
                    with open("html/salesinvoice.html") as file:
                        self.textEdit.setText(Template(file.read()).render( invoice=invoicedata,data=datas,setting=setting,total=value))

                    printer = QPrinter(QPrinter.HighResolution)
                    previewDialog = QPrintPreviewDialog(printer, self)
                    previewDialog.paintRequested.connect(self.print_preview)
                    previewDialog.exec_()                       
                    self.data=[]    
                    self.loadData()
                    self.invoice.setText(str(random.randint(10000, 100000)))
                    self.paid.setText("0")
                    self.labour.setText("0")
                    self.vat.setText("0")
                    self.discount.setText("0")   
                    self.combocustomer.setCurrentText("Customers") 
                    cur.close() 
                else:
                    QMessageBox.warning(None, ("Failed"), ("Data not saved try again"),QMessageBox.Ok)        
            else:
                QMessageBox.warning(None, ("Required"), ("Product item is required"),QMessageBox.Ok)     
   
    def print_preview(self, printer):
        self.textEdit.print_(printer) 

    def select(self):
        if(self.stype.currentText()=="Retail"):
            self.sale.setText(self.pricep)
            return "Retail"      
        if(self.stype.currentText()=="Wholesale"):
            self.sale.setText(self.wholesalep)
            return "Wholesale" 

    def selectPercentPro(self):
        if(self.ppercent.isChecked()):
            return "1"     
        else:
            return "0"    
    def discountPercent(self):
        if(self.discountpercent.isChecked()):
            return "1"     
        else:
            return "0" 

    def addItem(self):
        pid = self.pid
        pn = self.pn.text()
        unit = self.unit.text()
        qtn = self.qtn.text()
        sale = self.sale.text()
        discount_p = self.discount_p.text()
        type = self.select()
        ppercent = self.selectPercentPro()
        if(pid=="" and pn==""):
            QMessageBox.warning(None, ("Required"), 
            ("Product Name is Required"),
             QMessageBox.Ok)
        elif(sale=="" or qtn=="" or discount_p==""):
            QMessageBox.warning(None, ("All 0 field is Required"), 
            ("All 0 Zero field not be empty minimum 0 is required"),
             QMessageBox.Ok)  
        else:
            if ppercent=="1":
                sales = float(sale)
                qtns = float(qtn) 
                total = qtns*sales
                di = float(discount_p)
                t = total*di/100
                v = total-t            
                data = {"pid":pid,"pname":pn,"unit":unit,"type":type,"qtn":qtn,"sale":sale,"discount_p":t,"ppercent":discount_p,"vatpercent":self.vatpercent}  
                self.data.append(data)
            else:
                data = {"pid":pid,"pname":pn,"unit":unit,"type":type,"qtn":qtn,"sale":sale,"discount_p":discount_p,"ppercent":"0","vatpercent":self.vatpercent}  
                self.data.append(data)                    
            self.pid=""
            self.pn.setText("")
            self.unit.setText("")
            self.qtn.setText("0")
            self.sale.setText("0")
            self.discount_p.setText("0")  
            self.vatpercent="0"
            self.pv.setText("")
            self.stockshow.setText("0")
            self.comboproduct.setCurrentText("Products")
            self.loadData()


    def loadData(self):
        self.tableWidget.setRowCount(len(self.data))
        value = 0
        vattext = float(self.vat.text())
        vattext1=0
        for index, i in enumerate(self.data):
            total = float(i["sale"])* float(i["qtn"])
            totalv = total - float(i["discount_p"])
            value+=float(totalv)
            vatpercent = float(i["vatpercent"])
            v = totalv*vatpercent/100
            vattext1 +=v
            print(v)
            self.tableWidget.setItem(index,0,QTableWidgetItem(i["pname"]))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i["sale"]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i["qtn"]+" "+i["unit"]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(str(total)))
            self.tableWidget.setItem(index,4,QTableWidgetItem(str(i["discount_p"])))
            self.tableWidget.setItem(index,5,QTableWidgetItem(str(totalv)))
        self.vat.setText(str(vattext1))
        if self.discount.text()=="" or self.labour.text()=="" or self.paid.text()=="":
            a=0 
        else:      
            d = self.discountPercent()
            if d=="1":
                fvalue = value+float(self.vat.text())+float(self.labour.text())
                paid = float(self.paid.text())
                di = float(self.discount.text())
                t = fvalue*di/100
                self.disd = t
                grand = fvalue-t
                less = grand-paid                
                self.total.setText(str(fvalue))
                self.grand.setText(str(grand))
                self.paidtext.setText(str(paid))
                self.less.setText(str(less))
            else:                         
                fvalue = value+float(self.vat.text())+float(self.labour.text())
                paid = float(self.paid.text())
                grand = fvalue-float(self.discount.text())
                less = grand-paid
                self.disd=self.discount.text()
                self.total.setText(str(fvalue))
                self.grand.setText(str(grand))
                self.paidtext.setText(str(paid))
                self.less.setText(str(less))

    def removeData(self):
        NewInd = self.tableWidget.currentIndex()
        if len(self.data)>0 and NewInd.row()!=-1:
            self.data.pop(NewInd.row())
            print(NewInd.row())
            self.loadData()

    def onDateChanged(self, newDate):
        date = newDate.toString("yyyy-MM-dd")
        #print(date)
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')
        date_current = self.dateEdit.date() 
        date = date_current.toString("yyyy-MM-dd")
        #print(date+" "+currenttime)
    def searchP(self):
        value = self.pv.text()
        cur = self.conn.cursor()
        if value=="":
            value = value
            self.pn.setText("")  
            self.pid =""  
            self.unit.setText("") 
            self.stockshow.setText("")
            self.sale.setText("")
            self.pricep="0"
            self.wholesalep="0"
            self.vatpercent="0"
            self.qtn.setText("0")
        else:
            result = cur.execute("SELECT * FROM products WHERE id=? OR barcode=? OR name LIKE ? ",(value,value,"%"+value+"%",))
            data = result.fetchone()
            if data:
                self.pn.setText(data[1])
                self.pid = data[0]
                self.unit.setText(data[4])
                self.stockshow.setText(data[8])
                self.itemTotal()
                self.pricep=data[6]
                self.wholesalep=data[7]
                self.vatpercent=data[9]
                self.qtn.setText("1")
                if data[15]=="Fixed":
                    self.sale.setReadOnly(True)
                    self.discount_p.setReadOnly(True)
                    self.discount.setReadOnly(True)

                if self.stype.currentText()=="Retail":
                    self.sale.setText(data[6])
                    self.itemTotal()
                if self.stype.currentText()=="Wholesale":
                    self.sale.setText(data[7])    
                    self.itemTotal()   
                try:
                    #playsound('./audio/mixit.mp3')
                    print("Music ...")
                except:
                    print("Music Play Error")        
            else:
                self.pn.setText("")  
                self.pid =""  
                self.unit.setText("")
                self.stockshow.setText("0")
                self.sale.setText("")
                self.pricep="0"
                self.wholesalep="0"       
                self.vatpercent="0"    
                self.qtn.setText("0")
            cur.close()    


    def searchCustomer(self):
        value = self.sv.text()
        if value!="":
            cur = self.conn.cursor()
            result = cur.execute("SELECT * FROM customer WHERE name LIKE ? OR id LIKE ? OR partycode LIKE ? ",("%"+value+"%","%"+value+"%","%"+value+"%",))
            data = result.fetchone()
            if data:
                self.cn.setText(data[1])
                self.cid = data[0]
                bal = balcus.bal(data[0])
                self.mobile.setText(data[3])
                self.phone = data[3]
                self.previousdue.setText(str(bal))
                self.discount.setText(data[8])
                self.caddress.setText(data[6])
                self.discountpercent.setChecked(True)
                self.itemTotal()
            else:
                self.cn.setText("")  
                self.cid ="" 
                self.previousdue.setText("0")
                self.mobile.setText("")
                self.phone=""
                self.discountpercent.setChecked(False)
                self.discount.setText("0")
                self.caddress.setText("")
            cur.close()    
        else:
            self.cn.setText("")  
            self.cid ="" 
            self.previousdue.setText("0")
            self.mobile.setText("")
            self.phone="" 
            self.discountpercent.setChecked(False)
            self.discount.setText("0")
            self.caddress.setText("")



