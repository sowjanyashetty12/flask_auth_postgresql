from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,ValidationError
import email_validator,psycopg2
class RegisterForm(FlaskForm):
    username=StringField('Name',validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Submit')
    # defining custom validation 
    def validate_email(self,field):
      conn=psycopg2.connect(
    database="flask_pg",host="localhost",user="postgres",password="shetty12",port="5432"
) 
      cur=conn.cursor()
      cur.execute('''SELECT * FROM  users WHERE email=%s''',(field.data,))
      user=cur.fetchone()
      cur.close()
      conn.close()
      if user:
         raise ValidationError("Email already taken")
         

class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Submit")