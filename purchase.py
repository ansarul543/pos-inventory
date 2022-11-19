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
#sys.setrecursionlimit(5000)
print(sys.getrecursionlimit())
from supplierbalance import SupplierBalance
balsup = SupplierBalance()



class Purchases(QWidget):
    def __init__(self,uid='',role='',parent=None):
        super().__init__()
        uic.loadUi('./ui/purchase1.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Purchase Entry")
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.conn = sqlite3.connect('./database/data.db')
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())
        self.cur = self.conn.cursor()
        self.uid = uid
        self.tableWidget.setHorizontalHeaderLabels(["Product Name","Buy Price","Qtn","Value","Discount","Total"])
        self.invoice.setText(str(random.randint(10000, 100000)))
        date = QDate.currentDate()
        self.dateEdit.setDate(date)
        self.dateEdit.dateChanged.connect(self.onDateChanged)
        self.pv.textChanged.connect(self.searchP)
        self.sv.textChanged.connect(self.searchSupplier)
        self.onlynumber = QDoubleValidator(0.00,99.99,10)
        self.buy.setValidator(self.onlynumber)
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
        self.labour.setAlignment(QtCore.Qt.AlignRight)
        self.discount_p.setAlignment(QtCore.Qt.AlignRight)
        self.discount.setAlignment(QtCore.Qt.AlignRight)
        self.qtn.setAlignment(QtCore.Qt.AlignRight)
        self.buy.setAlignment(QtCore.Qt.AlignRight)
        self.sale.setAlignment(QtCore.Qt.AlignRight)
        self.itemvalue.setAlignment(QtCore.Qt.AlignRight)
        self.wholesale.setAlignment(QtCore.Qt.AlignRight)
        self.previousdue.setAlignment(QtCore.Qt.AlignRight)
        self.totalpp.setAlignment(QtCore.Qt.AlignRight)

        self.purchaseb.clicked.connect(self.submitData)
        self.paid.textChanged.connect(self.paidData)
        self.vat.textChanged.connect(self.vatData)
        self.labour.textChanged.connect(self.labourData)
        self.discount.textChanged.connect(self.discountData)
        self.dpercent.stateChanged.connect(self.discountData)
        self.qtn.textChanged.connect(self.itemTotal)
        self.discount_p.textChanged.connect(self.itemTotal)
        self.buy.textChanged.connect(self.itemTotal)
        self.pid =""
        self.sid =""
        self.data=[]
        self.loadData()
        self.loadData2()
        self.disd="0"

        self.additemb.clicked.connect(self.addItem)
        self.clearb.clicked.connect(self.clearWindow)
        self.textEdit.hide()
        self.vatpercent="0"
        self.saveonlyb.clicked.connect(self.saveonly)
        self.ppercent.stateChanged.connect(self.itemTotal)


    def itemTotal(self):
        if self.buy.text()=="":
            buy = self.buy.text()
        elif self.qtn.text()=="":
            qtn = self.qtn.text()
        else:    
            buy = float(self.buy.text())
            qtn = float(self.qtn.text())    
            total = qtn*buy 
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

    def clearWindow(self):
        self.close()
        self.win = Purchases()
        self.win.show()

    def paidData(self):
        self.loadData()
        self.loadData2()
    def vatData(self):
        self.loadData()
        self.loadData2()
    def labourData(self):
        self.loadData()
        self.loadData2()
    def discountData(self):
        self.loadData()
        self.loadData2()

    def saveonly(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')
        stype = self.select()
        sid = self.sid
        invoice = self.invoice.text()
        date_current = self.dateEdit.date() 
        date = date_current.toString("yyyy-MM-dd")
        dateandtime = date+" "+currenttime
        paid = self.paid.text()
        vat = self.vat.text()
        labour = self.labour.text()
        discount = self.discount.text()
        total = self.grand.text()
        address = ""
        previousdue = self.previousdue.text()
        paribahan = ""
        discountpd = self.discountPercent()

        if sid=="" and self.sn.text()=="":
            QMessageBox.warning(None, ("Required"), 
            ("Supplier Name is Required"),
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
                query = (stype,sid,total,invoice,vat,labour,self.disd,paid,dateandtime,self.uid,address,paribahan,previousdue,)
                result = self.cur.execute("INSERT INTO pinvoice(stype,sid,total,invoice,vat,labour,discount,paid,date,uid,area,paribahan,previus_due)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",query)
                self.conn.commit()
                if result:                   
                    id = result.lastrowid
                    for i in self.data:
                        pid = i["pid"]
                        query2 = (sid,pid,id,i["qtn"],i["buy"],i["sale"],invoice,i["discount_p"],dateandtime,i["wholesale"],self.uid,i["ppercent"],)
                        dd = self.cur.execute("INSERT INTO purchase(sid,pid,pinvoice_id,qtn,buy_rate,sale_rate,invoice,discount,date,wholesale,uid,discountpercent)VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",query2)
                        self.conn.commit()
                        purchaseid = dd.lastrowid
                        result2 = self.cur.execute("SELECT * FROM products WHERE id=?",(pid,)) 
                        data = result2.fetchone()
                        qtns = data[8]
                        qtn2 = float(qtns)+float(i["qtn"])
                        buy2 = i["buy"]
                        sale = i["sale"]
                        wholesale=i["wholesale"]
                        self.cur.execute("UPDATE products SET buyrate=?,salerate=?,wholesale=?,qtn=? WHERE id=?",(buy2,sale,wholesale,qtn2,pid,))
                        self.conn.commit()
                        query3 = ("Purchase",pid,purchaseid,sid,self.uid,i["buy"],i["qtn"],i["discount_p"],i["ppercent"],)
                        self.cur.execute("INSERT INTO pledger(type,pid,purcchase_id,sid,uid,price,qtn,dicount,discount_percent)VALUES(?,?,?,?,?,?,?,?,?)",query3)
                        self.conn.commit()                        
                    self.cur.execute("INSERT INTO ppp(type,invoice_id,sid,date,uid)VALUES(?,?,?,?,?)",("PURCHASE",id,sid,dateandtime,self.uid,))
                    self.conn.commit()       
                    QMessageBox.information(None, ("Successful"), ("Data added and saved successfully"),QMessageBox.Ok) 
                   
                    self.data=[]    
                    self.loadData()
                    self.invoice.setText(str(random.randint(10000, 100000)))
                    self.paid.setText("0")
                    self.labour.setText("0")
                    self.vat.setText("0")
                    self.discount.setText("0")      
                    self.wholesale.setText("0")     
                    self.vatpercent="0"    
    
                else:
                    QMessageBox.warning(None, ("Failed"), ("Data not saved try again"),QMessageBox.Ok)        
            else:
                QMessageBox.warning(None, ("Required"), ("Product item is required"),QMessageBox.Ok)     


    def submitData(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')
        stype = self.select()
        sid = self.sid
        invoice = self.invoice.text()
        date_current = self.dateEdit.date() 
        date = date_current.toString("yyyy-MM-dd")
        dateandtime = date+" "+currenttime
        paid = self.paid.text()
        vat = self.vat.text()
        labour = self.labour.text()
        discount = self.discount.text()
        total = self.grand.text()
        address = ""
        previousdue = self.previousdue.text()
        paribahan = ""
        discountpd = self.discountPercent()

        if sid=="" and self.sn.text()=="":
            QMessageBox.warning(None, ("Required"), 
            ("Supplier Name is Required"),
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
                query = (stype,sid,total,invoice,vat,labour,self.disd,paid,dateandtime,self.uid,address,paribahan,previousdue,)
                result = self.cur.execute("INSERT INTO pinvoice(stype,sid,total,invoice,vat,labour,discount,paid,date,uid,area,paribahan,previus_due)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",query)
                self.conn.commit()
                if result:                   
                    id = result.lastrowid
                    for i in self.data:
                        pid = i["pid"]
                        query2 = (sid,pid,id,i["qtn"],i["buy"],i["sale"],invoice,i["discount_p"],dateandtime,i["wholesale"],self.uid,i["ppercent"],)
                        dd = self.cur.execute("INSERT INTO purchase(sid,pid,pinvoice_id,qtn,buy_rate,sale_rate,invoice,discount,date,wholesale,uid,discountpercent)VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",query2)
                        self.conn.commit()
                        purchaseid = dd.lastrowid
                        result2 = self.cur.execute("SELECT * FROM products WHERE id=?",(pid,)) 
                        data = result2.fetchone()
                        qtns = data[8]
                        qtn2 = float(qtns)+float(i["qtn"])
                        buy2 = i["buy"]
                        sale = i["sale"]
                        wholesale=i["wholesale"]
                        self.cur.execute("UPDATE products SET buyrate=?,salerate=?,wholesale=?,qtn=? WHERE id=?",(buy2,sale,wholesale,qtn2,pid,))
                        self.conn.commit()
                        query3 = ("Purchase",pid,purchaseid,sid,self.uid,i["buy"],i["qtn"],i["discount_p"],i["ppercent"],)
                        self.cur.execute("INSERT INTO pledger(type,pid,purcchase_id,sid,uid,price,qtn,dicount,discount_percent)VALUES(?,?,?,?,?,?,?,?,?)",query3)
                        self.conn.commit()                          
                    self.cur.execute("INSERT INTO ppp(type,invoice_id,sid,date,uid)VALUES(?,?,?,?,?)",("PURCHASE",id,sid,dateandtime,self.uid,))
                    self.conn.commit() 
                    QMessageBox.information(None, ("Successful"), ("Data added and saved successfully"),QMessageBox.Ok) 
                    s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
                    setting = s.fetchone()
                    invoiced = self.cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,supplier.address,supplier.phone,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total,supplier.id as sid,pinvoice.previus_due,pinvoice.area,pinvoice.paribahan,pinvoice.status  FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id WHERE pinvoice.invoice=?",(invoice,))   
                    invoicedata = invoiced.fetchone()
                    result = self.cur.execute("SELECT purchase.invoice,strftime('%d/%m/%Y',purchase.date),supplier.name as sname,products.name as pname,purchase.buy_rate,purchase.qtn,products.unit,purchase.discount,purchase.discountpercent FROM purchase INNER JOIN supplier ON purchase.sid=supplier.id INNER JOIN products ON purchase.pid=products.id  WHERE purchase.invoice=?",(invoice,))
                    datas = result.fetchall() 
                    value = 0
                    for index, i in enumerate(datas):
                        total = float(i[5])*float(i[4])
                        totalv = total-float(i[7])
                        value+=float(totalv)
                    with open("html/purchaseinvoice.html") as file:
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
                    self.wholesale.setText("0")  
                    self.vatpercent="0" 
              
                else:
                    QMessageBox.warning(None, ("Failed"), ("Data not saved try again"),QMessageBox.Ok)        
            else:
                QMessageBox.warning(None, ("Required"), ("Product item is required"),QMessageBox.Ok)     

    def print_preview(self, printer):
        self.textEdit.print_(printer) 

    def select(self):
        if(self.stype.currentText()=="Local"):
            return "Local"      
        if(self.stype.currentText()=="Foreign"):
            return "Foreign" 

    def selectPercentPro(self):
        if(self.ppercent.isChecked()):
            return "1"     
        else:
            return "0"    
    def discountPercent(self):
        if(self.dpercent.isChecked()):
            return "1"     
        else:
            return "0" 

    def addItem(self):
        pid = self.pid
        pn = self.pn.text()
        unit = self.unit.text()
        qtn = self.qtn.text()
        buy = self.buy.text()
        sale = self.sale.text()
        ppercent = self.selectPercentPro()
        wholesale = self.wholesale.text()
        discount_p = self.discount_p.text()
        if(pid=="" and pn==""):
            QMessageBox.warning(None, ("Required"), 
            ("Product Name is Required"),
             QMessageBox.Ok)
        elif(buy=="" or sale=="" or qtn=="" or discount_p==""):
            QMessageBox.warning(None, ("All 0 field is Required"), 
            ("All 0 Zero field not be empty minimum 0 is required"),
             QMessageBox.Ok)  
        else:
            if ppercent=="1":
                buys = float(buy)
                qtns = float(qtn) 
                total = qtns*buys
                di = float(discount_p)
                t = total*di/100
                v = total-t
                data = {"pid":pid,"pname":pn,"unit":unit,"qtn":qtn,"buy":buy,"sale":sale,"discount_p":t,"wholesale":wholesale,"ppercent":discount_p}  
                self.data.append(data)
            else:
                data = {"pid":pid,"pname":pn,"unit":unit,"qtn":qtn,"buy":buy,"sale":sale,"discount_p":discount_p,"wholesale":wholesale,"ppercent":"0"}  
                self.data.append(data)                          
            self.pid=""
            self.pn.setText("")
            self.unit.setText("")
            self.qtn.setText("0")
            self.buy.setText("0")
            self.sale.setText("0")
            self.discount_p.setText("0")  
            self.pv.setText("")
            self.wholesale.setText("0")
            self.showstocks.setText(str(""))
            self.loadData()
            self.loadData2()

    def loadData2(self):
        value = 0
        for index, i in enumerate(self.data):
            total = float(i["buy"]) * float(i["qtn"])
            totalv = total - float(i["discount_p"])
            value+=float(totalv)          
        if self.discount.text()=="" or self.vat.text()=="" or self.labour.text()=="" or self.paid.text()=="":
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

    def loadData(self):
        self.tableWidget.setRowCount(len(self.data))
        value = 0
        for index, i in enumerate(self.data):
            total = float(i["buy"]) * float(i["qtn"])
            totalv = total - float(i["discount_p"])
            value+=float(totalv)     
            self.tableWidget.setItem(index,0,QTableWidgetItem(i["pname"]))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i["buy"]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(str(total)))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i["qtn"]+" "+i["unit"]))
            self.tableWidget.setItem(index,4,QTableWidgetItem(str(i["discount_p"])))    
            self.tableWidget.setItem(index,5,QTableWidgetItem(str(totalv)))        

    def removeData(self):
        NewInd = self.tableWidget.currentIndex()
        if len(self.data)>0 and NewInd.row()!=-1:
            self.data.pop(NewInd.row())
            print(NewInd.row())
            self.loadData()
            self.loadData2()

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
        if value !="":
            result = self.cur.execute("SELECT * FROM products WHERE name LIKE ? OR id LIKE ? OR barcode LIKE ? OR itemcode LIKE ? ",("%"+value+"%","%"+value+"%","%"+value+"%","%"+value+"%",))
            data = result.fetchone()
            if data:
                self.pn.setText(str(data[1]))
                self.pid = data[0]
                self.unit.setText(data[4])
                self.buy.setText(data[5])
                self.sale.setText(data[6])
                self.wholesale.setText(data[7])
                self.showstocks.setText(str(data[8]))
                self.vatpercent=data[9]
                playsound('./audio/mixit.mp3') 
            else:
                self.pn.setText("")  
                self.pid =""  
                self.unit.setText("")
                self.buy.setText("0")
                self.sale.setText("0")
                self.wholesale.setText("0")  
                self.showstocks.setText(str(""))     
                self.vatpercent="0"         
        else:
            self.pn.setText("")  
            self.pid =""  
            self.unit.setText("")    
            self.buy.setText("0")
            self.sale.setText("0")
            self.wholesale.setText("0")
            self.showstocks.setText(str(""))       
            self.vatpercent="0"          

    def searchSupplier(self):
        value = self.sv.text()
        if value!="":
            result = self.cur.execute("SELECT * FROM supplier WHERE name LIKE ? OR id LIKE ? OR partycode LIKE ? ",("%"+value+"%","%"+value+"%","%"+value+"%",))
            data = result.fetchone()
            if data:
                self.sn.setText(data[1])
                self.sid = data[0]
                bal = balsup.bal(data[0])
                self.previousdue.setText(str(bal))
            else:
                self.sn.setText("")  
                self.sid =""  
                self.previousdue.setText("0")
        else:
            self.sn.setText("")  
            self.sid =""  
            self.previousdue.setText("0")        



