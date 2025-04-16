from flask import Flask, render_template, request, session
from Cryptodome.Cipher import AES
import string,base64
import sqlite3 as sql

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
app = Flask(__name__)

@app.route('/')
def index():
	session['logged_in'] = False
	session['user'] = ""
	return render_template('login.html')

@app.route('/add.html')
def new_user():
	if not session.get("logged_in"):
		return render_template('login.html')
	if session.get('role') < 3:
		return render_template('not_found.html')
	return render_template('add.html')

@app.route('/addentry.html')
def new_entry():
	if not session.get("logged_in"):
		return render_template('login.html')
	return render_template('addentry.html')

@app.route('/home.html')
def home():
	if not session.get("logged_in"):
		return render_template('login.html')
	user = session['user']
	return render_template('home.html', user = user, name = cipher.decrypt(user[0]))

@app.route('/addrec', methods = ['POST', 'GET'])
def addrec():
	if not session.get("logged_in"):
		return render_template('login.html')
	if session.get('role') < 3:
		return render_template('not_found.html')
	msg = ""
	if request.method == 'POST':
		name = request.form['Name']
		age = request.form['Age']
		number = request.form['Number']
		security = request.form['Security']
		password = request.form['Password']
		if(name.isspace() or name == ""):
			msg = msg + "You can not enter in an empty name\n"
		try:
			if((int(age) > 120 or int(age) < 1)):
				msg = msg + "The Age must be a whole number greater than 0 and less than 121\n"
		except ValueError:
			msg = msg + "The Age must be a whole number greater than 0 and less than 121\n"
		if(number.isspace() or number == ""):
			msg = msg + "You can not enter in an empty phone number\n"
		try:
			if((int(security) < 1 or int(security)  > 3)):
				msg = msg + "The Security Level must be a numeric between 1 and 3\n"
		except ValueError:
			msg = msg + "The Security Level must be a numeric between 1 and 3\n"
		if(password.isspace() or password == ""):
			msg = msg + "You can not enter in an empty password\n"
		if(msg == ""):
			name = cipher.encrypt(bytes(name, 'utf-8'))
			number = cipher.encrypt(bytes(str(number), 'utf-8'))
			password = cipher.encrypt(bytes(str(password), 'utf-8'))
			msg = "Record successfully added"
			with sql.connect('BakingDB.db') as con:
				cur = con.cursor()

				cur.execute('''Insert INTO BAKER(Name, Age, Number, Security, Password) VALUES
					(?, ?, ?, ?, ?)''',(name, age, number, security, password) )
		msg = msg.split('\n')
		return render_template("results.html", msg=msg)

@app.route('/addentry', methods = ['POST', 'GET'])
def addentry():
	if not session.get("logged_in"):
		return render_template('login.html')
	msg = ""
	if request.method == 'POST':
		name = request.form['Name']
		excellent = request.form['Excellent']
		ok = request.form['Ok']
		bad = request.form['Bad']
		if(name.isspace() or name == ""):
			msg = msg + "You can not enter in an empty name\n"
		try:
			if((int(excellent) < 0)):
				msg = msg + "Number must be greater than 0\n"
		except ValueError:
			msg = msg + "Must be a number\n"
		try:
			if((int(ok) < 0)):
				msg = msg + "Number must be greater than 0\n"
		except ValueError:
			msg = msg + "Must be a number\n"
		try:
			if((int(bad) < 0)):
				msg = msg + "Number must be greater than 0\n"
		except ValueError:
			msg = msg + "Must be a number\n"
		if msg == "":
			msg = "Entry Successfully added"
			with sql.connect('BakingDB.db') as con:
					cur = con.cursor()

					cur.execute('''Insert Into RESULT('EntryId', 'UserId', 'Item', 'NumExcellent', 'NumOK', 'NumBad')
					Values(?, ?, ?, ?, ?, ?)''', (1, session['user'][0], name, excellent, ok, bad))
		
		msg = msg.split('\n')
		return render_template("results.html", msg=msg)

@app.route('/list.html')
def list():
	if not session.get("logged_in"):
		return render_template('login.html')
	if session.get('role') < 2:
		return render_template('not_found.html')
	con = sql.connect('BakingDB.db')
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("select * from Baker")

	rows = cur.fetchall()

	decrypted_rows=[]
	for row in rows:
		col = []
		col.append(cipher.decrypt(row["Name"]))
		col.append(row["Age"])
		col.append(cipher.decrypt(row["Number"]))
		col.append(row["Security"])
		col.append(cipher.decrypt(row["Password"]))
		decrypted_rows.append(col)

	return render_template("list.html", rows = decrypted_rows)

@app.route('/contestResults.html')
def listResults():
	if not session.get("logged_in"):
		return render_template('login.html')
	if session.get('role') < 3:
		return render_template('not_found.html')
	con = sql.connect('BakingDB.db')
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("SELECT * FROM result;")

	rows = cur.fetchall()
	decrypted_rows=[]
	for row in rows:
		col = []
		col.append((row["EntryId"]))
		col.append(cipher.decrypt(row["UserId"]))
		col.append(row["Item"])
		col.append(row["NumExcellent"])
		col.append(row["NumOk"])
		col.append(row["NumBad"])
		decrypted_rows.append(col)
	print(decrypted_rows)
	return render_template('contestResults.html', rows = decrypted_rows)

@app.route('/myentry.html')
def listmyentries():
	if not session.get("logged_in"):
		return render_template('login.html')
	con = sql.connect('BakingDB.db')
	con.row_factory = sql.Row
	user = session['user']

	cur = con.cursor()
	cur.execute("SELECT * FROM Result WHERE UserID = ?", (user[0],))

	rows = cur.fetchall()
	return render_template('myentry.html', rows = rows)

@app.route('/login.html', methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		name = cipher.encrypt(bytes(request.form['Name'], 'utf-8'))
		password = cipher.encrypt(bytes(request.form['Password'], 'utf-8'))
		con = sql.connect('BakingDB.db')
		cur = con.cursor()
		cur.execute("SELECT * FROM Baker WHERE Name = ? AND Password = ?", (name, password))
		user = cur.fetchone()
		con.close()
		if user:
			session['user'] = user
			session['role'] = user[3]
			session['logged_in'] = True
			user = session['user']
			return render_template('home.html', user = user, name = user[0])
		else:
			return render_template('login.html', error = 'true')

if __name__ == '__main__':
	key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
	iv = b'OWFJATh1Zowac2xr'
	cipher = AESCipher(key,iv)

	app.secret_key = '1234567679'
	app.run(host = '127.0.0.1', port = 65535)
