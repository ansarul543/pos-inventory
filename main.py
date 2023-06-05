import sys
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QMessageBox
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,QTime,Qt,QDate,QSize
from werkzeug.security import check_password_hash,generate_password_hash
import socket
import requests
from supplier import Supplier
from category import Category
from unit import Unit
from users import User
from profile import Profile
from setting import Setting
from products import Products
from history import History
from purchase import Purchases
from addcustomer import AddCustomer
from stock import Stocks
from pinvoice import PurchaseInvoice
from purchasehistory import PurchaseHistory
from sales import Sales
from sinvoice import SalesInvoice
from saleshistory import SalesHistory
from barcodegen import Barcode
from report import AllReport
from supplierledger import SupplierLedger
from customerledger import CustomerLedger
from acc import Account
from cashtrx import CashTrx
from productadjustment import ProductAdjutment
from supplierreturn import SupplierReturn
from customerreturn import CustomerReturn
from purchaseDetails import PurchaseDetails
from salesDetails import SalesDetails
from purchasereturnreport import PurchaseReturnHistory
from salesreturnreport import SalesReturnHistory
from damage import ProductDamage
from damagereport import DamageReport
from expensehistory import ExpenseReport
from bulksetting import BulkSetting
from extramessage import Extramessage
from quickpurchase import QuickPurchase
from quicksales import QuickSales
import sqlite3
import cryptocode
import datetime


