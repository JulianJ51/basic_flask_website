import sqlite3
from Cryptodome.Cipher import AES
import string,base64

class AESCipher(object):
    def __init__(self, key,iv):
        self.key = key
        self.iv = iv

    def encrypt(self, raw):
        self.cipher = AES.new(self.key, AES.MODE_CFB,self.iv)
        ciphertext = self.cipher.encrypt(raw)
        encoded = base64.b64encode(ciphertext)
        return encoded

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        self.cipher = AES.new(self.key, AES.MODE_CFB,self.iv)
        decrypted = self.cipher.decrypt(decoded)
        return str(decrypted, 'utf-8')

key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
iv = b'OWFJATh1Zowac2xr'
cipher = AESCipher(key,iv)

name1 = cipher.encrypt(bytes('julian', 'utf-8'))
name2 = cipher.encrypt(bytes('nick', 'utf-8'))
name3 = cipher.encrypt(bytes('natalie', 'utf-8'))
number1 = cipher.encrypt(bytes(str(407), 'utf-8'))
number2 = cipher.encrypt(bytes(str(850), 'utf-8'))
number3 = cipher.encrypt(bytes(str(912), 'utf-8'))
password1 = cipher.encrypt(bytes('j345', 'utf-8'))
password2 = cipher.encrypt(bytes('n234', 'utf-8'))
password3 = cipher.encrypt(bytes('n123', 'utf-8'))

conn = sqlite3.connect('BakingDB.db')

cur = conn.cursor()

try:
    conn.execute('''Drop table Baker''')

    conn.commit()
    print('Baker table dropped.')
except:
    print('Baker table did not exist')


#create table in database
cur.execute('''CREATE TABLE BAKER(
Name TEXT NOT NULL,
Age INTEGER NOT NULL,
Number INTEGER NOT NULL,
Security INTEGER NOT NULL,
Password TEXT NOT NULL);
''')
conn.commit()

cur.execute('''Insert Into Baker('Name', 'Age', 'Number', 'Security', 'Password')
Values(?, ?, ?, ?, ?)''', (name1, 21, number1, 3, password1))

conn.commit()

cur.execute('''Insert Into Baker('Name', 'Age', 'Number', 'Security', 'Password')
Values(?, ?, ?, ?, ?)''', (name2, 24, number2, 2, password2))

conn.commit()

cur.execute('''Insert Into Baker('Name', 'Age', 'Number', 'Security', 'Password')
Values(?, ?, ?, ?, ?)''', (name3, 12, number3, 1, password3))

conn.commit()

for row in cur.execute('SELECT * FROM Baker;'):
    print(row)

#save changes
print('Baker Table Created.')

try:
    conn.execute('''Drop table Result''')

    conn.commit()
    print('Result table dropped.')
except:
    print('Result table did not exist')

cur.execute('''CREATE TABLE RESULT(
EntryId INTEGER NOT NULL,
UserId TEXT NOT NULL,
Item TEXT NOT NULL,
NumExcellent INTEGER NOT NULL,
NumOK INTEGER NOT NULL,
NumBad INTEGER NOT NULL);
''')

conn.commit()
print('Result table created')

cur.execute('''Insert Into RESULT('EntryId', 'UserId', 'Item', 'NumExcellent', 'NumOK', 'NumBad')
Values(?, ?, ?, ?, ?, ?)''', (1, name1, 'Cookie', 2, 4, 0))

conn.commit()

cur.execute('''Insert Into RESULT('EntryId', 'UserId', 'Item', 'NumExcellent', 'NumOK', 'NumBad')
Values(?, ?, ?, ?, ?, ?)''', (2, name2, 'Brownie', 4, 2, 0))

conn.commit()

cur.execute('''Insert Into RESULT('EntryId', 'UserId', 'Item', 'NumExcellent', 'NumOK', 'NumBad')
Values(?, ?, ?, ?, ?, ?)''', (3, name3, 'Cookie', 2, 4, 0))

conn.commit()

for row in cur.execute('SELECT * FROM Result;'):
    print(row)

conn.close()
print('Connection closed.')