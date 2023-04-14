from flask import Flask, render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:mike2002@localhost'
db = SQLAlchemy(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mike2002",
)


mycursor = mydb.cursor()

mycursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;")

myresult = mycursor.fetchall()
available = []
for database in myresult:
  print(database[0])
  tables = []
  if database[0] not in ['mysql', 'information_schema', 'performance_schema','sys']:
    mycursor.execute(f"USE {database[0]}") # select the database
    mycursor.execute("SHOW TABLES")
    for (table_name,) in mycursor:
          tables.append(table_name)
    available.append((database[0],tables))

print(available)

mycursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;")

myresult = mycursor.fetchall()


@app.route('/login', methods=['POST',"GET"])
def home():
    # Get the form data
    username = request.form['username']
    password = request.form['password']
    host = request.form['host']
    port = request.form['port']

    # Connect to MySQL database using the provided host and port
    # and check if username and password match your database records
    
    return render_template('index.html',myresult=myresult, username=username, host=host, port=port,available=available)

@app.route('/')
def login():
    return render_template('login.html')




@app.route('/database', methods=['POST'])
def view_table():
    
    data  = request.form
    value = data.getlist('value')[0]
    value = value.split(",")
    db = value[0]
    table = value[1]

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mike2002",
    database = db
    )
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM {table} LIMIT 50;")

    myresult = mycursor.fetchall()

    print('Showing '+db+'.'+table)

    return render_template('database.html',myresult= myresult,table=table, )

@app.route('/table_menu', methods=['POST'])
def table_menu():
    action  = request.form
    value = action.getlist(0)
    print(value)
    mycursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    return value