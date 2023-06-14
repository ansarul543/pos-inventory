import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap,QDoubleValidator
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template 
from msginvoice import InvoiceMessage
import sqlite3
import datetime

class SalesInvoice(QDialog):
    def __init__(self,id='',type='',parent=None):
        super().__init__()
        uic.loadUi('./ui/sinvoice.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Sales Invoice")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)
        #self.toDate()
        self.tableWidget.setHorizontalHeaderLabels(["Invoice No.","Date","Customer Name","Paid","Total Amount","Due","Payment Type","Prepared By"])
        self.searchv.textChanged.connect(self.search)
        self.submitb.clicked.connect(self.viewDate)
        self.deleteb.clicked.connect(self.deleteData)
        self.textEdit.hide()
        self.printb.clicked.connect(self.printData)
        self.print2.clicked.connect(self.printB)
        self.tableWidget.doubleClicked.connect(self.printData)
        self.refreshb.clicked.connect(self.refreshD)
        self.allb.clicked.connect(self.allDa)
        self.msgb.clicked.connect(self.messageB)
        self.textEdit.setMaximumWidth(200)

    def messageB(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if id is None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row to sent message"),QMessageBox.Ok)
        else:
            self.msgin=InvoiceMessage(id)
            self.msgin.show()

    def allDa(self):
        self.loadData()
    def refreshD(self):
        self.toDate()

    def loadData(self):     
        cur = self.conn.cursor() 
        result = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype,users.name FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id LEFT JOIN users ON sinvoice.uid=users.id ORDER BY sinvoice.id DESC")
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
            self.tableWidget.setItem(index,7,QTableWidgetItem(i[9]))
        self.total.setText(str(totalp))
        cur.close() 
               

    def toDate(self):
        currenttime = '23:58:00'
        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date
        tod = date+" "+currenttime    
        cur = self.conn.cursor()       
        result = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype,users.name FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id LEFT JOIN users ON sinvoice.uid=users.id WHERE sinvoice.date BETWEEN ? AND ?",(fromd,tod,))
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
            self.tableWidget.setItem(index,7,QTableWidgetItem(i[9]))
        self.total.setText(str(totalp))
        cur.close()


    def viewDate(self):
        sv = self.searchv.text()   
        time = QTime.currentTime()
        currenttime = currenttime = '23:58:00'

        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date

        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime    
        cur = self.conn.cursor()  
        if sv=="":
            result = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype,users.name FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id LEFT JOIN users ON sinvoice.uid=users.id WHERE sinvoice.date BETWEEN ? AND ?",(fromd,tod,))
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
                self.tableWidget.setItem(index,7,QTableWidgetItem(i[9]))
            self.total.setText(str(totalp))
        else:
            result = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype,users.name FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id LEFT JOIN users ON sinvoice.uid=users.id WHERE sinvoice.invoice LIKE ? OR customer.name LIKE ? OR customer.partycode LIKE ? OR customer.id LIKE ? and sinvoice.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",fromd,tod,))
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
                self.tableWidget.setItem(index,7,QTableWidgetItem(i[9]))
            self.total.setText(str(totalp)) 
        cur.close()                   
        

    def search(self):
        sv = self.searchv.text() 
        cur = self.conn.cursor()   
        result = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype,users.name FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id LEFT JOIN users ON sinvoice.uid=users.id WHERE sinvoice.invoice LIKE ? OR customer.name LIKE ? OR customer.partycode LIKE ? OR customer.id LIKE ? ",("%"+sv+"%","%"+sv+"%","%"+sv+"%","%"+sv+"%",))
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
            self.tableWidget.setItem(index,7,QTableWidgetItem(i[9]))
        self.total.setText(str(totalp))
        cur.close()
          
    
    def deleteData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        cur = self.conn.cursor()
        reply = QMessageBox.question(None, ("Warning"), ("Do you want to delete selected invoice row"),QMessageBox.Yes,QMessageBox.No) 
        if(reply == QMessageBox.Yes and id!=None):
            sda = cur.execute("SELECT total,paid,cid,id FROM sinvoice WHERE invoice=?",(id,))
            sdata = sda.fetchone()
            total = float(sdata[0])
            paid = float(sdata[1])
            invoice_i = sdata[3]
            cid = sdata[2]
            due = total-paid
            result = cur.execute("DELETE FROM sinvoice WHERE invoice=?",(id,))
            self.conn.commit()
            datas = cur.execute("SELECT * FROM sales WHERE invoice=?",(id,))
            datas = datas.fetchall()
            if(result):
                for i in datas:
                    pid = i[2]
                    result2 = cur.execute("SELECT * FROM products WHERE id=?",(pid,)) 
                    data = result2.fetchone()
                    qtns = data[8]
                    qtn2 = float(qtns)+float(i[4])
                    cur.execute("UPDATE products SET qtn=? WHERE id=?",(qtn2,pid,))
                    self.conn.commit()
                    cur.execute("DELETE FROM pledger WHERE sales_id=?",(i[0],))
                    self.conn.commit()                     
                cur.execute("DELETE FROM sales WHERE invoice=?",(id,)) 
                self.conn.commit()  
                cur.execute("DELETE FROM sss WHERE invoice_id=?",(invoice_i,))
                self.conn.commit()                                   
                self.loadData()   
                QMessageBox.information(None, ("Successful"), ("Data deleted successfully"),QMessageBox.Ok) 
            else:
                QMessageBox.information(None, ("Failed"), ("Data not deleted successfully"),QMessageBox.Ok)     
        cur.close()        
                
    def printB(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        cur = self.conn.cursor()
        if id is None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row to do print"),QMessageBox.Ok)
        else:
            s = cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()
            invoice = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,customer.address,customer.phone,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype,customer.id as cid,sinvoice.previus_due,sinvoice.area,sinvoice.paribahan,sinvoice.status FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id WHERE sinvoice.invoice=?",(id,))   
            invoice = invoice.fetchone()
            result = cur.execute("SELECT sales.invoice,strftime('%d/%m/%Y',sales.date),customer.name as cname,products.name as pname,sales.price,sales.qtn,products.unit,sales.discount,sales.type,sales.vatpercent,sales.discountpercent FROM sales INNER JOIN customer ON sales.cid=customer.id INNER JOIN products ON sales.pid=products.id WHERE sales.invoice=?",(id,))
            data = result.fetchall() 
            value = 0
            for index, i in enumerate(data):
                total = float(i[5])*float(i[4])
                totalv = total-float(i[7])
                value+=float(totalv)
            with open("html/salesinvoice.html") as file:
                self.textEdit.setText(Template(file.read()).render( invoice=invoice,data=data,setting=setting,total=value))        
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.textEdit.print_(printer)
        cur.close()        

    def printData(self):
        NewInd = self.tableWidget.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        cur = self.conn.cursor()
        if id is None:
            QMessageBox.warning(None, ("Warning"), ("Please select any row to do print"),QMessageBox.Ok)
        else:
            s = cur.execute("SELECT * FROM settings WHERE id=? ",(1,))
            setting = s.fetchone()
            invoice = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,customer.address,customer.phone,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype,customer.id as cid,sinvoice.previus_due,sinvoice.area,sinvoice.paribahan,sinvoice.status FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id WHERE sinvoice.invoice=?",(id,))   
            invoice = invoice.fetchone()
            result = cur.execute("SELECT sales.invoice,strftime('%d/%m/%Y',sales.date),customer.name as cname,products.name as pname,sales.price,sales.qtn,products.unit,sales.discount,sales.type,sales.vatpercent,sales.discountpercent FROM sales INNER JOIN customer ON sales.cid=customer.id INNER JOIN products ON sales.pid=products.id WHERE sales.invoice=?",(id,))
            data = result.fetchall() 
            value = 0
            for index, i in enumerate(data):
                total = float(i[5])*float(i[4])
                totalv = total-float(i[7])
                value+=float(totalv)
            with open("html/salesinvoice.html") as file:
                self.textEdit.setText(Template(file.read()).render( invoice=invoice,data=data,setting=setting,total=value))

            printer = QPrinter(QPrinter.HighResolution)
            previewDialog = QPrintPreviewDialog(printer, self)
            previewDialog.paintRequested.connect(self.print_preview)
            previewDialog.exec_() 
        cur.close()    

    def print_preview(self, printer):
        self.textEdit.print_(printer)             

        