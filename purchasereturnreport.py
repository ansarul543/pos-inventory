import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 


class PurchaseReturnHistory(QDialog):
    def __init__(self,id='',type='',parent=None):
        super().__init__()
        uic.loadUi('./ui/purchasereturnreport.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Purchase Return Item Report")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)
        self.searchv.textChanged.connect(self.search)
        self.submitb.clicked.connect(self.viewDate)
        self.allb.clicked.connect(self.loadData)
        self.print.clicked.connect(self.printB)
        self.printpreview.clicked.connect(self.printA)
        self.loadDataEmpty()

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
        sv = self.searchv.text()   
        time = QTime.currentTime()
        currenttime = '23:58:00'

        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date

        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime     
        if sv=="":
            result = self.cur.execute("SELECT preturn.id,strftime('%d/%m/%Y',preturn.date),supplier.name as sname,products.name as pname,preturn.price,preturn.qtn,products.unit,preturn.discount,preturn.paid FROM preturn INNER JOIN supplier ON preturn.sid=supplier.id INNER JOIN products ON preturn.pid=products.id  WHERE preturn.date BETWEEN ? AND ?",(fromd,tod,))
            data = result.fetchall()
            total =0
            for index,i in enumerate(data):
                price = float(i[4])
                qtn = float(i[5])
                total += price*qtn-float(i[7])
            s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()            
            with open("html/purchasereturnreport.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,data=data,total=total,name=""))
        else:
            result = self.cur.execute("SELECT preturn.id,strftime('%d/%m/%Y',preturn.date),supplier.name as sname,products.name as pname,preturn.price,preturn.qtn,products.unit,preturn.discount,preturn.paid FROM preturn INNER JOIN supplier ON preturn.sid=supplier.id INNER JOIN products ON preturn.pid=products.id  WHERE products.name LIKE ? OR products.id LIKE ? OR supplier.name LIKE ? OR supplier.id LIKE ? OR supplier.partycode LIKE ? OR products.itemcode LIKE ? and preturn.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",fromd,tod,))
            data = result.fetchall()
            total =0
            for index,i in enumerate(data):
                price = float(i[4])
                qtn = float(i[5])
                total += price*qtn-float(i[7])
            s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()            
            with open("html/purchasereturnreport.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,data=data,total=total,name=""))

    def loadData(self):
        result = self.cur.execute("SELECT preturn.id,strftime('%d/%m/%Y',preturn.date),supplier.name as sname,products.name as pname,preturn.price,preturn.qtn,products.unit,preturn.discount,preturn.paid FROM preturn INNER JOIN supplier ON preturn.sid=supplier.id INNER JOIN products ON preturn.pid=products.id  ORDER BY preturn.id DESC")
        data = result.fetchall()
        total =0
        for index,i in enumerate(data):
            price = float(i[4])
            qtn = float(i[5])
            total += price*qtn-float(i[7])
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()            
        with open("html/purchasereturnreport.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=data,total=total,name="All Purchase Return Record"))

    def loadDataEmpty(self):
        data=[]
        total =0
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()            
        with open("html/purchasereturnreport.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=data,total=total,name=""))
  
    def search(self):
        sv = self.searchv.text()    
        result = self.cur.execute("SELECT preturn.id,strftime('%d/%m/%Y',preturn.date),supplier.name as sname,products.name as pname,preturn.price,preturn.qtn,products.unit,preturn.discount,preturn.paid FROM preturn INNER JOIN supplier ON preturn.sid=supplier.id INNER JOIN products ON preturn.pid=products.id  WHERE products.name LIKE ? OR products.id LIKE ? OR supplier.name LIKE ? OR supplier.id LIKE ? OR supplier.partycode LIKE ? OR products.itemcode LIKE ? ORDER BY preturn.id DESC",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        data = result.fetchall()
        total =0
        for index,i in enumerate(data):
            price = float(i[4])
            qtn = float(i[5])
            total += price*qtn-float(i[7])
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()            
        with open("html/purchasereturnreport.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=data,total=total,name="All Purchase Return Search Record "+sv))



