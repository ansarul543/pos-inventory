import sqlite3

conn = sqlite3.connect('./database/data.db')
cur = conn.cursor()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'account'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'cash'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'category'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'customer'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'damage'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'loginhistory'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'pinvoice'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'ppp'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'preturn'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'proadjust'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'products'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'purchase'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'sales'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'sinvoice'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'sreturn'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'sss'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'supplier'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'unit'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'users'")
conn.commit()

cur.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'pledger'")
conn.commit()

print("Ok")