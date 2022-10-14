import time
from flask import Flask
import requests
import basedonnee as bd
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

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
    date = r['localObsDateTime'][0:10]
    heure = r['localObsDateTime'][11:19]
    return [temperature, humidte, pressionAtmos, date, heure]

def resReq(nomVille):
    maRequete = requeteToJson(nomVille)
    return [infosVille(maRequete), infosReleve(maRequete)]

@app.route('/demo')
def demo():
    tab = resReq("Montréal")
    bd.deleteDatabase()
    bd.createDatabase()
    bd.ajoutPays(tab[0][1])
    bd.ajoutVille(tab[0][0])
    x = bd.getIdVille(tab[0][0])
    bd.ajoutReleve(tab[1][0],tab[1][1],tab[1][2],tab[1][3],x)
    return tab

def resetDatabase():
    bd.deleteDatabase()
    bd.createDatabase()

def getData(ville):
    tab = resReq(ville)
    y = bd.getVille(ville)
    if not y:
        bd.ajoutVille(tab[0][0])
    x = bd.getPays(tab[0][1])
    if not x:
        bd.ajoutPays(tab[0][1])
    x = bd.getIdVille(tab[0][0])
    bd.ajoutReleve(tab[1][0], tab[1][1], tab[1][2], tab[1][3], x)

def automatization():
    getData("Montréal")
    print("done")
    getData("Roubaix")
    print("done")
    getData("Paris")
    print("done")
    getData("Strasbourg")
    print("done")
    getData("Marseille")
    print("done")
    getData("Lyon")
    print("done Lyon")


#resetDatabase()
scheduler = BackgroundScheduler()
scheduler.add_job(func=automatization, trigger="interval", seconds=15)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run()
