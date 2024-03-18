import psycopg2
conn=psycopg2.connect(
    database="flask_pg",host="localhost",user="postgres",password="shetty12",port="5432"
) 
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users(name varchar(100) NOT NULL,email varchar(100) NOT NULL,password varchar(100) NOT NULL)''')
cur.execute('''ALTER TABLE users ADD COLUMN userid SERIAL PRIMARY KEY''')
conn.commit()
cur.close()
conn.close()