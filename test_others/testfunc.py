

"""
from cryptography.fernet import Fernet
message = "0"
key = Fernet.generate_key()
fernet = Fernet(key)

decMessage = fernet.decrypt(encMessage).decode()
print(decMessage)
"""



import datetime

date = datetime.datetime.now() + datetime.timedelta(days=7)
print(date)

currentdate = datetime.datetime.now() 
print(currentdate)

date = datetime.datetime.now() + datetime.timedelta(days=1)
print(date)

time = "2021-11-01 22:30:40.994952"
time = datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S.%f")

if(currentdate<time):
    print(True)
else:
    print(False)    
	

import cryptocode

encoded = cryptocode.encrypt("0","mypassword")
print(encoded)
decoded = cryptocode.decrypt("fw==*/MlcBAnJLVWXLC3y/Z3X6A==*TzgCKg7H2sAnHtqKb3Q7Tw==*Nf6Sb0oQj2qtCIHO2fM0nA==", "mypassword")
print(decoded)



















	
	