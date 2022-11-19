import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 

from msgdue import DueMessage
from customerbalance import CustomerBalance
balcus = CustomerBalance()

class CustomerDetails(QDialog):
    def __init__(self,id=''):
        super().__init__()
        uic.loadUi('./ui/customerdetails.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Customer Details")
        self.conn = sqlite3.connect('./database/data.db')
        self.id=id
        #self.c = self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.detailsLoad()
        self.loadData2()
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)
        self.fromd_2.setDate(date)
        self.tod_2.setDate(date)        
        self.viewb.clicked.connect(self.dateLoad)
        self.viewb_2.clicked.connect(self.viewDate2)
        self.alld.clicked.connect(self.allBc)
        self.printb.clicked.connect(self.printA)
        self.print2.clicked.connect(self.printB)
        self.msgb.clicked.connect(self.messageB)
        self.alld_2.clicked.connect(self.loadData2)

        self.printb_2.clicked.connect(self.printA2)
        self.print2_2.clicked.connect(self.printB2)

    def printA2(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_preview2)
        previewDialog.exec_()    
    def print_preview2(self, printer):
        self.textEdit_2.print_(printer)   

    def printB2(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit_2.print_(printer) 

    def viewDate2(self):
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()     
        time = QTime.currentTime()
        currenttime = '23:58:00'
        date_current = self.fromd_2.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date
        date_current = self.tod_2.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime    
        query = """
               SELECT strftime('%d/%m/%Y',pledger.date),pledger.type,products.name,customer.name,
               pledger.price,pledger.qtn,products.unit,pledger.dicount FROM pledger 
               LEFT JOIN customer ON pledger.cid=customer.id 
               LEFT JOIN supplier ON pledger.sid=supplier.id
               INNER JOIN products ON pledger.pid=products.id
               WHERE pledger.cid=? and pledger.date BETWEEN ? AND ? 
               """
        result = self.cur.execute(query,(self.id,fromd,tod,))
        data = result.fetchall()
        cu = self.cur.execute("SELECT id,name,address,phone FROM customer WHERE id=? ",(self.id,))
        customer = cu.fetchone()
        with open("html/customeritemhistory.html") as file:
            self.textEdit_2.setText(Template(file.read()).render(fromd=fromd,customer=customer,tod=date,setting=setting,data=data,name=""))

    def loadData2(self):        
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        query = """
               SELECT strftime('%d/%m/%Y',pledger.date),pledger.type,products.name,customer.name,
               pledger.price,pledger.qtn,products.unit,pledger.dicount FROM pledger 
               LEFT JOIN customer ON pledger.cid=customer.id 
               LEFT JOIN supplier ON pledger.sid=supplier.id
               INNER JOIN products ON pledger.pid=products.id
               WHERE pledger.cid=?
               """
        result = self.cur.execute(query,(self.id,))
        data = result.fetchall()
        cu = self.cur.execute("SELECT id,name,address,phone FROM customer WHERE id=? ",(self.id,))
        customer = cu.fetchone()
        with open("html/customeritemhistory.html") as file:
            self.textEdit_2.setText(Template(file.read()).render(fromd="",tod="",customer=customer,setting=setting,data=data,name=""))
    
    def messageB(self):
        self.das = DueMessage(self.id)
        self.das.show() 

    def printA(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec_()    
    def print_preview(self, printer):
        self.textEdit.print_(printer)   

    def printB(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)  

    def allBc(self):
        self.detailsLoad()

    def detailsLoad(self):
        id= self.id    
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data "),
             QMessageBox.Cancel) 
        else:
            lqr = """
            SELECT sss.id,sss.type,strftime('%d/%m/%Y',sss.date),sinvoice.invoice,
            sinvoice.total,sinvoice.paid,
            cash.amount,sreturn.paid,sreturn.price,sreturn.qtn,sreturn.discount
            FROM sss 
            LEFT JOIN sinvoice ON sss.invoice_id=sinvoice.id 
            LEFT JOIN cash ON sss.cash_id=cash.id 
            LEFT JOIN sreturn ON sss.return_id=sreturn.id 
            WHERE sss.cid=?
            """
            led = self.cur.execute(lqr,(id,))
            ledger = led.fetchall()

            s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()

            cu = self.cur.execute("SELECT id,name,address,phone FROM customer WHERE id=? ",(id,))
            customer = cu.fetchone()
            
            with open("html/customerledger.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd='',tod='',ledger=ledger,customer=customer,setting=setting))


    def dateLoad(self):
        id= self.id    
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')

        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date
        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime                  
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data "),
             QMessageBox.Cancel) 
        else:
            lqr = """
            SELECT sss.id,sss.type,strftime('%d/%m/%Y',sss.date),sinvoice.invoice,
            sinvoice.total,sinvoice.paid,
            cash.amount,sreturn.paid,sreturn.price,sreturn.qtn,sreturn.discount
            FROM sss 
            LEFT JOIN sinvoice ON sss.invoice_id=sinvoice.id 
            LEFT JOIN cash ON sss.cash_id=cash.id 
            LEFT JOIN sreturn ON sss.return_id=sreturn.id 
            WHERE sss.cid=? and sss.date BETWEEN ? AND ?
            """
            led = self.cur.execute(lqr,(id,fromd,tod,))
            ledger = led.fetchall()

            s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()

            cu = self.cur.execute("SELECT id,name,address,phone FROM customer WHERE id=? ",(id,))
            customer = cu.fetchone()
            
            with open("html/customerledger.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,ledger=ledger,customer=customer,setting=setting))
             


       
