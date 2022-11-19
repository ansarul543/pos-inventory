
import sqlite3

class SupplierBalance:
    def __init__(self,id=''):
        self.id = id
        self.conn = sqlite3.connect('./database/data.db')
        self.cur = self.conn.cursor()
    
    
    def bal(self,id):
            cu = self.cur.execute("SELECT id,name,address,phone FROM supplier WHERE id=? ",(id,))
            supplier = cu.fetchone()
            
            sql="""SELECT id,invoice,stype,paid,total,strftime('%d/%m/%Y',date) as date FROM pinvoice WHERE sid=? """
            da = self.cur.execute(sql,(id,))
            result = da.fetchall()

            sql="""SELECT paytype,amount,des,strftime('%d/%m/%Y',date) as date FROM cash WHERE sid=? and type='Supplier' """
            cas = self.cur.execute(sql,(id,))
            cash = cas.fetchall()

            sql="""SELECT price,qtn,discount,strftime('%d/%m/%Y',date) as date,paid FROM preturn WHERE sid=? """
            retur = self.cur.execute(sql,(id,))
            repro = retur.fetchall()
            total =0
            paid = 0       
            for index, i in enumerate(result):
                total+=float(i[4])
                paid +=float(i[3])           
            for index, i in enumerate(cash):
                paid +=float(i[1])        
            for index, i in enumerate(repro):
                paid -=float(i[4])
                total -= float(i[0])*float(i[1])-float(i[2])          
            bal = total-paid
            return bal       


