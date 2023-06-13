import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3


class ExpenseReport(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/expensehistory.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Expense Statement Report")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        self.setMaximumWidth(979)
        self.setMaximumHeight(787)        
        self.officialpay.setHorizontalHeaderLabels(["Date","Account Name","Payment Type","Description","Amount","Prepared By"])

        self.officialpay.setColumnWidth(5,100)

        date = QDate.currentDate()
        self.fromd_5.setDate(date)
        self.tod_5.setDate(date)

        self.viewdoffb.clicked.connect(self.officialspaydate)
        self.loadalloffb.clicked.connect(self.loadofficialall)
        self.svop.textChanged.connect(self.officialspaySearch)


    def loadofficialall(self):
        self.officialspay()

    def officialspaydate(self):
        sv = self.svop.text()

        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')

        date_current = self.fromd_5.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date

        date_current = self.tod_5.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime   
        cur = self.conn.cursor()  
        if sv=="":      
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),account.name,cash.paytype,cash.des,cash.amount,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' AND cash.date BETWEEN ? AND ?",(fromd,tod,))
            result=result.fetchall()
            self.officialpay.setRowCount(len(result))
            valuein = 0
            valueout = 0
            for index, i in enumerate(result):
                if i[3]=="Cash Receive" or i[3]=="Deposit":
                    total = float(i[5])
                    valuein+=float(total)
                if i[3]=="Cash Payment" or i[3]=="Withdrew":
                    total = float(i[5])
                    valueout+=float(total)                
                self.officialpay.setItem(index,0,QTableWidgetItem(i[1]))
                self.officialpay.setItem(index,1,QTableWidgetItem(i[2]))
                self.officialpay.setItem(index,2,QTableWidgetItem(i[3]))
                self.officialpay.setItem(index,3,QTableWidgetItem(i[4]))
                self.officialpay.setItem(index,4,QTableWidgetItem(i[5]))
                self.officialpay.setItem(index,5,QTableWidgetItem(i[6]))
            self.opayshowout.setText(str(valueout)) 
            self.opayshowin.setText(str(valuein))
        else:
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),account.name,cash.paytype,cash.des,cash.amount,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' and account.name LIKE ? AND cash.date BETWEEN ? AND ?",("%"+sv+"%",fromd,tod,))
            result=result.fetchall()
            self.officialpay.setRowCount(len(result))
            valuein = 0
            valueout = 0
            for index, i in enumerate(result):
                if i[3]=="Cash Receive" or i[3]=="Deposit":
                    total = float(i[5])
                    valuein+=float(total)
                if i[3]=="Cash Payment" or i[3]=="Withdrew":
                    total = float(i[5])
                    valueout+=float(total)                
                self.officialpay.setItem(index,0,QTableWidgetItem(i[1]))
                self.officialpay.setItem(index,1,QTableWidgetItem(i[2]))
                self.officialpay.setItem(index,2,QTableWidgetItem(i[3]))
                self.officialpay.setItem(index,3,QTableWidgetItem(i[4]))
                self.officialpay.setItem(index,4,QTableWidgetItem(i[5]))
                self.officialpay.setItem(index,5,QTableWidgetItem(i[6]))
            self.opayshowout.setText(str(valueout)) 
            self.opayshowin.setText(str(valuein))
        cur.close()    

    def officialspaySearch(self):
        sv = self.svop.text()
        cur = self.conn.cursor()
        if sv!="":
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),account.name,cash.paytype,cash.des,cash.amount,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' and account.name LIKE ?",("%"+sv+"%",))
            result=result.fetchall()
            self.officialpay.setRowCount(len(result))
            valuein = 0
            valueout = 0
            for index, i in enumerate(result):
                if i[3]=="Cash Receive" or i[3]=="Deposit":
                    total = float(i[5])
                    valuein+=float(total)
                if i[3]=="Cash Payment" or i[3]=="Withdrew":
                    total = float(i[5])
                    valueout+=float(total)                
                self.officialpay.setItem(index,0,QTableWidgetItem(i[1]))
                self.officialpay.setItem(index,1,QTableWidgetItem(i[2]))
                self.officialpay.setItem(index,2,QTableWidgetItem(i[3]))
                self.officialpay.setItem(index,3,QTableWidgetItem(i[4]))
                self.officialpay.setItem(index,4,QTableWidgetItem(i[5]))
                self.officialpay.setItem(index,5,QTableWidgetItem(i[6]))
            self.opayshowout.setText(str(valueout)) 
            self.opayshowin.setText(str(valuein))
        cur.close()    

    def officialspay(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),account.name,cash.paytype,cash.des,cash.amount,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' ORDER BY cash.id DESC")
        result=result.fetchall()
        self.officialpay.setRowCount(len(result))
        valuein = 0
        valueout = 0
        for index, i in enumerate(result):
            if i[3]=="Cash Receive" or i[3]=="Deposit":
                total = float(i[5])
                valuein+=float(total)
            if i[3]=="Cash Payment" or i[3]=="Withdrew":
                total = float(i[5])
                valueout+=float(total)                
            self.officialpay.setItem(index,0,QTableWidgetItem(i[1]))
            self.officialpay.setItem(index,1,QTableWidgetItem(i[2]))
            self.officialpay.setItem(index,2,QTableWidgetItem(i[3]))
            self.officialpay.setItem(index,3,QTableWidgetItem(i[4]))
            self.officialpay.setItem(index,4,QTableWidgetItem(i[5]))
            self.officialpay.setItem(index,5,QTableWidgetItem(i[6]))
        self.opayshowout.setText(str(valueout)) 
        self.opayshowin.setText(str(valuein))
        cur.close()

     




