import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QWidget
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,QTime,Qt,QDate
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3
from supplierdetails import SupplierDetails
from customerdetails import CustomerDetails
from supplierbalance import SupplierBalance
balsup = SupplierBalance()
from customerbalance import CustomerBalance
balcus = CustomerBalance()

class AllReport(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/report.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("All Report")
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
        #self.setFixedSize(937, 555)
        #self.setFixedSize(950, 600)   
        self.supplierdue.setHorizontalHeaderLabels(["Supplier ID","Supplier Name","Contact No","Due Amount"])
        self.customerdue.setHorizontalHeaderLabels(["Customer ID","Customer Name","Contact No","Due Amount"])
        self.supplierpayment.setHorizontalHeaderLabels(["Date","Supplier Name","Payment Type","Description","Amount","Bank Name","CHQ NUMBER","Trx ID","Prepared By"])
        self.customerpay.setHorizontalHeaderLabels(["Date","Customer Name","Payment Type","Description","Amount","Bank Name","CHQ NUMBER","Trx ID","Prepared By"])
        self.officialpay.setHorizontalHeaderLabels(["Date","Account Name","Payment Type","Description","Amount","Bank Name","CHQ NUMBER","Trx ID","Prepared By"])
        self.supplierdue.setColumnWidth(0,200)
        self.supplierdue.setColumnWidth(1,234)
        self.supplierdue.setColumnWidth(2,230)
        self.supplierdue.setColumnWidth(3,234)

        self.customerdue.setColumnWidth(0,200)
        self.customerdue.setColumnWidth(1,230)
        self.customerdue.setColumnWidth(2,234)
        self.customerdue.setColumnWidth(3,234)

        self.officialpay.setColumnWidth(5,100)
        self.customerpay.setColumnWidth(5,100)
        self.supplierpayment.setColumnWidth(5,100)

        self.suppliers.textChanged.connect(self.dueSearchSup)
        self.supplierb.clicked.connect(self.supAll)
        self.customers.textChanged.connect(self.customerDueSearch)
        self.allcusb.clicked.connect(self.cusAll)
        #self.supplierpay()
        #self.cuspay()
        #self.officialspay()
        self.viewdsup.clicked.connect(self.supplierpaydate)
        date = QDate.currentDate()
        self.fromd.setDate(date)
        self.tod.setDate(date)

        self.fromd_2.setDate(date)
        self.tod_2.setDate(date)
        self.fromd_5.setDate(date)
        self.tod_5.setDate(date)
        self.fromdover.setDate(date)
        self.todover.setDate(date)

        self.loadallsupb.clicked.connect(self.loadsup)
        self.viewdcus.clicked.connect(self.viewcustomerdate)
        self.loadallcusb.clicked.connect(self.loadallcustomer)
        self.viewdoffb.clicked.connect(self.officialspaydate)
        self.loadalloffb.clicked.connect(self.loadofficialall)
        self.loadoverall.clicked.connect(self.loadOverview)
        self.overviewb.clicked.connect(self.loadOverviewDate)
        #self.officialspaydate()
        #self.viewcustomerdate()
        #self.supplierpaydate()
        #self.loadOverviewDate()
        #self.loadOverviewData()
        self.svsp.textChanged.connect(self.supplierpaySearch)
        self.svcp.textChanged.connect(self.cuspaySearch)
        self.svop.textChanged.connect(self.officialspaySearch)
        self.supplierledger.clicked.connect(self.detailsSup)
        self.customerledger.clicked.connect(self.detailsCus)
        self.supplierdue.doubleClicked.connect(self.detailsSup)
        self.customerdue.doubleClicked.connect(self.detailsCus)

    def detailsSup(self):
        NewInd = self.supplierdue.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data "),
             QMessageBox.Ok) 
        else:
            self.datasup = SupplierDetails(id)
            self.datasup.show() 

    def detailsCus(self):
        NewInd = self.customerdue.currentIndex().siblingAtColumn(0)
        id = NewInd.data()
        if id==None:
            QMessageBox.warning(None, ("Required"), 
            ("Data not selected yet Please select data "),
             QMessageBox.Ok) 
        else:
            self.datacus = CustomerDetails(id)
            self.datacus.show() 

    def loadOverview(self):
        self.loadOverviewData()    

    def loadOverviewDate(self):
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')

        date_current = self.fromdover.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date

        date_current = self.todover.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime   
        cur = self.conn.cursor()
        result = cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id  WHERE pinvoice.date BETWEEN ? AND ?",(fromd,tod,))
        data = result.fetchall()
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
        self.totalap.setText(str(totalp))
        pr = cur.execute("SELECT preturn.id,strftime('%d/%m/%Y',preturn.date),supplier.name as sname,products.name as pname,preturn.price,preturn.qtn,products.unit,preturn.discount,preturn.paid FROM preturn INNER JOIN supplier ON preturn.sid=supplier.id INNER JOIN products ON preturn.pid=products.id  WHERE preturn.date BETWEEN ? AND ?",(fromd,tod,))
        prdata = pr.fetchall()
        prtotal =0
        prpaid =0
        for index,i in enumerate(prdata):
            price = float(i[4])
            qtn = float(i[5])
            prtotal += price*qtn-float(i[7])
            prpaid+=float(i[8])
        result = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id  WHERE sinvoice.date BETWEEN ? AND ?",(fromd,tod,))
        data2 = result.fetchall()
        totalps = 0
        dueps = 0
        paidps=0
        for index,i in enumerate(data2):
            total = i[7]
            paid = i[6]
            due = float(total) - float(paid)
            dueps+=due
            totalps+=float(total)
            paidps+=float(paid)            
        self.totalsp.setText(str(totalps))
        srd = cur.execute("SELECT sreturn.id,strftime('%d/%m/%Y',sreturn.date),customer.name as cname,products.name as pname,sreturn.price,sreturn.qtn,products.unit,sreturn.discount,sreturn.paid,products.buyrate  FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id INNER JOIN products ON sreturn.pid=products.id WHERE sreturn.date BETWEEN ? AND ?",(fromd,tod,))
        srdata = srd.fetchall()
        srtotalv =0
        srbuyv =0
        srpaid =0
        for index,i in enumerate(srdata):
            price = float(i[4])
            qtn = float(i[5])
            total = price*qtn
            dis = float(i[7])
            srtotalv += total-dis
            buy = float(i[9])
            srbuyv+=buy*qtn  
            srpaid+=float(i[8])      
        cur.execute("SELECT id,strftime('%d/%m/%Y',date),type,paytype,des,amount FROM cash WHERE date BETWEEN ? AND ? ",(fromd,tod,))
        data3 = self.cur.fetchall()
        amountin =0
        amountout=0
        customerpay=0
        supplierpay=0
        officialin=0
        officialout=0
        for index, i in enumerate(data3):
            if i[3]=="Cash Receive" or i[3]=="Deposit":
                amountin+=float(i[5])
                if i[2]=="Customer":
                    customerpay+=float(i[5])
                if i[2]=="Official":
                    officialin+=float(i[5])                    
            else:
                amountin+=0   
            if i[3]=="Cash Payment" or i[3]=="Withdrew":
                amountout+=float(i[5])  
                if i[2]=="Supplier":
                    supplierpay+=float(i[5])
                if i[2]=="Official":
                    officialout+=float(i[5])                                
            else:
                amountout+=0  
        self.totalcashin.setText(str(amountout))       
        self.totalcashout.setText(str(amountin)) 

        self.recieve.setText(str(customerpay))       
        self.payment.setText(str(supplierpay)) 

        self.offrecieve.setText(str(officialin))       
        self.offout.setText(str(officialout)) 

        for index, i in enumerate(data3):
            if i[3]=="Cash Receive" and i[2]=="Customer":
                total = float(i[5])
                dueps-=float(total)
                paidps+=float(total)
            if i[3]=="Cash Payment" and i[2]=="Supplier":
                total = float(i[5])
                duep-=float(total)   
                paidp+=float(total)  
        self.prt.setText(str(prtotal)) 
        self.prp.setText(str(prpaid)) 
        srlose = srtotalv-srbuyv 
        self.srt.setText(str(srtotalv)) 
        self.srp.setText(str(srpaid)) 
        self.srps.setText(str(srlose))   

        self.totalapdues.setText(str(dueps))
        self.totalapduep.setText(str(duep))
        self.totalpaids.setText(str(paidps))
        self.totalpaidp.setText(str(paidp))
        result = cur.execute("SELECT sales.invoice,strftime('%d/%m/%Y',sales.date),customer.name as cname,products.name as pname,sales.price,sales.qtn,products.unit,sales.discount,sales.type,products.buyrate FROM sales INNER JOIN customer ON sales.cid=customer.id INNER JOIN products ON sales.pid=products.id  WHERE sales.date BETWEEN ? AND ? ",(fromd,tod,))
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
        totalfinal = totalps-srtotalv 
        totalfinalpaid = paidps-srpaid
        profitfinalvalue = profit - srlose
        self.profitv.setText(str(profit))
        self.sft.setText(str(totalfinal))
        self.sfp.setText(str(totalfinalpaid))
        self.stprofitfinal.setText(str(profitfinalvalue))
        cur.close() 

    def loadOverviewData(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id,strftime('%d/%m/%Y',date),type,paytype,des,amount FROM cash ORDER BY id DESC")
        data3 = self.cur.fetchall()

        result = cur.execute("SELECT pinvoice.invoice,strftime('%d/%m/%Y',pinvoice.date),supplier.name as sname,pinvoice.vat,pinvoice.labour,pinvoice.discount,pinvoice.paid,pinvoice.total FROM pinvoice INNER JOIN supplier ON pinvoice.sid=supplier.id  ORDER BY pinvoice.id DESC")
        data = result.fetchall()
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
        self.totalap.setText(str(totalp))
        pr = cur.execute("SELECT preturn.id,strftime('%d/%m/%Y',preturn.date),supplier.name as sname,products.name as pname,preturn.price,preturn.qtn,products.unit,preturn.discount,preturn.paid FROM preturn INNER JOIN supplier ON preturn.sid=supplier.id INNER JOIN products ON preturn.pid=products.id  ORDER BY preturn.id DESC")
        prdata = pr.fetchall()
        prtotal =0
        prpaid =0
        for index,i in enumerate(prdata):
            price = float(i[4])
            qtn = float(i[5])
            prtotal += price*qtn-float(i[7])
            prpaid+=float(i[8])
        result = cur.execute("SELECT sinvoice.invoice,strftime('%d/%m/%Y',sinvoice.date),customer.name as cname,sinvoice.vat,sinvoice.labour,sinvoice.discount,sinvoice.paid,sinvoice.total,sinvoice.paytype FROM sinvoice INNER JOIN customer ON sinvoice.cid=customer.id  ORDER BY sinvoice.id DESC")
        data2 = result.fetchall()
        totalps = 0
        dueps = 0
        paidps=0
        for index,i in enumerate(data2):
            total = i[7]
            paid = i[6]
            due = float(total) - float(paid)
            dueps+=due
            totalps+=float(total)
            paidps+=float(paid)            
        self.totalsp.setText(str(totalps))
        srd = cur.execute("SELECT sreturn.id,strftime('%d/%m/%Y',sreturn.date),customer.name as cname,products.name as pname,sreturn.price,sreturn.qtn,products.unit,sreturn.discount,sreturn.paid,products.buyrate  FROM sreturn INNER JOIN customer ON sreturn.cid=customer.id INNER JOIN products ON sreturn.pid=products.id ")
        srdata = srd.fetchall()
        srtotalv =0
        srbuyv =0
        srpaid =0
        for index,i in enumerate(srdata):
            price = float(i[4])
            qtn = float(i[5])
            total = price*qtn
            dis = float(i[7])
            srtotalv += total-dis
            buy = float(i[9])
            srbuyv+=buy*qtn 
            srpaid+=float(i[8])          
        for index, i in enumerate(data3):
            if i[3]=="Cash Receive" and i[2]=="Customer":
                total = float(i[5])
                dueps-=float(total)
                paidps+=float(total)
            if i[3]=="Cash Payment" and i[2]=="Supplier":
                total = float(i[5])
                duep-=float(total)   
                paidp+=float(total)     
        self.prt.setText(str(prtotal)) 
        self.prp.setText(str(prpaid))      
        srlose = srtotalv-srbuyv 
        self.srt.setText(str(srtotalv)) 
        self.srp.setText(str(srpaid)) 
        self.srps.setText(str(srlose))                    
        self.totalapdues.setText(str(dueps))
        self.totalapduep.setText(str(duep))
        self.totalpaids.setText(str(paidps))
        self.totalpaidp.setText(str(paidp))

        amountin =0
        amountout=0
        customerpay=0
        supplierpay=0
        officialin=0
        officialout=0
        for index, i in enumerate(data3):
            if i[3]=="Cash Receive" or i[3]=="Deposit":
                amountin+=float(i[5])
                if i[2]=="Customer":
                    customerpay+=float(i[5])
                if i[2]=="Official":
                    officialin+=float(i[5])                    
            else:
                amountin+=0   
            if i[3]=="Cash Payment" or i[3]=="Withdrew":
                amountout+=float(i[5])  
                if i[2]=="Supplier":
                    supplierpay+=float(i[5])
                if i[2]=="Official":
                    officialout+=float(i[5])                                
            else:
                amountout+=0  
        self.totalcashin.setText(str(amountout))       
        self.totalcashout.setText(str(amountin)) 

        self.recieve.setText(str(customerpay))       
        self.payment.setText(str(supplierpay)) 

        self.offrecieve.setText(str(officialin))       
        self.offout.setText(str(officialout)) 

        result = cur.execute("SELECT sales.invoice,strftime('%d/%m/%Y',sales.date),customer.name as cname,products.name as pname,sales.price,sales.qtn,products.unit,sales.discount,sales.type,products.buyrate FROM sales INNER JOIN customer ON sales.cid=customer.id INNER JOIN products ON sales.pid=products.id  ORDER BY sales.id DESC")
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
        totalfinal = totalps-srtotalv 
        totalfinalpaid = paidps-srpaid
        profitfinalvalue = profit - srlose
        self.profitv.setText(str(profit))
        self.sft.setText(str(totalfinal))
        self.sfp.setText(str(totalfinalpaid))
        self.stprofitfinal.setText(str(profitfinalvalue))
        cur.close()


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
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),account.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' AND cash.date BETWEEN ? AND ?",(fromd,tod,))
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
                self.officialpay.setItem(index,6,QTableWidgetItem(i[7]))
                self.officialpay.setItem(index,7,QTableWidgetItem(i[8]))
                self.officialpay.setItem(index,8,QTableWidgetItem(i[9]))
            self.opayshowout.setText(str(valueout)) 
            self.opayshowin.setText(str(valuein))
        else:
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),account.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' and account.name LIKE ? AND cash.date BETWEEN ? AND ?",("%"+sv+"%",fromd,tod,))
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
                self.officialpay.setItem(index,6,QTableWidgetItem(i[7]))
                self.officialpay.setItem(index,7,QTableWidgetItem(i[8]))
                self.officialpay.setItem(index,8,QTableWidgetItem(i[9]))                
            self.opayshowout.setText(str(valueout)) 
            self.opayshowin.setText(str(valuein))
        cur.close()    

    def officialspaySearch(self):
        sv = self.svop.text()
        cur = self.conn.cursor()
        if sv!="":
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),account.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' and account.name LIKE ?",("%"+sv+"%",))
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
                self.officialpay.setItem(index,6,QTableWidgetItem(i[7]))
                self.officialpay.setItem(index,7,QTableWidgetItem(i[8]))
                self.officialpay.setItem(index,8,QTableWidgetItem(i[9]))                

            self.opayshowout.setText(str(valueout)) 
            self.opayshowin.setText(str(valuein))
        cur.close()    

    def officialspay(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),account.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN account ON cash.accid=account.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Official' ORDER BY cash.id DESC")
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
            self.officialpay.setItem(index,6,QTableWidgetItem(i[7]))
            self.officialpay.setItem(index,7,QTableWidgetItem(i[8]))
            self.officialpay.setItem(index,8,QTableWidgetItem(i[9]))            
        self.opayshowout.setText(str(valueout)) 
        self.opayshowin.setText(str(valuein))
        cur.close() 
    
    def viewcustomerdate(self):
        sv = self.svcp.text()
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')

        date_current = self.fromd_2.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date

        date_current = self.tod_2.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime 
        cur = self.conn.cursor()
        if sv=="":        
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),customer.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN customer ON cash.cid=customer.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Customer' AND cash.date BETWEEN ? AND ?",(fromd,tod,))
            result=result.fetchall()
            self.customerpay.setRowCount(len(result))
            value = 0
            for index, i in enumerate(result):
                total = float(i[5])
                value+=float(total)
                self.customerpay.setItem(index,0,QTableWidgetItem(i[1]))
                self.customerpay.setItem(index,1,QTableWidgetItem(i[2]))
                self.customerpay.setItem(index,2,QTableWidgetItem(i[3]))
                self.customerpay.setItem(index,3,QTableWidgetItem(i[4]))
                self.customerpay.setItem(index,4,QTableWidgetItem(i[5]))
                self.customerpay.setItem(index,5,QTableWidgetItem(i[6]))
                self.customerpay.setItem(index,6,QTableWidgetItem(i[7]))
                self.customerpay.setItem(index,7,QTableWidgetItem(i[8]))
                self.customerpay.setItem(index,8,QTableWidgetItem(i[9]))                
            self.cpayshow.setText(str(value))
        else:
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),customer.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN customer ON cash.cid=customer.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Customer' and customer.name LIKE ? OR customer.id LIKE ? OR customer.partycode LIKE ? AND cash.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",fromd,tod,))
            result=result.fetchall()
            self.customerpay.setRowCount(len(result))
            value = 0
            for index, i in enumerate(result):
                total = float(i[5])
                value+=float(total)
                self.customerpay.setItem(index,0,QTableWidgetItem(i[1]))
                self.customerpay.setItem(index,1,QTableWidgetItem(i[2]))
                self.customerpay.setItem(index,2,QTableWidgetItem(i[3]))
                self.customerpay.setItem(index,3,QTableWidgetItem(i[4]))
                self.customerpay.setItem(index,4,QTableWidgetItem(i[5]))
                self.customerpay.setItem(index,5,QTableWidgetItem(i[6]))
                self.customerpay.setItem(index,6,QTableWidgetItem(i[7]))
                self.customerpay.setItem(index,7,QTableWidgetItem(i[8]))
                self.customerpay.setItem(index,8,QTableWidgetItem(i[9]))            
            self.cpayshow.setText(str(value))
        cur.close()    

    def loadallcustomer(self):
        self.cuspay()

    def cuspaySearch(self):
        sv = self.svcp.text()
        cur = self.conn.cursor()
        if sv!="":
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),customer.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN customer ON cash.cid=customer.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Customer' and customer.name LIKE ? OR customer.id LIKE ? OR customer.partycode LIKE ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
            result=result.fetchall()
            self.customerpay.setRowCount(len(result))
            value = 0
            for index, i in enumerate(result):
                total = float(i[5])
                value+=float(total)
                self.customerpay.setItem(index,0,QTableWidgetItem(i[1]))
                self.customerpay.setItem(index,1,QTableWidgetItem(i[2]))
                self.customerpay.setItem(index,2,QTableWidgetItem(i[3]))
                self.customerpay.setItem(index,3,QTableWidgetItem(i[4]))
                self.customerpay.setItem(index,4,QTableWidgetItem(i[5]))
                self.customerpay.setItem(index,5,QTableWidgetItem(i[6]))
                self.customerpay.setItem(index,6,QTableWidgetItem(i[7]))
                self.customerpay.setItem(index,7,QTableWidgetItem(i[8]))
                self.customerpay.setItem(index,8,QTableWidgetItem(i[9]))                
            self.cpayshow.setText(str(value)) 
        cur.close()    

    def cuspay(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),customer.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN customer ON cash.cid=customer.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Customer' ORDER BY cash.id DESC")
        result=result.fetchall()
        self.customerpay.setRowCount(len(result))
        value = 0
        for index, i in enumerate(result):
            total = float(i[5])
            value+=float(total)
            self.customerpay.setItem(index,0,QTableWidgetItem(i[1]))
            self.customerpay.setItem(index,1,QTableWidgetItem(i[2]))
            self.customerpay.setItem(index,2,QTableWidgetItem(i[3]))
            self.customerpay.setItem(index,3,QTableWidgetItem(i[4]))
            self.customerpay.setItem(index,4,QTableWidgetItem(i[5]))
            self.customerpay.setItem(index,5,QTableWidgetItem(i[6]))
            self.customerpay.setItem(index,6,QTableWidgetItem(i[7]))
            self.customerpay.setItem(index,7,QTableWidgetItem(i[8]))
            self.customerpay.setItem(index,8,QTableWidgetItem(i[9]))
        self.cpayshow.setText(str(value)) 
        cur.close() 

    def supplierpaydate(self):
        sv = self.svsp.text()
        time = QTime.currentTime()
        currenttime = time.toString('hh:mm:ss')

        date_current = self.fromd.date() 
        date = date_current.toString("yyyy-MM-dd")
        fromd = date

        date_current = self.tod.date() 
        date = date_current.toString("yyyy-MM-dd")
        tod = date+" "+currenttime 
        cur = self.conn.cursor()
        if sv=="":
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),supplier.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN supplier ON cash.sid=supplier.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Supplier' AND cash.date BETWEEN ? AND ?",(fromd,tod,))
            result=result.fetchall()
            self.supplierpayment.setRowCount(len(result))
            value = 0
            for index, i in enumerate(result):
                total = float(i[5])
                value+=float(total)
                self.supplierpayment.setItem(index,0,QTableWidgetItem(i[1]))
                self.supplierpayment.setItem(index,1,QTableWidgetItem(i[2]))
                self.supplierpayment.setItem(index,2,QTableWidgetItem(i[3]))
                self.supplierpayment.setItem(index,3,QTableWidgetItem(i[4]))
                self.supplierpayment.setItem(index,4,QTableWidgetItem(i[5]))
                self.supplierpayment.setItem(index,5,QTableWidgetItem(i[6]))
                self.supplierpayment.setItem(index,6,QTableWidgetItem(i[7]))
                self.supplierpayment.setItem(index,7,QTableWidgetItem(i[8]))
                self.supplierpayment.setItem(index,8,QTableWidgetItem(i[9]))                
            self.spayshow.setText(str(value)) 
        else:
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),supplier.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN supplier ON cash.sid=supplier.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Supplier' and supplier.name LIKE ? OR supplier.id LIKE ? OR supplier.partycode LIKE ? AND cash.date BETWEEN ? AND ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",fromd,tod,))
            result=result.fetchall()
            self.supplierpayment.setRowCount(len(result))
            value = 0
            for index, i in enumerate(result):
                total = float(i[5])
                value+=float(total)
                self.supplierpayment.setItem(index,0,QTableWidgetItem(i[1]))
                self.supplierpayment.setItem(index,1,QTableWidgetItem(i[2]))
                self.supplierpayment.setItem(index,2,QTableWidgetItem(i[3]))
                self.supplierpayment.setItem(index,3,QTableWidgetItem(i[4]))
                self.supplierpayment.setItem(index,4,QTableWidgetItem(i[5]))
                self.supplierpayment.setItem(index,5,QTableWidgetItem(i[6]))
                self.supplierpayment.setItem(index,6,QTableWidgetItem(i[7]))
                self.supplierpayment.setItem(index,7,QTableWidgetItem(i[8]))
                self.supplierpayment.setItem(index,8,QTableWidgetItem(i[9]))
            self.spayshow.setText(str(value))  
        cur.close()                   

    def loadsup(self):
        self.supplierpay()

    def supplierpaySearch(self):
        sv = self.svsp.text()
        cur = self.conn.cursor()
        if sv!="":
            result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),supplier.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN supplier ON cash.sid=supplier.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Supplier' and supplier.name LIKE ? OR supplier.id LIKE ? OR supplier.partycode LIKE ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
            result=result.fetchall()
            self.supplierpayment.setRowCount(len(result))
            value = 0
            for index, i in enumerate(result):
                total = float(i[5])
                value+=float(total)
                self.supplierpayment.setItem(index,0,QTableWidgetItem(i[1]))
                self.supplierpayment.setItem(index,1,QTableWidgetItem(i[2]))
                self.supplierpayment.setItem(index,2,QTableWidgetItem(i[3]))
                self.supplierpayment.setItem(index,3,QTableWidgetItem(i[4]))
                self.supplierpayment.setItem(index,4,QTableWidgetItem(i[5]))
                self.supplierpayment.setItem(index,5,QTableWidgetItem(i[6]))
                self.supplierpayment.setItem(index,6,QTableWidgetItem(i[7]))
                self.supplierpayment.setItem(index,7,QTableWidgetItem(i[8]))
                self.supplierpayment.setItem(index,8,QTableWidgetItem(i[9]))                
            self.spayshow.setText(str(value)) 
        cur.close()     

    def supplierpay(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT cash.id,strftime('%d/%m/%Y',cash.date),supplier.name,cash.paytype,cash.des,cash.amount,cash.bankname,cash.chqnumber,cash.trxid,users.name FROM cash INNER JOIN supplier ON cash.sid=supplier.id LEFT JOIN users ON cash.uid=users.id WHERE cash.type='Supplier' ORDER BY cash.id DESC")
        result=result.fetchall()
        self.supplierpayment.setRowCount(len(result))
        value = 0
        for index, i in enumerate(result):
            total = float(i[5])
            value+=float(total)
            self.supplierpayment.setItem(index,0,QTableWidgetItem(i[1]))
            self.supplierpayment.setItem(index,1,QTableWidgetItem(i[2]))
            self.supplierpayment.setItem(index,2,QTableWidgetItem(i[3]))
            self.supplierpayment.setItem(index,3,QTableWidgetItem(i[4]))
            self.supplierpayment.setItem(index,4,QTableWidgetItem(i[5]))
            self.supplierpayment.setItem(index,5,QTableWidgetItem(i[6]))
            self.supplierpayment.setItem(index,6,QTableWidgetItem(i[7]))
            self.supplierpayment.setItem(index,7,QTableWidgetItem(i[8]))
            self.supplierpayment.setItem(index,8,QTableWidgetItem(i[9]))
        self.spayshow.setText(str(value))
        cur.close() 

    def cusAll(self):
        self.customerDue()
    def supAll(self):
        self.supplierDue()

    def dueSearchSup(self):
        sv = self.suppliers.text()
        cur = self.conn.cursor()
        if sv !="":
            result = cur.execute("SELECT id,name,phone FROM supplier WHERE id LIKE ? OR name LIKE ? OR partycode LIKE ?",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
            result=result.fetchall()
            self.supplierdue.setRowCount(len(result))
            value = 0
            for index, i in enumerate(result):
                total = balsup.bal(i[0])
                value+=float(total)
                self.supplierdue.setItem(index,0,QTableWidgetItem(str(i[0])))
                self.supplierdue.setItem(index,1,QTableWidgetItem(i[1]))
                self.supplierdue.setItem(index,2,QTableWidgetItem(i[2]))
                self.supplierdue.setItem(index,3,QTableWidgetItem(str(total)))
            self.totalduesup.setText(str(value))
        cur.close()                

    def supplierDue(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,name,phone FROM supplier ")
        result=result.fetchall()
        self.supplierdue.setRowCount(len(result))
        value = 0
        for index, i in enumerate(result):
            total = balsup.bal(i[0])
            value+=float(total)
            self.supplierdue.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.supplierdue.setItem(index,1,QTableWidgetItem(i[1]))
            self.supplierdue.setItem(index,2,QTableWidgetItem(i[2]))
            self.supplierdue.setItem(index,3,QTableWidgetItem(str(total)))
        self.totalduesup.setText(str(value))  
        cur.close()

    def customerDueSearch(self):
        sv = self.customers.text()
        cur = self.conn.cursor()
        if sv!="":
            result = cur.execute("SELECT id,name,phone FROM customer WHERE id LIKE ? OR name LIKE ? OR partycode LIKE ? ",("%"+sv+"%","%"+sv+"%","%"+sv+"%",))
            result=result.fetchall()
            self.customerdue.setRowCount(len(result))
            value = 0
            for index, i in enumerate(result):
                total = balcus.bal(i[0])
                value+=float(total)
                self.customerdue.setItem(index,0,QTableWidgetItem(str(i[0])))
                self.customerdue.setItem(index,1,QTableWidgetItem(i[1]))
                self.customerdue.setItem(index,2,QTableWidgetItem(i[2]))
                self.customerdue.setItem(index,3,QTableWidgetItem(str(total)))
            self.totalduecus.setText(str(value)) 
        cur.close()    

    def customerDue(self):
        cur = self.conn.cursor()
        result = cur.execute("SELECT id,name,phone FROM customer ")
        result=result.fetchall()
        self.customerdue.setRowCount(len(result))
        value = 0
        for index, i in enumerate(result):
            total = balcus.bal(i[0])
            value+=float(total)
            self.customerdue.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.customerdue.setItem(index,1,QTableWidgetItem(i[1]))
            self.customerdue.setItem(index,2,QTableWidgetItem(i[2]))
            self.customerdue.setItem(index,3,QTableWidgetItem(str(total)))
        self.totalduecus.setText(str(value))  
        cur.close()      




