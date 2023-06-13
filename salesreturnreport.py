import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 

class SalesReturnHistory(QDialog):
    def __init__(self,id='',type='',parent=None):
        super().__init__()
        uic.loadUi('./ui/salesreturnreport.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Sales Return Report")
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
        cur = self.conn.cursor()
        s = cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
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
            result = cur.execute("SELECT sreturn.id,strftime('%d/%m/%Y',sreturn.date),customer.name as cname,products.name as pname,sreturn.price,sreturn.qtn,products.unit,sreturn.discount,sreturn.paid,products.buyrate  FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id INNER JOIN products ON sreturn.pid=products.id  WHERE sreturn.date BETWEEN ? AND ?",(fromd,tod,))
            data = result.fetchall()
            totalv =0
            buyv =0
            for index,i in enumerate(data):
                price = float(i[4])
                qtn = float(i[5])
                total = price*qtn
                dis = float(i[7])
                total = total-dis
                totalv +=total
                buy = float(i[9])
                t = buy*qtn
                buyv+=t
            profit = totalv-buyv     
            with open("html/salesreturnreport.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,data=data,profit=profit,buy=buyv,totals=totalv,name=""))
        else:
            result = cur.execute("SELECT sreturn.id,strftime('%d/%m/%Y',sreturn.date),customer.name as cname,products.name as pname,sreturn.price,sreturn.qtn,products.unit,sreturn.discount,sreturn.paid,products.buyrate  FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id INNER JOIN products ON sreturn.pid=products.id  WHERE products.name LIKE ? OR products.id LIKE ? OR customer.name LIKE ? OR customer.id LIKE ? OR customer.partycode LIKE ? OR products.itemcode LIKE ? and sreturn.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",fromd,tod,))
            data = result.fetchall()
            totalv =0
            buyv =0
            for index,i in enumerate(data):
                price = float(i[4])
                qtn = float(i[5])
                total = price*qtn
                dis = float(i[7])
                total = total-dis
                totalv +=total
                buy = float(i[9])
                t = buy*qtn
                buyv+=t
            profit = totalv-buyv     
            with open("html/salesreturnreport.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd=fromd,tod=date,setting=setting,data=data,profit=profit,buy=buyv,totals=totalv,name=""))
        cur.close()

    def loadDataEmpty(self):
            cur = self.conn.cursor()
            s = cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()
            data=[]
            totalv =0
            buyv =0
            profit = totalv-buyv     
            with open("html/salesreturnreport.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=data,profit=profit,buy=buyv,totals=totalv,name=" "))
            cur.close()

    def loadData(self):
            cur = self.conn.cursor()
            s = cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()
            result = cur.execute("SELECT sreturn.id,strftime('%d/%m/%Y',sreturn.date),customer.name as cname,products.name as pname,sreturn.price,sreturn.qtn,products.unit,sreturn.discount,sreturn.paid,products.buyrate  FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id INNER JOIN products ON sreturn.pid=products.id ")
            data = result.fetchall()
            totalv =0
            buyv =0
            for index,i in enumerate(data):
                price = float(i[4])
                qtn = float(i[5])
                total = price*qtn
                dis = float(i[7])
                total = total-dis
                totalv +=total
                buy = float(i[9])
                t = buy*qtn
                buyv+=t
            profit = totalv-buyv     
            with open("html/salesreturnreport.html") as file:
                self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=data,profit=profit,buy=buyv,totals=totalv,name="All Sales Return Record"))
            cur.close()

    def search(self):
        cur = self.conn.cursor()
        s = cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
        setting = s.fetchone()
        sv = self.searchv.text()    
        result = cur.execute("SELECT sreturn.id,strftime('%d/%m/%Y',sreturn.date),customer.name as cname,products.name as pname,sreturn.price,sreturn.qtn,products.unit,sreturn.discount,sreturn.paid,products.buyrate  FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id INNER JOIN products ON sreturn.pid=products.id WHERE products.name LIKE ? OR products.id LIKE ? OR customer.name LIKE ? OR customer.id LIKE ? OR customer.partycode LIKE ? OR products.itemcode LIKE ? ",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        data = result.fetchall()
        totalv =0
        buyv =0
        for index,i in enumerate(data):
            price = float(i[4])
            qtn = float(i[5])
            total = price*qtn
            dis = float(i[7])
            total = total-dis
            totalv +=total
            buy = float(i[9])
            t = buy*qtn
            buyv+=t
        profit = totalv-buyv     
        with open("html/salesreturnreport.html") as file:
            self.textEdit.setText(Template(file.read()).render(fromd='',tod='',setting=setting,data=data,profit=profit,buy=buyv,totals=totalv,name="All Sales Return Search Record "+sv))
        cur.close()


