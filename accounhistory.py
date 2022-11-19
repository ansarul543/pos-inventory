import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 

class OfficialAccount(QDialog):
    def __init__(self,id='',name=''):
        super().__init__()
        uic.loadUi('./ui/accounthistory.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle(name+" Expense Account")
        self.id = id
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.officialspay()
        date = QDate.currentDate()
        self.fromd_5.setDate(date)
        self.tod_5.setDate(date)
        self.viewdoffb.clicked.connect(self.officialspaydate)
        self.loadalloffb.clicked.connect(self.loadofficialall)
        self.printb.clicked.connect(self.printA)

    def printA(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec_()    
    def print_preview(self, printer):
        self.textEdit.print_(printer) 

    def loadofficialall(self):
        self.officialspay()

    def officialspaydate(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')

        date_current = self.fromd_5.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date

        date_current = self.tod_5.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime   

        result = self.cur.execute("SELECT strftime('%d/%m/%Y',cash.date),cash.paytype,cash.des,cash.amount,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' AND cash.accid=? AND cash.date BETWEEN ? AND ?",(self.id,fromd,tod,))
        result=result.fetchall()

        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()   

        acc = self.cur.execute("SELECT * FROM account WHERE id=? ",(self.id,))
        account = acc.fetchone()
            
        with open("html/officialledger.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=tod,ledger=result,account=account,setting=setting))        


    def officialspay(self):
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        result = self.cur.execute("SELECT strftime('%d/%m/%Y',cash.date),cash.paytype,cash.des,cash.amount,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' AND cash.accid=? ",(self.id,))
        result=result.fetchall()

        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()   
        
        acc = self.cur.execute("SELECT * From account WHERE id=? ",(self.id,))
        account = acc.fetchone()
            
        with open("html/officialledger.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',ledger=result,account=account,setting=setting))     
    
