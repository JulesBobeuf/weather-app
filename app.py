from flask import Flask
import requests

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
    date = r['localObsDateTime'][0:9]
    heure = r['localObsDateTime'][11:19]
    return [temperature, date, heure]


@app.route('/json')
def affichage():
    maRequete = requeteToJson('Lens')
    return [infosVille(maRequete), infosReleve(maRequete)]


if __name__ == '__main__':
    app.run()
