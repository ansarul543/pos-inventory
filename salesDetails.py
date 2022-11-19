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

class SalesDetails(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/salesDetails.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Sales Ledger")
        self.conn = sqlite3.connect('./database/data.db')
        self.c = self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        #self.detailsLoad()
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)
        self.viewb.clicked.connect(self.dateLoad)
        self.alld.clicked.connect(self.allBc)
        self.printb.clicked.connect(self.printA)
        self.print2.clicked.connect(self.printB)
        self.sv.textChanged.connect(self.searchV)

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

    def searchV(self):
        sv = self.sv.text()
        if sv!="":
            s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()
            sql="""SELECT sinvoice.id,sinvoice.invoice,sinvoice.paytype,sinvoice.paid,
            sinvoice.total,strftime('%d/%m/%Y',sinvoice.date) as date, customer.name FROM sinvoice 
            INNER JOIN customer ON sinvoice.cid=customer.id WHERE sinvoice.invoice LIKE ? OR customer.name LIKE ?"""
            da = self.cur.execute(sql,("%"+sv+"%","%"+sv+"%",))
            result = da.fetchall()
            sql="""SELECT cash.id,cash.paytype,cash.amount,cash.des,strftime('%d/%m/%Y',cash.date) as date,customer.name
             FROM cash INNER JOIN customer ON cash.cid=customer.id WHERE cash.type='Customer' and customer.name LIKE ?"""
            cash = self.cur.execute(sql,("%"+sv+"%",))
            cashs = cash.fetchall()
            sql="""SELECT sreturn.id,sreturn.price,sreturn.qtn,sreturn.discount,strftime('%d/%m/%Y',sreturn.date) as date,paid ,customer.name
            FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id WHERE customer.name LIKE ?"""
            retur = self.cur.execute(sql,("%"+sv+"%",))
            repro = retur.fetchall()
            total =0
            paid = 0
            debit = 0
            returnamount = 0     
            fromd = ""       
            tod = ""
            for index, i in enumerate(result):
                total+=float(i[4])
                paids = float(i[3])
                paid +=paids            
            for index, i in enumerate(cashs):
                paid +=float(i[2])        
            for index, i in enumerate(repro):
                returnamount +=float(i[5])
                debit += float(i[1])*float(i[2])-float(i[3])
            with open("html/salesDetails.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=tod,setting=setting,invoice=result,cash=cashs,repro=repro,total=total,paid=paid,returnamount=returnamount,debit=debit))

    def detailsLoad(self):
            s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()

            sql="""SELECT sinvoice.id,sinvoice.invoice,sinvoice.paytype,sinvoice.paid,
            sinvoice.total,strftime('%d/%m/%Y',sinvoice.date) as date, customer.name FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id"""
            da = self.cur.execute(sql)
            result = da.fetchall()

            sql="""SELECT cash.id,cash.paytype,cash.amount,cash.des,strftime('%d/%m/%Y',cash.date) as date,customer.name
             FROM cash INNER JOIN customer ON cash.cid=customer.id WHERE cash.type='Customer'"""
            cash = self.cur.execute(sql)
            cashs = cash.fetchall()
            
            sql="""SELECT sreturn.id,sreturn.price,sreturn.qtn,sreturn.discount,strftime('%d/%m/%Y',sreturn.date) as date,paid ,customer.name
            FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id"""
            retur = self.cur.execute(sql)
            repro = retur.fetchall()
            total =0
            paid = 0
            debit = 0
            returnamount = 0     
            fromd = ""       
            tod = ""
            for index, i in enumerate(result):
                total+=float(i[4])
                paids = float(i[3])
                paid +=paids            
            for index, i in enumerate(cashs):
                paid +=float(i[2])        
            for index, i in enumerate(repro):
                returnamount +=float(i[5])
                debit += float(i[1])*float(i[2])-float(i[3])

            with open("html/salesDetails.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=tod,setting=setting,invoice=result,cash=cashs,repro=repro,total=total,paid=paid,returnamount=returnamount,debit=debit))

    def dateLoad(self):
        sv = self.sv.text()
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')
        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date
        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime                  
        
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        if sv=="":
            sql="""SELECT sinvoice.id,sinvoice.invoice,sinvoice.paytype,sinvoice.paid,
            sinvoice.total,strftime('%d/%m/%Y',sinvoice.date) as date, customer.name FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id
             WHERE sinvoice.date BETWEEN ? AND ? """
            da = self.cur.execute(sql,(fromd,tod,))
            result = da.fetchall()
            sql="""SELECT cash.type,cash.paytype,cash.amount,cash.des,strftime('%d/%m/%Y',cash.date) as date,customer.name
             FROM cash INNER JOIN customer ON cash.cid=customer.id WHERE cash.type='Customer' and cash.date BETWEEN ? AND ? """
            cas = self.cur.execute(sql,(fromd,tod,))
            cash = cas.fetchall()
            sql="""SELECT sreturn.id,sreturn.price,sreturn.qtn,sreturn.discount,strftime('%d/%m/%Y',sreturn.date) as date,paid ,customer.name
            FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id WHERE sreturn.date BETWEEN ? AND ? """
            retur = self.cur.execute(sql,(fromd,tod,))
            repro = retur.fetchall()
            total =0
            paid = 0
            debit = 0
            returnamount = 0            
            for index, i in enumerate(result):
                total+=float(i[4])
                paids = float(i[3])
                paid +=paids            
            for index, i in enumerate(cash):
                paid +=float(i[2])        
            for index, i in enumerate(repro):
                returnamount +=float(i[5])
                debit += float(i[1])*float(i[2])-float(i[3])
            with open("html/salesDetails.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,invoice=result,cash=cash,repro=repro,total=total,paid=paid,returnamount=returnamount,debit=debit))
        else:
            sql="""SELECT sinvoice.id,sinvoice.invoice,sinvoice.paytype,sinvoice.paid,
            sinvoice.total,strftime('%d/%m/%Y',sinvoice.date) as date, customer.name FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id
             WHERE sinvoice.invoice LIKE ? OR customer.name LIKE ? and sinvoice.date BETWEEN ? AND ? """
            da = self.cur.execute(sql,("%"+sv+"%","%"+sv+"%",fromd,tod,))
            result = da.fetchall()
            sql="""SELECT cash.type,cash.paytype,cash.amount,cash.des,strftime('%d/%m/%Y',cash.date) as date,customer.name
             FROM cash INNER JOIN customer ON cash.cid=customer.id WHERE cash.type='Customer' AND customer.name LIKE ? and cash.date BETWEEN ? AND ? """
            cas = self.cur.execute(sql,("%"+sv+"%",fromd,tod,))
            cash = cas.fetchall()
            sql="""SELECT sreturn.id,sreturn.price,sreturn.qtn,sreturn.discount,strftime('%d/%m/%Y',sreturn.date) as date,paid ,customer.name
            FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id WHERE customer.name LIKE ? and sreturn.date BETWEEN ? AND ? """
            retur = self.cur.execute(sql,("%"+sv+"%",fromd,tod,))
            repro = retur.fetchall()
            total =0
            paid = 0
            debit = 0
            returnamount = 0            
            for index, i in enumerate(result):
                total+=float(i[4])
                paids = float(i[3])
                paid +=paids            
            for index, i in enumerate(cash):
                paid +=float(i[2])        
            for index, i in enumerate(repro):
                returnamount +=float(i[5])
                debit += float(i[1])*float(i[2])-float(i[3])
            with open("html/salesDetails.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,invoice=result,cash=cash,repro=repro,total=total,paid=paid,returnamount=returnamount,debit=debit))
                              


       

