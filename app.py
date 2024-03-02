from flask import Flask,render_template,redirect,url_for
from forms import RegisterForm
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
 return render_template('index.html')
@app.route("/login")
def login():
 return render_template("login.html")

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
 return render_template("dashboard.html")


if __name__=="__main__":
 app.run(debug=True)
