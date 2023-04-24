from flask import Flask, render_template,request,redirect, url_for
from sqlite3 import OperationalError
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import re


app = Flask(__name__)



#mydb = mysql.connector.connect(
#  host="localhost",
#  user="root",
#  password="mike2002",
#)

username= None
password= None
host= None
port= None


#mycursor = mydb.cursor()
#
#mycursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;")
#
#myresult = mycursor.fetchall()
#available = []
#for database in myresult:
#  tables = []
#  if database[0] not in ['mysql', 'information_schema', 'performance_schema','sys']:
#    mycursor.execute(f"USE {database[0]}") # select the database
#    mycursor.execute("SHOW TABLES")
#    for (table_name,) in mycursor:
#          tables.append(table_name)
#    available.append((database[0],tables))
#
#mycursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;")
#
#myresult = mycursor.fetchall()

#print(available)

@app.route('/login', methods=['POST',"GET"])
def home():
    # Get the form data
    global username
    global host
    global port
    global password
    filename = None
    try:

      host = request.form['host']
      username = request.form['username']
      password = request.form['password']
      port = request.form['port']
    except:
      print(request.form)
      data  = request.form
      value = data.getlist('value')[0]
      print('value:', value)
      value = value.split(",")
      filename = value[0]
      print(filename)


    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{host}:{password}@{username}'

    mydb = mysql.connector.connect(
      host=host,
      user=username,
      password=password,
      port = port
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;")

    myresult = mycursor.fetchall()
    available = []
    for database in myresult:
      tables = []
      if database[0] not in ['mysql', 'information_schema', 'performance_schema','sys']:
        mycursor.execute(f"USE {database[0]}") # select the database
        mycursor.execute("SHOW TABLES")
        for (table_name,) in mycursor:
              tables.append(table_name)
        available.append((database[0],tables))

    mycursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;")

    myresult = mycursor.fetchall()
    # Connect to MySQL database using the provided host and port
    # and check if username and password match your database records
    # Open and read the file as a single buffer

    if filename:
      fd = open('filename', 'r', encoding="utf-8")
      sqlFile = fd.read()
      fd.close()

      # all SQL commands (split on ';')
      sqlCommands = sqlFile.split(';\n')
      #sqlCommands = re.split(r";\n|;;\n|\$\$\n|//\n",sqlFile)
      #print(sqlCommands[0])
      #for block in sqlCommands:
      #  vers = block[0:4].replace(' ','')
      #  vers = vers.replace('\n','')
      #  if vers == ';' or "-":
      #     
      #     lines = block.split(';\n')
      #     for line in lines:
      #        print("line:", line)
      #        mycursor.execute(line)
      #  print('-----------------------------------------------------------------')
#
             
      # Execute every command from the input file
      for command in sqlCommands:
          try:
              print(command)
              mycursor.execute(command, multi=True)
          except mysql.connector.Error as err:
              print(F"Error: {err}")
      
    return render_template('index.html',myresult=myresult, username=username, host=host, port=port,available=available)

@app.route('/')
def login():
    return render_template('login.html')




@app.route('/database', methods=['POST'])
def view_table():
    global username
    global host
    global port
    global password
    print(request.form)
    data  = request.form
    value = data.getlist('value')[0]
    value = value.split(",")
    db = value[0]
    table = value[1]

    mydb = mysql.connector.connect(
      host=host,
      user=username,
      password=password,
      database = db
    )
    mycursor = mydb.cursor()
    print(mycursor)
    print(db, table)
    mycursor.execute(f"SELECT * FROM {table} LIMIT 50;")

    myresult = mycursor.fetchall()

    field_names = [i[0] for i in mycursor.description]
    print(field_names)
    print('Showing '+db+'.'+table)

    return render_template('database.html',myresult= myresult,table=table, field_names=field_names, db=db)

@app.route('/new', methods=['POST'])
def new():
    return render_template('new.html')

@app.route('/show', methods=['POST'])
def show():
    
    global username
    global host
    global port
    global password
    mydb = mysql.connector.connect(
      host=host,
      user=username,
      password=password
    )
    mycursor = mydb.cursor()
    
    for x in request.form:
      if x == 'filename':
        filename = request.form['filename']
    if filename:
      fd = open(filename, 'r', encoding="utf-8")
      sqlFile = fd.read()
      fd.close()

      # all SQL commands (split on ';')
      sqlCommands = sqlFile.split(';\n')
      #print(sqlCommands)
      # Execute every command from the input file
      #for command in sqlCommands:
      # print(command)
      # try:
      #     print(command)
      #     mycursor.execute(command)
      # except OperationalError:
      #     print(F"Command skipped: {command}")
  
    return render_template('show.html', doc=sqlCommands ,filename=filename, username=username, host=host,port=port,password=password)

@app.route('/table_menu', methods=['POST'])
def table_menu():
    action  = request.form
    val = action.getlist('value')[0]
    val = val.split(',')
    db = val[2]
    global username
    global host
    global port
    global password
    mydb = mysql.connector.connect(
      host=host,
      user=username,
      password=password,
      database = db
    )
    if val[0] == 'drop':

      
      mycursor = mydb.cursor()

      mycursor.execute(f"SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME='{val[1]}';")
      constaints = mycursor.fetchall()
      temp = []
      for constraint in constaints:
         
         if constraint[0] != 'PRIMARY':
          temp.append(constraint[0])
      
      print(temp)

      for x in temp:
        mycursor.execute(f'ALTER TABLE {val[1]} DROP FOREIGN KEY {x};')

      mycursor.execute(f"SET foreign_key_checks = 0;")
      mycursor.execute(f"DROP TABLE IF EXISTS {val[1]}")
      mycursor.execute(f"SET foreign_key_checks = 1;")
 
      mycursor.execute("SHOW Tables")
      print(mycursor.fetchall())
      return val

    if val[0] == 'filter':

      return val
    
