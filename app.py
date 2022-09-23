from flask import Flask
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

def createDatabase():
    con = sql.connect('bd.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE VILLE ( idVille int primary key, nomVille varchar, nomPays varchar);''')
    cur.execute('''CREATE TABLE RELEVE ( idReleve int primary key, temperature int, dateDuReleve date, idVille varchar REFERENCES VILLE(idVille));''')
    con.commit()
    con.close()

def ajoutVille(ville,pays):
    values = "\'"+ville+"\',\'"+pays
    con = sql.connect('bd.db')
    cur = con.cursor()
    cur.execute("INSERT INTO VILLE(nomVille,nomPays) VALUES ( " + values + ");")
    con.commit()
    con.close()

if __name__ == '__main__':
    app.run()
