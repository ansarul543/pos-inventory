import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 

class ProductLedger(QDialog):
    def __init__(self,id='',parent=None):
        super().__init__()
        uic.loadUi('./ui/productledger.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Product Ledger")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)
        self.pid = id
        self.submitb.clicked.connect(self.viewDate)
        self.print.clicked.connect(self.printB)
        self.printpreview.clicked.connect(self.printA)
        self.allb.clicked.connect(self.loadData)
        self.loadDataEmpty()
        self.loadData()
        


    def printB(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

    def printA(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec_()    
    def print_preview(self, printer):
        self.textEdit.print_(printer) 

    def viewDate(self):
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        p = self.cur.execute("SELECT name,itemcode,qtn,unit,buyrate,wholesale,salerate,tax FROM products WHERE id=? ",(self.pid,))
        pro = p.fetchone()        
        time = QTime.currentTime()
        currenttime = '23:58:00'
        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date
        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime    
        query = """
               SELECT strftime('%d/%m/%Y',pledger.date),pledger.type,supplier.name,customer.name,
               pledger.price,pledger.qtn,products.unit,pledger.dicount FROM pledger 
               LEFT JOIN customer ON pledger.cid=customer.id 
               LEFT JOIN supplier ON pledger.sid=supplier.id
               INNER JOIN products ON pledger.pid=products.id
               WHERE pledger.pid=? and pledger.date BETWEEN ? AND ? 
               """
        result = self.cur.execute(query,(self.pid,fromd,tod,))
        data = result.fetchall()

        with open("html/productledger.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,data=data,pro=pro,name=""))

    def loadData(self):        
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        query = """
               SELECT strftime('%d/%m/%Y',pledger.date),pledger.type,supplier.name,customer.name,
               pledger.price,pledger.qtn,products.unit,pledger.dicount FROM pledger 
               LEFT JOIN customer ON pledger.cid=customer.id 
               LEFT JOIN supplier ON pledger.sid=supplier.id
               INNER JOIN products ON pledger.pid=products.id
               WHERE pledger.pid=?
               """
        result = self.cur.execute(query,(self.pid,))
        data = result.fetchall()
        p = self.cur.execute("SELECT name,itemcode,qtn,unit,buyrate,wholesale,salerate,tax FROM products WHERE id=? ",(self.pid,))
        pro = p.fetchone()

        with open("html/productledger.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',pro=pro,setting=setting,data=data,name=" "))

    def loadDataEmpty(self):
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        p = self.cur.execute("SELECT name,itemcode,qtn,unit,buyrate,wholesale,salerate,tax FROM products WHERE id=? ",(self.pid,))
        pro = p.fetchone()        
        data=[]
        totalv =0
        buyv =0
        profit = totalv-buyv     
        with open("html/productledger.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',pro=pro,setting=setting,data=data,name=" "))





