from flask import Flask, render_template, redirect, session, g, url_for, request
from flask_mysqldb import MySQL
import os

app=Flask(__name__)
app.secret_key = os.urandom(20)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='arun12345'
app.config['MYSQL_DB']='userflask'


mysql=MySQL(app)

@app.before_request
def before_request():
	g.id=None
  if 'id' in session:
                g.id=session['id']

@app.route('/', methods=['GET','POST'])
def home():
	if request.method=="POST":
		email=request.form['email']
		name=request.form['name']
		password=request.form['password']
		cur=mysql.connection.cursor()
		cur.execute("SELECT * FROM users WHERE email='{}' and password='{}'".format(email, password))
		data=cur.fetchone()
		cur.close()
		if data:
			msg='Email already register'
			return render_template('home.html', msg=msg)
		elif data is None:
			cur=mysql.connection.cursor()
			cur.execute("INSERT INTO users(name, email, password) VALUES('{}', '{}', '{}')".format(name,email,password))
			mysql.connection.commit()
			data=cur.fetchone()
			print(data)
			cur.close()
			msg='Account created successfully, Now click on login button'
			return render_template('home.html',msg=msg)
	return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method=='POST':
		email=request.form['email']
		password=request.form['password']
		cur=mysql.connection.cursor()
		cur.execute("SELECT * FROM users WHERE email='{}' and password='{}'".format(email, password))
		data=cur.fetchone()
		cur.close()
		if data is None:
			msg='Email/password maybe incorrect'
			return render_template('login.html', msg=msg)
		elif data:
			session['id']=data[0]
			session['loggedin']=True
			return redirect(url_for('welcome'))
	return render_template('login.html')

@app.route('/welcome')
def welcome():
	if g.id:
		return render_template('welcome.html')
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id',None)
	return redirect(url_for('home'))
			
@app.errorhandler(404)
def handle_bad_request(error):
	return '404 Not found'




if __name__ == '__main__':
	app.run('0.0.0.0', debug=True)

