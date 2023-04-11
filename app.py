from flask import Flask

app = Flask(__name__)

@app.route("/")

def database_terminal():
    
    return "<p>test!</p> <button>button</button>"