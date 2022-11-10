import atexit
from datetime import datetime
from flask import Flask, render_template, app
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField
from wtforms.validators import DataRequired
import requests
import basedonnee as bd
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import matplotlib.pyplot as plt
import os

import basedonnee as bd
import visualisationDonnees


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
        )
    else:
        app.config.from_mapping(test_config)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/formulaire', methods=['GET', 'POST'])
    def accueil():
        form = CityForm()
        if form.validate_on_submit():
            nomVille = form.name.data
            dateDebut = form.dateDebut.data
            dateFin = form.dateFin.data

            donneesRecentes = bd.relevePourUneVille(nomVille)
            tabReleveVille = bd.relevePourUneVilleEtDate(nomVille, dateDebut, dateFin)
            visualisationDonnees.temperatureVisu([x[4] for x in tabReleveVille], [x[1] for x in tabReleveVille])
            visualisationDonnees.humiditeVisu([x[4] for x in tabReleveVille], [x[2] for x in tabReleveVille])
            visualisationDonnees.pressionVisu([x[4] for x in tabReleveVille], [x[3] for x in tabReleveVille])

            return render_template('infosVille.html', nom=nomVille, dateDebut=dateDebut, dateFin=dateFin,
                                   tabReleveVille=tabReleveVille, donneesRecentes=donneesRecentes[-1])

        return render_template('form.html', form=form)

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
        humidite = r['humidity']
        pressionAtmos = r['pressure']
        date = r['localObsDateTime'][0:10]
        heure = r['localObsDateTime'][11:19]
        return [temperature, humidite, pressionAtmos, date, heure]

    def resReq(nomVille):
        maRequete = requeteToJson(nomVille)
        return [infosVille(maRequete), infosReleve(maRequete)]

    @app.route('/demo')
    def demo():
        tab = bd.resReq("Montréal")
        bd.deleteDatabase()
        bd.createDatabase()
        bd.ajoutPays(tab[0][1])
        bd.ajoutVille(tab[0][0])
        x = bd.getIdVille(tab[0][0])
        bd.ajoutReleve(tab[1][0], tab[1][1], tab[1][2], tab[1][3], tab[1][4], x)
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
        bd.ajoutReleve(tab[1][0], tab[1][1], tab[1][2], tab[1][3], tab[1][4], x)
        logger(ville, tab[1][3], tab[1][4])

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
        getData("Lyon")
        print("done Lyon")

    @app.route('/test', methods=['GET', 'POST'])
    def test():
        tab = bd.relevePourUneVilleEtDate('Roubaix', '2022-10-10', '2022-10-15')
        print(tab[0][0], tab[0][1], tab)
        return "x"

    @app.route('/test2', methods=['GET', 'POST'])
    def graph():
        tab = bd.relevePourUneVilleEtDate('Roubaix', '2022-10-10', '2022-10-30')

        plt.xlabel("time")
        plt.ylabel("temperature")
        temperature = []
        datereleve = []
        for i in range(len(tab)):
            temperature.append(tab[i][1])
            datereleve.append(tab[i][5])
        plt.plot(datereleve, temperature)
        plt.show()
        return "x"

    def logger(ville, jour, heure):
        val = "\nData added for " + str(ville) + " at " + str(jour) + " " + str(heure) + " local time. "
        with open('logs.txt', 'a') as f:
            f.write(val)

    class CityForm(FlaskForm):
        name = SelectField(u'Villes :',
                           choices=[('Roubaix', 'Roubaix'), ('Paris', 'Paris'), ('Strasbourg', 'Strasbourg'),
                                    ('Lyon', 'Lyon'), ('Marseille', 'Marseille'), ('Montreal', 'Montreal')])
        dateDebut = DateField('Date', format='%Y-%m-%d')
        dateFin = DateField('Date', format='%Y-%m-%d', default=datetime.today())

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=automatization, trigger="interval", seconds=3600)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    return app
