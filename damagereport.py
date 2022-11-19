import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 

class DamageReport(QDialog):
    def __init__(self,id='',type='',parent=None):
        super().__init__()
        uic.loadUi('./ui/damagereport.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Damage Item Report")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)
        self.searchv.textChanged.connect(self.search)
        self.submitb.clicked.connect(self.viewDate)
        self.print.clicked.connect(self.printB)
        self.printpreview.clicked.connect(self.printA)
        self.allb.clicked.connect(self.loadData)
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
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        time = QTime.currentTime()
        currenttime = '23:58:00'
        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date
        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime    
        if sv=="":
            result = self.cur.execute("SELECT strftime('%d/%m/%Y',damage.date),products.name as pname,damage.qtn,products.unit,products.buyrate  FROM damage INNER JOIN products ON damage.pid=products.id  WHERE damage.date BETWEEN ? AND ? ORDER BY damage.id DESC",(fromd,tod,))
            data = result.fetchall()   
            with open("html/damageitem.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,data=data,name=""))
        else:
            result = self.cur.execute("SELECT strftime('%d/%m/%Y',damage.date),products.name as pname,damage.qtn,products.unit,products.buyrate  FROM damage  INNER JOIN products ON damage.pid=products.id  WHERE products.name LIKE ? OR products.id LIKE ? OR products.itemcode LIKE ? and damage.date BETWEEN ? AND ? ",("%"+sv+"%","%"+sv+"%","%"+sv+"%",fromd,tod,))
            data = result.fetchall()   
            with open("html/damageitem.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,data=data,name=""))

    def loadData(self):
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        result = self.cur.execute("SELECT strftime('%d/%m/%Y',damage.date),products.name as pname,damage.qtn,products.unit,products.buyrate FROM damage INNER JOIN products ON damage.pid=products.id  ORDER BY damage.id DESC")
        data = result.fetchall()   
        with open("html/damageitem.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=data,name="All damage Record"))

    def loadDataEmpty(self):
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        with open("html/damageitem.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=[],name=" "))


    def search(self):
        s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        sv = self.searchv.text()    
        result = self.cur.execute("SELECT strftime('%d/%m/%Y',damage.date),products.name as pname,damage.qtn,products.unit,products.buyrate  FROM damage  INNER JOIN products ON damage.pid=products.id WHERE products.name LIKE ? OR products.id LIKE ? OR products.itemcode LIKE ? ORDER BY damage.id DESC",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        data = result.fetchall()   
        with open("html/damageitem.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=data,name="All damage Search Record "+sv))


