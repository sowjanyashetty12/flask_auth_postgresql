from flask import Flask,render_template,redirect,url_for,session,flash
from forms import RegisterForm,LoginForm
import os
import bcrypt,psycopg2
app=Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

def db_connect():
  conn=psycopg2.connect(
    database="flask_pg",host="localhost",user="postgres",password="shetty12",port="5432"
) 
  return conn

@app.route('/')
def index():

 return render_template("index.html")
@app.route("/login" , methods=["post","get"])
def login():
  form=LoginForm()
  if form.validate_on_submit():
   email=form.email.data
   password=form.password.data
   conn=db_connect()
   cur=conn.cursor()
   cur.execute('''SELECT * FROM USERS WHERE email=%s''',(email,))
   user=cur.fetchone()
   cur.close()
   if user and password==user[2]:
     session['user_id']=user[3]
     return redirect(url_for("dashboard"))
   else:
     flash("Login failed . Please check your username and password")
     return redirect(url_for("login"))
  return render_template("login.html",form=form)

@app.route("/register", methods=["GET","POST"])
def signup():
    form=RegisterForm()
    if form.validate_on_submit():
     name=form.username.data
     email=form.email.data
     password=form.password.data
    #  hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    #  print(len(hashed_password))
     print(len(email))
     print(len(name))
     print("here")
     conn=db_connect()
     cur=conn.cursor()
     
     cur.execute('''INSERT INTO users(name,email,password) VALUES (%s,%s,%s)''',(name,email,password))
     print("executing")
     conn.commit()
     cur.close()
     conn.close()
     return redirect(url_for("login"))
    return render_template("signup.html",form=form)
    
@app.route("/dashboard")
def dashboard():
  if 'user_id' in session:
   userid=session['user_id']
   conn=db_connect()
   cur=conn.cursor()
   cur.execute('''SELECT * FROM USERS WHERE userid=%s''',(userid,))
   user=cur.fetchone()
   cur.close()
   if user:
     name=user[0]
     return render_template("dashboard.html",name=name)
  return redirect(url_for("login"))
@app.route("/logout")
def logingout():
 session.pop('user_id',None)
 flash("Logged out Successfully")
 return redirect(url_for("login"))

if __name__=="__main__":
 app.run(debug=True)