import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
import sqlite3
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 

class PurchaseInvoice(QDialog):
    def __init__(self,id='',type='',parent=None):
        super().__init__()
        uic.loadUi('./ui/pinvoice.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Purchase Invoice")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)
        #self.toDate()
        self.tableWidget.setHorizontalHeaderLabels(["Invoice No.","Date","Supplier Name","Paid","Total Amount","Due","Prepared By"])
        self.tableWidget.setColumnWidth(4,180)
        self.tableWidget.setColumnWidth(5,180)
        self.searchv.textChanged.connect(self.search)
        self.submitb.clicked.connect(self.viewDate)
        self.deleteb.clicked.connect(self.deleteData)
        self.textEdit.hide()
        self.printb.clicked.connect(self.printData)   
        self.print2.clicked.connect(self.printB)  
        self.tableWidget.doubleClicked.connect(self.printData)   
        self.refreshb.clicked.connect(self.refreshD)
        self.allb.clicked.connect(self.allDa)

    def allDa(self):
        self.loadData()

    def refreshD(self):
        self.toDate()

    def loadData(self):
        result = self.cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total,users.name FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id LEFT JOIN users ON pinvoice.uid=users.id  ORDER BY pinvoice.id DESC")
        data = result.fetchall()
        self.tableWidget.setRowCount(len(data))
        totalp = 0
        duep = 0
        paidp=0
        for index,i in enumerate(data):
            total = i[7]
            paid = i[6]
            due = float(total) - float(paid)
            duep+=due
            totalp+=float(total)
            paidp+=float(paid)
            self.tableWidget.setItem(index,0,QTableWidgetItem(i[0]))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(i[6]))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[7]))
            self.tableWidget.setItem(index,5,QTableWidgetItem(str(due)))
            self.tableWidget.setItem(index,6,QTableWidgetItem(i[8]))
        self.total.setText(str(totalp))


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
            result = self.cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total,users.name FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id LEFT JOIN users ON pinvoice.uid=users.id WHERE pinvoice.date BETWEEN ? AND ?",(fromd,tod,))
            data = result.fetchall()
            self.tableWidget.setRowCount(len(data))
            totalp = 0
            duep = 0
            paidp=0
            for index,i in enumerate(data):
                total = i[7]
                paid = i[6]
                due = float(total) - float(paid)
                duep+=due
                totalp+=float(total)
                paidp+=float(paid)
                self.tableWidget.setItem(index,0,QTableWidgetItem(i[0]))
                self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
                self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
                self.tableWidget.setItem(index,3,QTableWidgetItem(i[6]))
                self.tableWidget.setItem(index,4,QTableWidgetItem(i[7]))
                self.tableWidget.setItem(index,5,QTableWidgetItem(str(due)))
                self.tableWidget.setItem(index,6,QTableWidgetItem(i[8]))
            self.total.setText(str(totalp))
        else:
            result = self.cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total,users.name FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id LEFT JOIN users ON pinvoice.uid=users.id WHERE pinvoice.invoice LIKE ? OR supplier.name LIKE ? OR supplier.partycode LIKE ? OR supplier.id LIKE ? and pinvoice.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",fromd,tod,))
            data = result.fetchall()
            self.tableWidget.setRowCount(len(data))
            totalp = 0
            duep = 0
            paidp=0
            for index,i in enumerate(data):
                total = i[7]
                paid = i[6]
                due = float(total) - float(paid)
                duep+=due
                totalp+=float(total)
                paidp+=float(paid)
                self.tableWidget.setItem(index,0,QTableWidgetItem(i[0]))
                self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
                self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
                self.tableWidget.setItem(index,3,QTableWidgetItem(i[6]))
                self.tableWidget.setItem(index,4,QTableWidgetItem(i[7]))
                self.tableWidget.setItem(index,5,QTableWidgetItem(str(due)))
                self.tableWidget.setItem(index,6,QTableWidgetItem(i[8]))
            self.total.setText(str(totalp))            

    def search(self):
        sv = self.searchv.text()    
        result = self.cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total,users.name FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id LEFT JOIN users ON pinvoice.uid=users.id WHERE pinvoice.invoice LIKE ? OR supplier.name LIKE ? OR supplier.id LIKE ?  OR supplier.partycode LIKE ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",))
        data = result.fetchall()
        self.tableWidget.setRowCount(len(data))
        totalp = 0
        duep = 0
        paidp=0
        for index,i in enumerate(data):
            total = i[7]
            paid = i[6]
            due = float(total) - float(paid)
            duep+=due
            totalp+=float(total)
            paidp+=float(paid)
            self.tableWidget.setItem(index,0,QTableWidgetItem(i[0]))
            self.tableWidget.setItem(index,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(index,3,QTableWidgetItem(i[6]))
            self.tableWidget.setItem(index,4,QTableWidgetItem(i[7]))
            self.tableWidget.setItem(index,5,QTableWidgetItem(str(due)))
            self.tableWidget.setItem(index,6,QTableWidgetItem(i[8]))
        self.total.setText(str(totalp))

    
    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()

        reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected row"),QMessageBox.Yes,QMessageBox.No) 
        if(reply == QMessageBox.Yes and id!=None):
            sda = self.cur.execute("SELECT total,paid,sid,id FROM pinvoice WHERE invoice=?",(id,))
            sdata = sda.fetchone()
            total = float(sdata[0])
            paid = float(sdata[1])
            invoice_i = sdata[3]
            sid = sdata[2]
            due = total-paid
            result = self.cur.execute("DELETE FROM pinvoice WHERE invoice=?",(id,))
            self.conn.commit()
            datas = self.cur.execute("SELECT * FROM purchase WHERE invoice=?",(id,))
            datas = datas.fetchall()
            if(result):             
                for i in datas:
                    pid = i[2]
                    result2 = self.cur.execute("SELECT * FROM products WHERE id=?",(pid,)) 
                    data = result2.fetchone()
                    qtns = data[8]
                    qtn2 = float(qtns)-float(i[4])
                    self.cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn2,pid,))
                    self.conn.commit()
                    self.cur.execute("DELETE FROM pledger WHERE purcchase_id=?",(i[0],))
                    self.conn.commit() 
                self.cur.execute("DELETE FROM purchase WHERE invoice=?",(id,)) 
                self.conn.commit()           
                self.cur.execute("DELETE FROM ppp WHERE invoice_id=?",(invoice_i,))
                self.conn.commit()    
                self.loadData()   
                QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
            else:
                QMessageBox.information(None, ("Failed"), ("Data not deleted successfully"),QMessageBox.Ok)     
    
    def printB(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if id is None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row to do print"),QMessageBox.Ok)
        else:
            s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()
            invoice = self.cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,supplier.address,supplier.phone,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total,supplier.id as sid,pinvoice.previus_due,pinvoice.area,pinvoice.paribahan,pinvoice.status FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id WHERE pinvoice.invoice=?",(id,))   
            invoice = invoice.fetchone()
            result = self.cur.execute("SELECT purchase.invoice,strftime('%d/%m/%Y',purchase.date),supplier.name as sname,products.name as pname,purchase.buy_rate,purchase.qtn,products.unit,purchase.discount,purchase.discountpercent FROM purchase INNER JOIN supplier ON purchase.sid=supplier.id INNER JOIN products ON purchase.pid=products.id  WHERE purchase.invoice=?",(id,))
            data = result.fetchall() 
            value = 0
            for index, i in enumerate(data):
                total = float(i[5])*float(i[4])
                totalv = total-float(i[7])
                value+=float(totalv)
            with open("html/purchaseinvoice.html") as file:
                self.textEdit.setText(Template(file.read()).render( invoice=invoice,data=data,setting=setting,total=value))        
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.textEdit.print_(printer)                

    def printData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if id is None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row to do print"),QMessageBox.Ok)
        else:
            s = self.cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()
            invoice = self.cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,supplier.address,supplier.phone,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total,supplier.id as sid,pinvoice.previus_due,pinvoice.area,pinvoice.paribahan,pinvoice.status FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id WHERE pinvoice.invoice=?",(id,))   
            invoice = invoice.fetchone()
            result = self.cur.execute("SELECT purchase.invoice,strftime('%d/%m/%Y',purchase.date),supplier.name as sname,products.name as pname,purchase.buy_rate,purchase.qtn,products.unit,purchase.discount,purchase.discountpercent FROM purchase INNER JOIN supplier ON purchase.sid=supplier.id INNER JOIN products ON purchase.pid=products.id  WHERE purchase.invoice=?",(id,))
            data = result.fetchall() 
            value = 0
            for index, i in enumerate(data):
                total = float(i[5])*float(i[4])
                totalv = total-float(i[7])
                value+=float(totalv)
            with open("html/purchaseinvoice.html") as file:
                self.textEdit.setText(Template(file.read()).render( invoice=invoice,data=data,setting=setting,total=value))

            printer = QPrinter(QPrinter.HighResolution)
            previewDialog = QPrintPreviewDialog(printer, self)
            previewDialog.paintRequested.connect(self.print_preview)
            previewDialog.exec_()    

    def print_preview(self, printer):
        self.textEdit.print_(printer) 


