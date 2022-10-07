from flask import Flask
import requests
import basedonnee as bd
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


if __name__ == '__main__':
    app.run()
