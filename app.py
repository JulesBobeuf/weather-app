import time
from flask import Flask
import requests
import basedonnee as bd
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'PAGE ACCUEIL AVEC FORMULAIRE!'

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
    if (tab[0][0] == "Montreal"):
        ville = "Montreal"
    elif (tab[0][0] == "Saint-Merri"):
        ville = "Paris"
    elif (tab[0][0] == "Strassbourg"):
        ville = "Strasbourg"
    elif (tab[0][0] == "Madrague De la Ville"):
        ville = "Marseille"
    elif (tab[0][0] == "Fourviere"):
        ville = "Lyon"

    y = bd.getVille(ville)
    if not y:
        bd.ajoutVille(ville)
    x = bd.getPays(tab[0][1])
    if not x:
        bd.ajoutPays(tab[0][1])
    x = bd.getIdVille(ville)
    bd.ajoutReleve(tab[1][0], tab[1][1], tab[1][2], tab[1][3], x)

def automatization():
    getData("Montreal")
    print("done Montreal")
    getData("Roubaix")
    print("done Roubaix")
    getData("Paris")
    print("done Paris")
    getData("Strasbourg")
    print("done Strasbourg")
    getData("Marseille")
    print("done Marseille")
    getData("Lyon ")
    print("done Lyon")

#print(bd.relevePourUneVille("Montreal")) A TESTER ( avec une route web maybe et une fonction + return
#resetDatabase()
scheduler = BackgroundScheduler()
scheduler.add_job(func=automatization, trigger="interval", seconds=10)
#scheduler.start()

atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run()