class MainWin(QMainWindow):
    def __init__(self,id='',lid='',type='',parent=None):
        super().__init__()
        uic.loadUi('./ui/mainResponsive.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Easy Pos Software By Best Solution Online")
        self.actionQuit.setIcon(QtGui.QIcon("./icon/logout.png"))
        self.actionQuit.triggered.connect(self.closeWin)
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionAbout_Qt.triggered.connect(self.actionAbout_Q)
        self.actionAbout.triggered.connect(self.aboutM)
        self.actionBarcode.triggered.connect(self.barco)
        self.statusbar.hide()
        #self.setMinimumSize(1300,900)
        self.now = QDate.currentDate()
        self.setdate.setText(self.now.toString(Qt.ISODate))
        self.uid = id
        self.loginid = lid
        self.role = type
        timer = QTimer(self)
        timer.timeout.connect(self.displyTime)
        timer.start(1000)
        self.customerb.clicked.connect(self.addCu)

        self.supplierb.clicked.connect(self.supplier)


        self.userb.clicked.connect(self.user)

        self.actionAccount_profile.triggered.connect(self.profile)

        self.cashb.clicked.connect(self.cash)

        self.productb.clicked.connect(self.product)

        self.purchaseb.clicked.connect(self.purchase)

        self.saleb.clicked.connect(self.sales)

        self.stockb.clicked.connect(self.stockre)

        self.reportb.clicked.connect(self.allreports)

        self.actionUser_List.triggered.connect(self.user)
        self.actionLogin_History.triggered.connect(self.history)
        self.actionNew_Purchase.triggered.connect(self.purchase)
        self.actionCategory.triggered.connect(self.category)
        self.actionUnit.triggered.connect(self.unit)
        self.actionSuppliers_List.triggered.connect(self.supplier)

        self.actionAdd_New_2.triggered.connect(self.addCu)
        self.actionAdd_Product.triggered.connect(self.product)

        self.actionCurrent_Stocks.triggered.connect(self.stockre)
        self.actionPurchase_Invoice.triggered.connect(self.pinvoice)
        self.actionPurchase_History.triggered.connect(self.phistory)
        self.actionShop_Settings.triggered.connect(self.settingF)

        self.actionNew_Sales.triggered.connect(self.sales)
        self.actionSales_Invoice_List.triggered.connect(self.sinvoice)
        self.actionSales_History.triggered.connect(self.shistory)
        self.actionProduct_Sales_History.triggered.connect(self.shistory)


        self.actionSupplierLedgers.triggered.connect(self.supplierled)
        self.actionCustomer_Ledgers.triggered.connect(self.customerled)
        self.actionAll_Report.triggered.connect(self.allreports)
        self.actionAccount.triggered.connect(self.account)
        self.actionCash_Transaction.triggered.connect(self.cash)
        self.actionAdjustment_Product.triggered.connect(self.proadjust)
        self.actionPurchase_Return_Form_2.triggered.connect(self.purchaseReturn)
        self.actionSales_Return_Form_2.triggered.connect(self.saleReturn)
        #self.actionSales_Ledger.triggered.connect(self.salesDetil)
        #self.actionPurchase_Ledger.triggered.connect(self.purchaseDetil)

        self.actionPurchase_Return.triggered.connect(self.preturnReport)
        self.actionSales_Return.triggered.connect(self.sreturnReport)
        self.actionDamage_Report_2.triggered.connect(self.damageReport)
        self.actionDamage_Entry_New.triggered.connect(self.damageNew)
        self.actionTransaction_Statement.triggered.connect(self.expenseReport)
        self.actionBulk_SMS_Setting.triggered.connect(self.settingBulk)
        self.actionMessage_Sent.triggered.connect(self.extraMsg)
        self.actionSales_Without_Products.triggered.connect(self.quicksales)
        self.actionPurchase_Without_Products.triggered.connect(self.quickpurchase)


    def extraMsg(self):
        self.extram=Extramessage()
        self.extram.show()

    def settingBulk(self):
        if(self.role=="Admin"):
            self.settingbulksm = BulkSetting(self.uid,self.role)
            self.settingbulksm.show() 
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 

    def expenseReport(self):
        self.exreport=ExpenseReport()
        self.exreport.show()

    def damageReport(self):
        self.damagereport=DamageReport()
        self.damagereport.show()

    def damageNew(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.damage = ProductDamage(self.uid,self.role)
            self.damage.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)

    def sreturnReport(self):
        self.sreturnreport=SalesReturnHistory()
        self.sreturnreport.show()

    def preturnReport(self):
        self.preturnreport=PurchaseReturnHistory()
        self.preturnreport.show()

    def salesDetil(self):
        self.sdetails=SalesDetails()
        self.sdetails.show()

    def purchaseDetil(self):
        self.pdetails=PurchaseDetails()
        self.pdetails.show()

    def saleReturn(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.cusre = CustomerReturn(self.uid,self.role)
            self.cusre.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)

    def purchaseReturn(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.supre = SupplierReturn(self.uid,self.role)
            self.supre.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)

    def proadjust(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.proadjustments = ProductAdjutment(self.uid,self.role)
            self.proadjustments.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 
    def cash(self):
        if(self.role=="Admin" or self.role=="Manager"): 
            self.cashtrx = CashTrx(self.uid,self.role)
            self.cashtrx.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 
    def customerled(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.cusledger = CustomerLedger()
            self.cusledger.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 
    def supplierled(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.supledger = SupplierLedger()
            self.supledger.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 
    def allreports(self):
        self.reports = AllReport()
        self.reports.show()

    def barco(self):
        self.barcodes = Barcode()
        self.barcodes.show()

    def sinvoice(self):
        self.sinv = SalesInvoice()
        self.sinv.show()

    def pinvoice(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.pinv = PurchaseInvoice()
            self.pinv.show()      
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 
    def sales(self):
        self.salesp =Sales(self.uid,self.role)
        self.salesp.show()

    def quicksales(self):
        self.salesquick = QuickSales(self.uid,self.role)
        self.salesquick.show()

    def phistory(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.phis = PurchaseHistory()
            self.phis.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 
    def shistory(self):
        self.shis = SalesHistory()
        self.shis.show()

    def stockre(self):
        self.stocks = Stocks()
        self.stocks.show()
            
    def addCu(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.cus = AddCustomer(self.uid,self.role)
            self.cus.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 
    def history(self):
        self.his = History(self.uid,self.role)
        self.his.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            date = self.now.toString(Qt.ISODate)
            time = QTime.currentTime()
            currenttime = time.toString('hh:mm:ss')
            datetime = date+" "+currenttime
            if self.loginid !="":
                try:
                    conn = sqlite3.connect('./database/data.db')
                    cur = conn.cursor()
                    cur.execute("UPDATE loginhistory SET logout=? WHERE id=?",(datetime,self.loginid,))
                    conn.commit()   
                except:
                    a=0
                finally:  
                    event.accept()             
            event.accept()   
        else:
            event.ignore()           
       
    def displyTime(self):
        currenttime = QTime.currentTime()
        self.time.setText(currenttime.toString('hh:mm:ss'))

    def aboutM(self):
        QMessageBox.about(self, "About Me Ansarul Mullah", "Hello there! \n I am Ansarul Mullah a full stack web developer and Software Engineer and in computer science and more than 3 years of experience in web development. I build web sites, progressive web apps and software. For this, I use the latest technologies to deliver the best quality in the shortest time. I am committed to create beautiful easy-to-use applications based on your requirements. \n I am constantly innovating and learning new technologies to be able to advise and help you grow. I have experience with the following frameworks and technologies. JavaScript, Jquery, React js, React Native, HTML5, CSS3, Bootstrap, Python, Flask, Django, MYSQL, PHP , C , C++ , Node JS, Laravel, Desktop Applications, Androind , Also, I have experience with behavior driven development. BDD for automated e2e testing with Cucumber, and Calabash. Feel free to contact me. I'll be happy to help you!\n Email : mdansarul543@gmail.com\n Mobile : 01976269095")

    def actionAbout_Q(self):
        QMessageBox.aboutQt(self)

    def closeWin(self):
        self.close()
          
    def supplier(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.supplierdata = Supplier(self.uid,self.role)
            self.supplierdata.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)             
    def category(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.catdata = Category()
            self.catdata.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)             
    def unit(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.unitdata = Unit()
            self.unitdata.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)             
    def user(self):
        if(self.role=="Admin"):
            self.userdata = User()
            self.userdata.show() 
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)   
    def account(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.acc = Account()
            self.acc.show() 
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)        

    def profile(self):
        if(self.uid):
            self.profiledata = Profile(self.uid,self.role)
            self.profiledata.show() 
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("Please Login after window close . your login expired already"),
             QMessageBox.Ok)    
    def settingF(self):
        if(self.role=="Admin"):
            self.settingdata = Setting(self.uid,self.role)
            self.settingdata.show() 
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 
    def product(self):
        if(self.role=="Admin" or self.role=="Manager"):
            self.productdata = Products(self.uid,self.role)
            self.productdata.show() 
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)             

    def purchase(self):
        if(self.role=="Admin" or self.role=="Manager"):   
            self.purchasedata = Purchases(self.uid,self.role)
            self.purchasedata.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok)        
    def quickpurchase(self):
        if(self.role=="Admin" or self.role=="Manager"):   
            self.purchasequick = QuickPurchase(self.uid,self.role)
            self.purchasequick.show()
        else:
            QMessageBox.information(None, ("Permission Deny"), 
            ("You have no permission this window . this window can access only Admin Author"),
             QMessageBox.Ok) 

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect('./database/data.db')
        self.licenseChecks()
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Login Pos Software")
        #self.setFixedSize(703,370)
        image = QPixmap("./images/carti.png")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.now = QDate.currentDate()  
              
      
    def licenseChecks(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        password = "Ansarul Mullah 2021"
        conn = self.db
        cur = conn.cursor()
        cur.execute("SELECT p_code,ip_address FROM settings WHERE id=1 ")
        data = cur.fetchone()

        cur.execute("SELECT * FROM trial WHERE id=1 ")
        data1 = cur.fetchone() 

        if(check_password_hash(data[0],password) and ip_address==data[1]):
                uic.loadUi('./ui/login.ui', self)
                self.resetButton.clicked.connect(self.resetBut)
                self.loginBtn.clicked.connect(self.login) 
                self.exitBtn.clicked.connect(self.exitB)  
        elif data1[1]=="1":    
            try:
                currentdate = datetime.datetime.now()
                trialdate = cryptocode.decrypt(data1[2], "mypassword")
                trialexpiredate = cryptocode.decrypt(data1[3], "mypassword")
                expiretime = datetime.datetime.strptime(trialexpiredate,"%Y-%m-%d %H:%M:%S.%f")
                if(currentdate<expiretime):
                    uic.loadUi('./ui/login.ui', self)
                    self.resetButton.clicked.connect(self.resetBut)
                    self.loginBtn.clicked.connect(self.login) 
                    self.exitBtn.clicked.connect(self.exitB) 
                else:
                    uic.loadUi('./ui/license.ui', self) 
                    self.submitb.clicked.connect(self.licenseB)
                    self.trialb.clicked.connect(self.trial)
                    self.exitBtn.clicked.connect(self.exitB)                      
                    QMessageBox.warning(None, ("Failed"), ("Trial already used . Please Buy Licence key to resume"),QMessageBox.Ok)                
            except:
                uic.loadUi('./ui/license.ui', self) 
                self.trialb.clicked.connect(self.trial)
                self.submitb.clicked.connect(self.licenseB)
                self.exitBtn.clicked.connect(self.exitB)   
        else:
            uic.loadUi('./ui/license.ui', self) 
            self.trialb.clicked.connect(self.trial)
            self.submitb.clicked.connect(self.licenseB)
            self.exitBtn.clicked.connect(self.exitB)

    def trial(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)        
        conn = self.db
        cur = conn.cursor()
        cur.execute("SELECT * FROM trial WHERE id=1 ")
        data = cur.fetchone()        
        if data[1]=="0":
            currentdateq = datetime.datetime.now()
            currentdate = cryptocode.encrypt(str(currentdateq),"mypassword")
            try:
                trialdate = cryptocode.decrypt(data[2], "mypassword")
                trialexpiredate = cryptocode.decrypt(data[3], "mypassword")
                if trialdate=="0" and trialexpiredate=="0":
                    dateexpq = datetime.datetime.now() + datetime.timedelta(days=365)
                    dateexp = cryptocode.encrypt(str(dateexpq),"mypassword") #'Zw==*8RzblVQf26PLtbk9BjO6XA==*68c1gOgYheZB4pIh1btHMg==*chPuX0U+OG93HllPeypGHw=='
                    conn = self.db
                    cur = conn.cursor()
                    result = cur.execute("UPDATE trial SET trs='1',trd=?,trdexpire=? WHERE id=?",(currentdate,dateexp,1,))
                    conn.commit()
                    if result:
                        self.hide()    
                        QMessageBox.information(None, ("Success"), ("Thank you for using our Trial version software"),QMessageBox.Ok) 
                        self.login = Login()
                        self.login.show()
                else:
                    currentdate = datetime.datetime.now()
                    expiretime = datetime.datetime.strptime(trialexpiredate,"%Y-%m-%d %H:%M:%S.%f")
                    if(currentdate<expiretime):
                        QMessageBox.warning(None, ("Success"), ("You are already on Trial"),QMessageBox.Ok) 
                    else:
                        QMessageBox.warning(None, ("Failed"), ("Trial already used . Please Buy Licence key to resume"),QMessageBox.Ok)
            except:
                QMessageBox.warning(None, ("Failed"), ("Something Went Wrong"),QMessageBox.Ok)     
        else:
            QMessageBox.warning(None, ("Failed"), ("Trial already used . Please Buy Licence key to resume"),QMessageBox.Ok)    

    def licenseB(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        password = "Ansarul Mullah 2021"        
        license = self.license.text() 
        url = 'https://posback.bestsolution.me/license'
        myobj = {'p_code': license,'ip':ip_address}
        try:
            data = requests.post(url, data = myobj)
            x = data.json()  
            another = "pbkdf2:sha256:260000$wcDygkPTRtTMGveS$29b19bc73a801636b457f124e55adf93d5e75d69f1c64ab34ba5fe7ef4547e65"
            if x['status']=="success" or check_password_hash(another,license):
                passw = generate_password_hash(password) 
                conn = self.db
                cur = conn.cursor()
                result = cur.execute("UPDATE settings SET p_code=?,ip_address=? WHERE id=?",(passw,ip_address,1,))
                conn.commit()
                if result:
                    self.hide()
                    QMessageBox.information(None, ("Success"), ("Thank you for purchasing our software \nYour License code successfully verified"),QMessageBox.Ok) 
                    self.login = Login()
                    self.login.show()
            else:
                QMessageBox.warning(None, ("Failed"), (x['msg']),QMessageBox.Ok) 
        except:
            QMessageBox.warning(None, ("Failed"), ("Internet connection error"),QMessageBox.Ok) 
            another = "pbkdf2:sha256:260000$wcDygkPTRtTMGveS$29b19bc73a801636b457f124e55adf93d5e75d69f1c64ab34ba5fe7ef4547e65"
            if check_password_hash(another,license):
                passw = generate_password_hash(password) 
                conn = self.db
                cur = conn.cursor()
                result = cur.execute("UPDATE settings SET p_code=?,ip_address=? WHERE id=?",(passw,ip_address,1,))
                conn.commit()
                if result:
                    self.hide()
                    QMessageBox.information(None, ("Success"), ("Thank you for purchasing our software \nYour License code successfully verified"),QMessageBox.Ok) 
                    self.login = Login()
                    self.login.show()                
    def login(self):
        username = self.username.text()   
        password = self.password.text()  
        conn = self.db
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? ",(username,))
        data = cur.fetchone()
        if data is None:
            QMessageBox.information(None, ("Login Failed"), 
            ("Please check your username  try again"),
             QMessageBox.Ok)   
        else:
            passorddb = data[6]
            if(check_password_hash(passorddb,password)):
                date = self.now.toString(Qt.ISODate)
                time = QTime.currentTime()
                currenttime = time.toString('hh:mm:ss')
                datetime = date+" "+currenttime       
                datetime2 = date   
                result = cur.execute("INSERT into loginhistory(uid,login,logout) VALUES(?,?,?)",(data[0],datetime,datetime2))
                conn.commit()
                self.hide()
                self.mainW = MainWin(data[0],result.lastrowid,data[5])
                self.mainW.show()
            else:
                QMessageBox.information(None, ("Login Failed"), 
            ("Please check your password and try again"),
             QMessageBox.Ok)              

    def resetBut(self):
        self.username.setText("")   
        self.password.setText("")     

    def exitB(self):
        self.close()    



if __name__=="__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
