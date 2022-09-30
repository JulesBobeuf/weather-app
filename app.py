from flask import Flask
import requests

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

def requeteToJson(ville):
    r = requests.get(f'https://wttr.in/{ville}?format=j1')
    infosJson = r.json()
    return infosJson


def infosVille(jsonRequest):
    r = jsonRequest['nearest_area'][0]
    nomVille = r['areaName'][0]['value']
    nomPays = r['country'][0]['value']
    return [nomVille, nomPays]


def infosReleve(jsonRequest):
    r = jsonRequest['current_condition'][0]
    temperature = r['temp_C']
    humidte = r['humidity']
    pressionAtmos = r['pressure']
    date = r['localObsDateTime'][0:9]
    heure = r['localObsDateTime'][11:19]
    return [temperature, humidte, pressionAtmos, date, heure]

def resReq(nomVille):
    maRequete = requeteToJson(nomVille)
    return [infosVille(maRequete), infosReleve(maRequete)]


if __name__ == '__main__':
    app.run()
